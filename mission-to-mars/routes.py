from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)
# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn)
# db = client.missions_to_mars
# mars_data = db.mars_data



@app.route("/")
def home():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    scraped_data = scrape_mars.scrape()
    mongo.db.mars_data.replace_one({}, scraped_data, upsert=True)
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)