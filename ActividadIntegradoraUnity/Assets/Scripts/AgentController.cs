using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class CarData
{
    public int uniqueID;
    public Vector3 position;
}

public class AgentData
{
    public List<Vector3> positions;
}

public class ModelState{
    public bool isDone;
}

public class AgentController : MonoBehaviour
{  
    //Server paramaters
    [SerializeField] string url;
    [SerializeField] string testEP;
    [SerializeField] string initEP;
    [SerializeField] string updateEP;
    [SerializeField] string agentsEP;
    [SerializeField] string boxesEP;
    [SerializeField] string stateEP;

    //Model parameters
    [SerializeField] float density;
    [SerializeField] int numberRobots;
    [SerializeField] int baseX;
    [SerializeField] int baseZ;
    [SerializeField] float updateDelay; //In seconds
    [SerializeField] int floorWidth; 
    [SerializeField] int floorHeight;
    [SerializeField] GameObject carPrefab;
    [SerializeField] GameObject floorPrefab;
    [SerializeField] GameObject BoxPrefab;
    [SerializeField] GameObject WallPrefab;
    
    //Unity parameters
    [SerializeField] Camera MainCamera;
    GameObject floor;
    Camera mainCamera;
    GameObject[] agents;
    GameObject[] boxes;
    GameObject[] walls;
    List<Vector3> oldPositions;
    List<Vector3> newPositions;
    List<Vector3> oldPositionsBox;
    List<Vector3> newPositionsBox;
     // Pause the simulation while we get the update from the server
    bool hold = true;
    bool holdBoxes = false;

    public float timer, dt;

    //float updateTime = 0;
    AgentData carsData, obstacleData;
    ModelState isDone;

    // Start is called before the first frame update
    void Start()
    {   
        isDone = new ModelState();
        carsData = new AgentData();
        obstacleData = new AgentData();
        oldPositions = new List<Vector3>();
        newPositions = new List<Vector3>();
        oldPositionsBox = new List<Vector3>();
        newPositionsBox = new List<Vector3>();

        timer = updateDelay;

        agents = new GameObject[numberRobots];
        walls = new GameObject[4];

        //Floor instantiation
        //Scales the width and height of the floor according to given parameters
        floor = Instantiate(floorPrefab, Vector3.zero, Quaternion.identity);
        Vector3 floorScale = new Vector3(floorWidth, floorHeight, 1f);
        floor.transform.localScale = floorScale;
        //Makes the bottom left corner start in (-0.5,0,-0.5) so the robots align with the grid
        float newWidth = floorWidth; //Makes the values floats so floating point operations can be done correctly
        float newHeight = floorHeight;
        floor.transform.position = new Vector3(newWidth/2 - 0.5f, 0, newHeight/2 - 0.5f);
        //Makes the Quad prefab horizontal
        floor.transform.eulerAngles = new Vector3(floor.transform.eulerAngles.x + 90, floor.transform.eulerAngles.y, floor.transform.eulerAngles.z);

        //Makes walls for each side
        for (int i = 0; i < 4; i++){
            walls[i] = Instantiate(WallPrefab, Vector3.zero, Quaternion.identity);
        }
        //Left Wall
        walls[0].name = "Left wall";
        walls[0].transform.position = new Vector3(-1f, 0.5f, newHeight/2 - 0.5f);
        walls[0].transform.localScale = new Vector3(1f, 1f, floorHeight);
        
        //Right Wall
        walls[1].name = "Right wall";
        walls[1].transform.position = new Vector3(floorWidth, 0.5f, newHeight/2 - 0.5f);
        walls[1].transform.localScale = new Vector3(1f, 1f, floorHeight);

        //Lower Wall
        walls[2].name = "Lower wall";
        walls[2].transform.position = new Vector3(newWidth/2 - 0.5f, 0.5f, -1f);
        walls[2].transform.localScale = new Vector3(floorWidth + 2, 1f, 1f);

        //Upper Wall
        walls[3].name = "Upper wall";
        walls[3].transform.position = new Vector3(newWidth/2 - 0.5f, 0.5f, floorHeight);
        walls[3].transform.localScale = new Vector3(floorWidth + 2, 1f, 1f);

        //Sets the camera angle so all the plane is visible (works best with wide aspect ratios)
        mainCamera = Camera.main;
        int biggestIfWH = isBiggest(floorWidth, floorHeight); 
        if (floorHeight == floorWidth){
            mainCamera.transform.position = new Vector3(floorWidth/2, biggestIfWH/2, floorHeight/3 * -1f);
        }
        else if (biggestIfWH == floorWidth){
            mainCamera.transform.position = new Vector3(floorWidth/2, biggestIfWH/2, floorHeight/3 * -1f);
        }
        else{
            mainCamera.transform.position = new Vector3(floorWidth/2, biggestIfWH/2, floorHeight/3 * -1f);
        }
        
        //cars = new GameObject[numberRobots];
        for(int i = 0; i < numberRobots; i++){
            agents[i] = Instantiate(carPrefab, Vector3.zero, Quaternion.identity);
        }

        StartCoroutine(TestConnection());
        StartCoroutine(SendConfiguration());
    }

