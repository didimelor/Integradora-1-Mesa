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

public class AgentController : MonoBehaviour
{  
    //Server paramaters
    [SerializeField] string url;
    [SerializeField] string testEP;
    [SerializeField] string initEP;
    [SerializeField] string updateEP;
    [SerializeField] string agentsEP;
    [SerializeField] string boxesEP;

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
    
    //Unity parameters
    [SerializeField] Camera MainCamera;
    GameObject floor;
    Camera mainCamera;
    GameObject[] agents;
    GameObject[] boxes;
    List<Vector3> oldPositions;
    List<Vector3> newPositions;
    List<Vector3> oldPositionsBox;
    List<Vector3> newPositionsBox;
     // Pause the simulation while we get the update from the server
    bool hold = false;

    public float timer, dt;

    float updateTime = 0;
    AgentData carsData, obstacleData;

    // Start is called before the first frame update
    void Start()
    {
        carsData = new AgentData();
        obstacleData = new AgentData();
        oldPositions = new List<Vector3>();
        newPositions = new List<Vector3>();
        oldPositionsBox = new List<Vector3>();
        newPositionsBox = new List<Vector3>();

        agents = new GameObject[numberRobots];

        //Floor instantiation
        //Scales the width and height of the floor according to given parameters
        floor = Instantiate(floorPrefab, Vector3.zero, Quaternion.identity);
        Vector3 floorScale = new Vector3(floorWidth, floorHeight, 1f);
        floor.transform.localScale = floorScale;
        //Makes the bottom left corner start in (-0.5,0,-0.5) so the robots align with the grid
        float newWidth = floorWidth;
        float newHeight = floorHeight;
        floor.transform.position = new Vector3(newWidth/2 - 0.5f, 0, newHeight/2 - 0.5f);
        //Makes the Quad prefab horizontal
        floor.transform.eulerAngles = new Vector3(floor.transform.eulerAngles.x + 90, floor.transform.eulerAngles.y, floor.transform.eulerAngles.z);

        //Sets the camera angle so all the plane is visible (works best with wide aspect ratios)
        mainCamera = Camera.main;
        int biggestIfWH = isBiggest(floorWidth, floorHeight); 
        if (floorHeight == floorWidth){
            mainCamera.transform.position = new Vector3(floorWidth/2, biggestIfWH, floorHeight/2);
        }
        else if (biggestIfWH == floorWidth){
            mainCamera.transform.position = new Vector3(floorWidth/2, biggestIfWH/2, floorHeight/2);
        }
        else{
            mainCamera.transform.position = new Vector3(floorWidth/2, biggestIfWH, floorHeight/2);
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
        if (updateTime > updateDelay){
            updateTime = 0;
            hold = true;
            StartCoroutine(UpdatePositions());   
        }

        if(!hold){
            for (int s = 0; s < agents.Length; s++)
            {

                agents[s].transform.localPosition = newPositions[s];
                boxes[s].transform.localPosition = newPositionsBox[s];

                /* Vector3 interpolated = Vector3.Lerp(oldPositions[s], newPositions[s], dt);
                agents[s].transform.localPosition = interpolated;
                
                Vector3 dir = oldPositions[s] - newPositions[s];
                agents[s].transform.rotation = Quaternion.LookRotation(dir);
                */
            }

            for (int s = 0; s < boxes.Length; s++)
            {
                boxes[s].transform.localPosition = newPositionsBox[s];

                /* Vector3 interpolated = Vector3.Lerp(oldPositions[s], newPositions[s], dt);
                agents[s].transform.localPosition = interpolated;
                
                Vector3 dir = oldPositions[s] - newPositions[s];
                agents[s].transform.rotation = Quaternion.LookRotation(dir);
                */
            }

            updateTime += Time.deltaTime;
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

            //hold = false;
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