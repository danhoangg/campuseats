import pymongo
from flask import Flask, send_from_directory, request, redirect, make_response, send_file
from pymongo.server_api import ServerApi
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from flask_socketio import SocketIO
from datetime import datetime
import requests
from flask_cors import CORS
import jwt


# ENV_FILE = find_dotenv()
# if ENV_FILE:
#     load_dotenv(ENV_FILE)



app = Flask("dating-app")
CORS(app)
app.secret_key = env.get("APP_SECRET_KEY")

socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


# # oauth = OAuth(app)

# # oauth.register(
# #     "auth0",
# #     client_id=env.get("AUTH0_CLIENT_ID"),
# #     client_secret=env.get("AUTH0_CLIENT_SECRET"),
# #     client_kwargs={
# #         "scope": "openid profile email",
# #     },
# #     server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
# # )

# # print(f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration')

# # @app.route("/login")
# # def login():
# #     return oauth.auth0.authorize_redirect(
# #         redirect_uri=url_for("callback", _external=True)
# #     )

# # @app.route("/callback", methods=["GET", "POST"])
# # def callback():
# #     token = oauth.auth0.authorize_access_token()
# #     session["user"] = token
# #     print("token", token)
# #     return redirect("/")

# # @app.route("/logout")
# # def logout():
# #     session.clear()
# #     return redirect(
# #         "https://" + env.get("AUTH0_DOMAIN")
# #         + "/v2/logout?"
# #         + urlencode(
# #             {
# #                 "returnTo": url_for("home", _external=True),
# #                 "client_id": env.get("AUTH0_CLIENT_ID"),
# #             },
# #             quote_via=quote_plus,
# #         )
# #     )


# @app.route("/")
# def home():
#     if "user" not in session:
#         # Redirect to the login page
#         return redirect(url_for("login"))
#     return render_template("index.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))





myclient = pymongo.MongoClient("mongodb+srv://admin:admin@dating-app.5bmxqgt.mongodb.net/?retryWrites=true&w=majority")
print("this")

mydb = myclient["dating-app"]

print("Database: ", myclient.list_database_names())

dblist = myclient.list_database_names()
if "dating-app" in dblist:
  print("The database exists.")



mycol = mydb["users"]

print(mydb.list_collection_names())

collist = mydb.list_collection_names()
if "users" in collist:
  print("users exists.")


mydict = {"name": "lissan", 
          "email": "lissan@example.com",
          "profile-pic":"lissan.png",
          "bio":"I am a cool guy",
          "Year": "1",
          "Course": "Computer Science",
          "pictures":["pic1.png", "pic2.png", "pic3.png"],
          "gender":"male",
          "who-liked-them":["oleg@example.com"],
          "seen":["lissan@example.com"],
          "messages":{}
          }

x = mycol.insert_one(mydict)


places_for_dates = {
   "kcl.ac.uk": [{"Strand Campus":0.9, "Waterloo Campus":0.4, "Guy's Campus":0.6, "Denmark Hill Campus":0.7}],
   "soton.ac.uk": [{"Highfield Campus":0.9, "Avenue Campus":0.4, "Boldrewood Campus":0.6, "Winchester Campus":0.7}],
}


print("inserted")
print(x.inserted_id)


def check_email_exists(email):
    myquery = {"email": email}

    mydoc = mycol.find(myquery)

    print(mydoc)

    for x in mydoc:
      print("This object (user) already exists: ", x)
      return True
    return False


def insert_user_db(user_info):
    mydict = user_info

    # check user exists
    if not check_email_exists(user_info["email"]):
      x = mycol.insert_one(mydict)
      print("inserted")
      print(x.inserted_id)
      return "Sucess"
    print("User already exists")
    return "User already exists"


@app.route("/add-user", methods=["POST"])
def add_user():
    print(request.args)
    data = request.get_json()

    print(data)
    insert_user_db(data)

    return "OK"


@app.route("/get-user-info", methods=["GET"])
def get_user_info():
    email = request.args.get("email")
    
    user = mycol.find({"email": email})
    for i in user:
      print(i)
      return {"users": str(i)}
    else:
      return "User not found"


@app.route("/messages", methods=["GET"])
def get_messages():
    user = request.args.get("user")
    other = request.args.get("other")

    user = mycol.find({"email": user})
    for i in user:
      messages = i["messages"]
      for message in messages:
        if message == other:
           all_messages = messages[message]
           # sort all the messages by date time
           # [("14:20", "this is the message",True),("14:21", "recieved this message",False)]

           return {"messages": all_messages}

    return "404"



@app.route("/send-message", methods=["POST", "GET"])
def send_message():
    user = request.args.get("user")
    other = request.args.get("other")
    sent_message = request.args.get("message")

    did_something = False

    sender_user = mycol.find({"email": user})
    print("sender_user", sender_user)
    for i in sender_user:
        messages = i["messages"]
        print("messages", messages)
        print(other in messages)
        if other in messages:
            for message in messages:
                if message == other:
                    messages[message].append([str(datetime.now().strftime('%H:%M')), sent_message, True])
                    mycol.update_one({"email": user}, {"$set": {"messages": messages}})
                    did_something = True
                    print("did 1")
        else:
            existing_messages = messages
            existing_messages[other] = [[str(datetime.now().strftime('%H:%M')), sent_message, True]]
            mycol.update_one({"email": user}, {"$set": {"messages": existing_messages}})
            did_something = True

    did_something = False
    
    reciever_user = mycol.find({"email": other})
    print("reciever_user", reciever_user)
    for i in reciever_user:
        messages = i["messages"]
        if user in messages:
            for message in messages:
                if message == user:
                    messages[message].append([str(datetime.now().strftime('%H:%M')), sent_message, False])
                    mycol.update_one({"email": other}, {"$set": {"messages": messages}})
                    did_something = True
                    print("did 2")
        else:
            existing_messages = messages
            existing_messages[user] = [[str(datetime.now().strftime('%H:%M')), sent_message, False]]
            did_something = True
           
        
    if did_something:
      return "OK"

    return "404"


@app.route("/contact-list", methods=["GET", "POST"])
def contact_list():
    user = request.args.get("user")

    user = mycol.find({"email": user})
    for i in user:
      messages = i["messages"]
      contact_list = []
      for message in messages:
        email = message
        print("email:", email)
        
        user = mycol.find({"email": email})
        print(user)
        for i in user:
            contact_list.append([email, i["name"], i["profile-pic"]])

      return {"contact_list": contact_list}

    return "404"


#
@socketio.on('some_event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    socketio.emit('message_from_server', {'data': 'This is a message from Flask!'})


@app.route("/media/<path:path>")
def send_media(path):
    return send_from_directory("media", path)


@app.route("/give-me-email")
def give_me_email():
    jwt_code = request.args.get("jwt")
    decoded_jwt = jwt.decode(jwt_code, options={"verify_signature": False})
    print(decoded_jwt)
    return decoded_jwt["email"]


@app.route("/upload-image", methods=["POST"])
def upload_image():
    print(request.files)
    file = request.files['file']
    print(file)
    file.save("media/" + file.filename)
    return "OK"



# app.run(host='0.0.0.0', port=8050, debug=False)

socketio.run(app, host='0.0.0.0', debug=False, port=8050)
