from flask import Flask, render_template, request
import datetime
import os
from dotenv import load_dotenv

# load_dotenv is going to populate our environment variables from the content of a file called .env
load_dotenv()
# That is going to allow us to open up a client side session to MongoDB that we can use to connect to our DB
from pymongo import MongoClient 
# The request variable is a value that has sthg inside it whenever we are in 
# a function that is currently responding to a request.
# This is going to populate our environment variable from the contexts of a file called .env that we'll create

def create_app():
    app = Flask(__name__)
    # Create a client
    client = MongoClient(os.getenv("MONGODB_URL")) 
    # Connecting the client to a db (microblog db created in our claster) and put the db value inside the app
    app.db = client.microblog
    #mongodb+srv://ibourahim:gataman@microblog-app.uk864co.mongodb.net/test&ssl=true&ssl_cert_reqs=CERT_NONE
    @app.route('/', methods=["GET", "POST"])
    def home(): 
    #print([a for a in app.db.posts.find({})])
        if request.method == "POST":
                # "content" is the name assigned to the texterea in the html file.
                entry_content = request.form.get("content")
                # Telling the datetime object to format itself as a string in the format %Y-%m-%d
                formatted_date = datetime.datetime.today().strftime('%Y-%m-%d')
                app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date = [
                (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
                )
                for entry in app.db.entries.find({})
            ]
            
        return render_template("home.html", entries=entries_with_date)

    return app
   
