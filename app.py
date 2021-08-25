import yaml
from flask import Flask, jsonify, request
import json

app = Flask(__name__)


@app.route("/")
def hello():
    return jsonify({"welcome": "There isn't anything here, YET! For now requests can be made through the normal endpoints."})
 

def saveAuth(list, id):
    writeFile = open("storage.json", 'w')
    list.append(id)
    print("saved the id:"+str(id)+" to the auth list.")
    writeFile.write(json.dumps(list))

# Handle API Requests


@app.route("/auth/<int:id>", methods=['POST', 'GET'])
def getAuth(id):

    # Setup
    yamlIn = yaml.safe_load(open("config.yml", 'r'))
    content = request.headers.get("secret")
    POST_AUTH_SECRET = str(yamlIn["POSTsecret"])
    GET_AUTH_SECRET = str(yamlIn["GETsecret"])
    print(content)
    inputStream = open("storage.json", 'r')
    storageObject = json.load(inputStream)
    AUTH_LIST = []
    for inter in storageObject:
        AUTH_LIST.append(inter)

    # Handle Request

    # Post
    if request.method == 'POST':
        if (content == None or content != POST_AUTH_SECRET):
            return jsonify({"result": "Your POST request secret is invalid!"}), 401
        saveAuth(AUTH_LIST, id)
        return jsonify({"result": "Sucsessfully added the id="+str(id)+" to the authentication list"}), 200

    # Get
    content = request.headers.get("secret")
    print(content)

    if (content == None or content != GET_AUTH_SECRET):
        return jsonify({"result": "Your GET request secret is invalid!"}), 401

    if (AUTH_LIST.__contains__(id)):
        return jsonify({"result": "Sucsess. The ID provided is verified.", "access": True}), 200
    else:
        return jsonify({"result": "Failure. The ID prodivded is NOT verified.", "access": False}), 200


if __name__ == '__main__':
    app.run(debug=True)
