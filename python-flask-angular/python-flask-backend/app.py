from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import yaml

app = Flask(__name__)
with open('database.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
client = MongoClient(config['uri'])

db = client['knf-dev']
CORS(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/users', methods=['POST', 'GET'])
def data():
    
 
    if request.method == 'POST':
        body = request.json
        firstName = body['firstName']
        lastName = body['lastName']
        emailId = body['emailId'] 
        
        db['users'].insert_one({
            "firstName": firstName,
            "lastName": lastName,
            "emailId":emailId
        })
        return jsonify({
            'status': 'Data is posted to MongoDB!',
            'firstName': firstName,
            'lastName': lastName,
            'emailId':emailId
        })
    
   
    if request.method == 'GET':
        allData = db['users'].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            firstName = data['firstName']
            lastName = data['lastName']
            emailId = data['emailId']
            dataDict = {
                'id': str(id),
                'firstName': firstName,
                'lastName': lastName,
                'emailId': emailId
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)

@app.route('/users/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    
    if request.method == 'GET':
        data = db['users'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        firstName = data['firstName']
        lastName = data['lastName']
        emailId = data['emailId']
        dataDict = {
            'id': str(id),
            'firstName': firstName,
            'lastName': lastName,
            'emailId':emailId
        }
        print(dataDict)
        return jsonify(dataDict)
        
    
    if request.method == 'DELETE':
        db['users'].delete_many({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

   
    if request.method == 'PUT':
        body = request.json
        firstName = body['firstName']
        lastName = body['lastName']
        emailId = body['emailId']

        db['users'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "firstName":firstName,
                    "lastName":lastName,
                    "emailId": emailId
                }
            }
        )

        print('\n # Update successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is updated!'})

if __name__ == '__main__':
    app.debug = True
    app.run()