from flask import Flask, request, render_template , send_file
import json
import random
import calendar
import datetime
import pymongo

app = Flask(__name__)
SENSORS = ['a','b','c']
deviceControl = { "led1" : "Off" , "led2" : "Off", "led3" : "Off"};

##Pymongo Interfacing
client = pymongo.MongoClient()
db = client.dummy_database
collection = db.sensorData

@app.route('/')
def hello_world():
    return 'Welcome to the Fish. Tank.!'

@app.route('/sensor/<sensor_id>/')
def sensor_data(sensor_id):
    data = {}
    numResults = 1
    params = request.args.to_dict()
    if not params['t']:
        return 404

    now = calendar.timegm(datetime.datetime.now().timetuple())*1000
    print(now)

    data["oxygen"]=[]
    for post in collection.find({"date":{"$lt":now,"$gt":now-2000000}}):
        print(post)
        data["oxygen"].append([post["date"],post["oxygen"]])
        ##print(collection.find({"date":{"$lt":now,"$gt":now-2000000}}).count())

    print(data)
    return json.dumps(data)

@app.route('/dashboard')
def show_dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html')

def log_user_in(name):
    return 'Welcome'+name

def valid_login(username, password):
    print((username, password))
    return True

@app.route('/<device_id>/toggle', methods=['PUT'])
def toggle(device_id):
    if not device_id in deviceControl:
        return ("Device " + device_id + " does not exist",404)
    if deviceControl[device_id] == 'Off':
        deviceControl[device_id] = 'On'
    else:
        deviceControl[device_id] = 'Off'
    return ("Success",202)

@app.route('/<device_id>/state', methods=['POST','GET'])
def state(device_id):
    if device_id == "~":
        return json.dumps(deviceControl)
    elif not device_id in deviceControl:
        return ("Device " + device_id + " does not exist",404)
    return deviceControl[device_id]

@app.route('/deviceList', methods=['GET'])
def deviceList():
    return json.dumps([i for i in deviceControl.keys()])


@app.route('/uploadImage', methods=['POST'])
def uploadImage():
    data = request.get_data()
    newFileByteArray = bytearray(data)
    with open('test.jpeg','wb') as newFile:
            newFile.write(data)
    return 'Image Sent!'

@app.route('/recentImage')
def recentImage():
     return send_file('test.jpeg', mimetype='image/gif')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
