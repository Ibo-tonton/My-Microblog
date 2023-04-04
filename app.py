from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient 
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    # Create a client
    client = MongoClient(os.getenv("MONGODB_URI")) 
    # Connecting the client to a db (microblog db created in our claster) and put the db value inside the app
    app.db = client.microblog
    
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
   
