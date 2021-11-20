from flask import Flask, request, jsonify
from random import uniform

app = Flask("Coordinate Server")

num_agents = 0
limit = 25

def randomPoint():
    return {"x": uniform(-limit, limit), "y": 0.2, "z": uniform(-limit, limit)}

#Create the flask server
@app.route("/")
def default():
    print("Recieved a requests at /")
    return "This is working!"

@app.route("/config", methods=['POST'])
def configure():
    global num_agents
    num_agents = int(request.form.get("numAgents"))
    print(f"Received num_agents = {num_agents}")
    return jsonify({"OK": num_agents})

@app.route("/update", methods=['GET'])
def update_positions():
    points = [randomPoint() for _ in range(num_agents)]
    print(f"Positions: {points}")
    return jsonify({"positions": points})

app.run()