    // Update is called once per frame
    void Update()
    {   
        float t = timer/updateDelay;
        // Smooth out the transition at start and end
        dt = t * t * ( 3f - 2f*t);

        // Smooth out the transition at start and end
        if (timer >= updateDelay){
            timer = 0;
            hold = true;
            holdBoxes = true;
            StartCoroutine(GetModelState()); //Checks if the model is done
            StartCoroutine(UpdatePositions()); //Moves agents and boxes
        }

        if(!hold && !holdBoxes && !isDone.isDone){
            //Moves agents
            for (int s = 0; s < agents.Length; s++)
            {   
                if (newPositions.Count > 0 && oldPositions.Count > 0)
                {
                    /* Vector3 interpolated = Vector3.Lerp(oldPositions[s], newPositions[s], dt);
                    agents[s].transform.localPosition = interpolated; */
                    agents[s].transform.localPosition = newPositions[s]; //Movement in "skips"
                    
                    Vector3 dir = newPositions[s] - oldPositions[s];
                    agents[s].transform.rotation = Quaternion.LookRotation(dir);
                }
            }

            //Moves boxes
            for (int s = 0; s < boxes.Length; s++)
            {
                if(newPositionsBox.Count > 0 && oldPositionsBox.Count > 0){
                    //Interpolation works, but is funky because of the way agent positions are reported
                    /* Vector3 interpolatedBox = Vector3.Lerp(oldPositionsBox[s], newPositionsBox[s], dt);
                    boxes[s].transform.localPosition = interpolatedBox; */
                    boxes[s].transform.localPosition = newPositionsBox[s]; //Movement in "skips"
                }
            }

            timer += Time.deltaTime;
        }
    }

    IEnumerator TestConnection(){
        UnityWebRequest www = UnityWebRequest.Get(url + testEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
        }
        else{
            Debug.Log(www.error);
        }
    }

    IEnumerator GetModelState(){
        UnityWebRequest www = UnityWebRequest.Get(url + stateEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success){
            isDone = JsonUtility.FromJson<ModelState>(www.downloadHandler.text);

            if (isDone.isDone == true)
            {
                Debug.Log("Model done");
            }
        }
        else{
            Debug.Log(www.error);
        }
    }

    IEnumerator SendConfiguration(){

        WWWForm form = new WWWForm();
        //Sends the variables given in Unity, to the model
        form.AddField("numberRobots", numberRobots.ToString());
        form.AddField("density", density.ToString());
        form.AddField("floorWidth", floorWidth.ToString());
        form.AddField("floorHeight", floorHeight.ToString());
        form.AddField("baseX", baseX.ToString());
        form.AddField("baseZ", baseZ.ToString());

        UnityWebRequest www = UnityWebRequest.Post(url + initEP, form);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
            StartCoroutine(GetObstacleData());
            StartCoroutine(UpdateBoxData());
            StartCoroutine(GetRobotsData());
        }
        else{
            Debug.Log(www.error);
        }
    }

    IEnumerator UpdatePositions(){
        UnityWebRequest www = UnityWebRequest.Get(url + updateEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
            StartCoroutine(UpdateBoxData());
            StartCoroutine(GetRobotsData());
        }
        else{
            Debug.Log(www.error);
        }
    }

    IEnumerator GetRobotsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(url + agentsEP);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            carsData = JsonUtility.FromJson<AgentData>(www.downloadHandler.text);

            // Store the old positions for each agent
            oldPositions = new List<Vector3>(newPositions);

            newPositions.Clear();

            foreach(Vector3 v in carsData.positions)
                newPositions.Add(v);

            hold = false;
        }
    }

    //Instantiates all boxes and asigns them inside the boxes array
    IEnumerator GetObstacleData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(url + boxesEP);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            obstacleData = JsonUtility.FromJson<AgentData>(www.downloadHandler.text);
            boxes = new GameObject[obstacleData.positions.Count];

            for (int i = 0; i < obstacleData.positions.Count; i++)
            {
                Vector3 newPosition = obstacleData.positions[i];
                boxes[i] = Instantiate(BoxPrefab, newPosition, Quaternion.identity);
            }

            /* foreach(Vector3 position in obstacleData.positions)
            {
                Instantiate(BoxPrefab, position, Quaternion.identity);
            } */
        }
    }

    //Fetches the position of each box
    IEnumerator UpdateBoxData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(url + boxesEP);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            obstacleData = JsonUtility.FromJson<AgentData>(www.downloadHandler.text);

            // Store the old positions for each agent
            oldPositionsBox = new List<Vector3>(newPositionsBox);

            newPositionsBox.Clear();

            foreach(Vector3 v in obstacleData.positions)
                newPositionsBox.Add(v);

            holdBoxes = false;
        }
    }

    int isBiggest(int width, int height){
        if(width > height){
            return width;
        }
        else{
            return height;
        }
    }
}