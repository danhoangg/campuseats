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
import os

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



# mydict = {"name": "lissan", 
#           "email": "lissan@example.com",
#           "pfp":"lissan.png",
#           "bio":"I am a cool guy",
#           "year": "1",
#           "course": "Computer Science",
#           "pictures":["pic1.png", "pic2.png", "pic3.png"],
#           "gender":"male",
#           "who-liked-them":["oleg@example.com"],
#           "seen":["lissan@example.com"],
#           "messages":{}
#           }

# x = mycol.insert_one(mydict)

# print("inserted")
# print(x.inserted_id)

places_for_dates = {
   "kcl.ac.uk": [{"Strand Campus":0.9, "Waterloo Campus":0.4, "Guy's Campus":0.6, "Denmark Hill Campus":0.7}],
   "soton.ac.uk": [{"Highfield Campus":0.9, "Avenue Campus":0.4, "Boldrewood Campus":0.6, "Winchester Campus":0.7}],
}




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
    mydict["messages"] = {}
    mydict["pictures"] = []
    mydict["who-liked-them"] = []
    mydict["disliked"] = []
    mydict["liked"] = []
    mydict["pfp"] = "default.png"
    mydict["elo"] = "1000"


# mydict = {"name": "lissan", 
#           "email": "lissan@example.com",
#           "pfp":"lissan.png",
#           "bio":"I am a cool guy",
#           "year": "1",
#           "course": "Computer Science",
#           "pictures":["pic1.png", "pic2.png", "pic3.png"],
#           "gender":"male",
#           "who-liked-them":["oleg@example.com"],
#           "seen":["lissan@example.com"],
#           "messages":{}

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

    email = data["email"]
    domain = email.split("@")[1]
    if domain.endswith("ac.uk"):

        print(data)
        insert_user_db(data)

        return "OK"
    
    print("You are not a student, use university email ending ac.uk")
    return "You are not a student, use university email ending ac.uk"


@app.route("/get-user-info", methods=["GET"])
def get_user_info():
    email = request.args.get("email")
    
    user = mycol.find({"email": email})
    print(user)
    for i in user:
      print(i)
      del i["_id"] # so it doesn't have to steralize the object, we delete the object
      return json.dumps({"users": i})
    else:
      return "User not found"
    
@app.route("/update-user-info", methods=["POST"])
def update_user_info():
    data = request.get_json()
    print("data", data)

    email = data["email"]

    # check if user exists
    response = requests.get("http://lissan.dev:8050/get-user-info?email=" + email).text
    if response == "User not found":
       response = requests.post("http://lissan.dev:8050/add-user", json=data).text
       if response == "You are not a student, use university email ending ac.uk":
          return "You are not a student", 403
       return "Ok", 200

    mycol.update_one({"email": email}, {"$set": data})
    return "OK", 200



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

           return json.dumps({"messages": all_messages})

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
            print("existing_messages", existing_messages)
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
            mycol.update_one({"email": other}, {"$set": {"messages": existing_messages}})
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
            contact_list.append([email, i["name"], i["pfp"]])

      return json.dumps({"contact_list": contact_list})

    return json.dumps({"contact_list": []})


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
    return json.dumps({"email":decoded_jwt["email"]})


@app.route('/upload-pfp', methods=['POST'])
def upload_file():
    email = request.args.get("email")
    print(email)

    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400 
    if file:
        filename = str(datetime.now()) + "-" + email.split("@")[0] + "-pfp.png"
        file.save(os.path.join("media/", filename))

        mycol.update_one({"email": email}, {"$set": {"pfp": filename}})

        return json.dumps({"filename":filename})



@app.route("/recommendations", methods=["GET"])
def recommendations():
    print("recommendations")
    email = request.args.get("email")
    users = mycol.find()
    all_emails = []
    for user in users:
       all_emails.append(user["email"])
    all_emails.remove(email) # remove yourself

    print(all_emails)

    users = mycol.find({"email": email})
    for user in users:
        user_elo = user["elo"]

        print("liked", user["liked"])
        disliked = user["disliked"] + user["liked"]
        print("disliked", disliked)
        for email in disliked:
            print("email", email)
            try:
                all_emails.remove(email)
            except:
                pass
    
    if len(all_emails) == 0:
        return json.dumps({"recommendations": []})
    
    lowest_difference = float("inf")
    most_closest_email = ""
    for other_ppl_email in all_emails:
        other = mycol.find({"email": other_ppl_email})
        for i in other:
            other_ppl_elo = i["elo"]
            # expected value

            current_difference = abs(float((user_elo).strip("\"")) - float((other_ppl_elo).strip("\"")))

            if current_difference < lowest_difference:
                lowest_difference = current_difference
                most_closest_email = other_ppl_email

    
    users = mycol.find({"email": most_closest_email})
    for i in users:
        del i["_id"]
        return json.dumps(i)



@app.route("/i-like", methods=["GET"])
def i_like():
    who_liked = request.args.get("email")
    print("who_liked", who_liked)

    liked = request.args.get("liked")

    liked_user = mycol.find({"email": liked})
    for i in liked_user:
       liked_user_who_liked_them = i["who-liked-them"]
       liked_user_who_liked_them.append(who_liked)
       
    mycol.update_one({"email": liked}, {"$set": {"who-liked-them": liked_user_who_liked_them}})
    mycol.update_one({"email": liked}, {"$set": {"elo": str(float((i["elo"]).strip("\"")) + 20)}})




    # CHECK IF THEY BOTH LIKED EACH OTHER, IF SO ADD EACH OTHER TO MESSAGES
    user = mycol.find({"email": who_liked})
    # add liked person to who liked messages
    for i in user:
        liked_person = i["who-liked-them"]
        messages = i["messages"]

        user_liked = i["liked"]
        user_liked.append(liked)
        mycol.update_one({"email": who_liked}, {"$set": {"liked": user_liked}})

        print("liked_person", liked_person)
        if liked in liked_person:
            print("SUCESS")
            # THIS MEAN THEY BOTH LIKE EACHER OTHER

            # SO NOW PUT EACH OTHER IN THEIR MESSAGES

            messages[liked] = [[]]
            mycol.update_one({"email": who_liked}, {"$set": {"messages": messages}})

            # add who liked to liked person messages
            user = mycol.find({"email": liked})
            for i in user:
                messages = i["messages"]
                messages[who_liked] = [[]]
                mycol.update_one({"email": liked}, {"$set": {"messages": messages}})

    return "OK"


@app.route("/disliked", methods=["GET"])
def disliked():
    email = request.args.get("email")
    
    disliked = request.args.get("disliked")

    user = mycol.find({"email": email})
    for i in user:
       disliked_list = i["disliked"]
       disliked_list.append(disliked)

    mycol.update_one({"email": email}, {"$set": {"disliked": disliked_list}})

    mycol.update_one({"email": disliked}, {"$set": {"elo": str(float((i["elo"]).strip("\"")) - 10)}})

    return "OK"


# app.run(host='0.0.0.0', port=8050, debug=False)

socketio.run(app, host='0.0.0.0', debug=False, port=8050)