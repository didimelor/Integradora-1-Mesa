from re import X
from flask import Flask, request, jsonify
from model import *

app = Flask("Act int 1 server")

numberRobots = 5
floorWidth = 15
floorHeight = 15
density = 0.65
trafficModel = None
baseX = 0
baseZ = 0
counter = 0

#Create the flask server
@app.route("/")
def default():
    print("Recieved a requests at /")
    return "Inital connection successful!"

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global trafficModel, numberRobots, floorWidth, floorHeight, baseX, baseZ, density

    if request.method == 'POST':
        number_agents = int(request.form.get('numberRobots'))
        width = int(request.form.get('floorWidth'))
        height = int(request.form.get('floorHeight'))
        baseX = int(request.form.get('baseX'))
        baseZ = int(request.form.get('baseZ'))
        density = float(request.form.get('density'))

        print(request.form)
        print(number_agents, width, height)
        trafficModel = FloorTiles(height, width, density, numberRobots, baseX, baseZ)

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global trafficModel

    if request.method == 'GET':
        #carPositions = [{"x": x, "y":0, "z":z} for (a, x, z) in trafficModel.grid.coord_iter() if isinstance(a, cargador)]
        carPositions = []
        for (c, x, z) in trafficModel.grid.coord_iter():
            for contents in c:
                if(isinstance(contents, cargador)):
                    carPositions.append({"x":x, "y":0, "z":z})

        return jsonify({'positions':carPositions})

@app.route('/getObstacles', methods=['GET'])
def getObstacles():
    global trafficModel

    if request.method == 'GET':
        #boxPositions = [{"x": x, "y":0, "z":z} for (a, x, z) in trafficModel.grid.get_cell_list_contents() if isinstance(a, caja)]
        boxPositions = []
        for (c, x, z) in trafficModel.grid.coord_iter():
            for contents in c:
                if(isinstance(contents, caja)):
                    boxPositions.append({"x":x, "y":0.5, "z":z})

        return jsonify({'positions':boxPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global counter, trafficModel
    if request.method == 'GET':
        trafficModel.step()
        counter += 1
        return jsonify({'message':f'Model updated to step {counter}.', 'currentStep':counter})

""" if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True) """

app.run()