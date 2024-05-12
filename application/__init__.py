from flask import Flask
from flask_pymongo import pymongo
app = Flask(__name__)

# Setup MongoDB connection
app.config["SECRET_KEY"] = "c15bf8093aa07284f719e278c3dd8cc8dbdc46c3"
conn = "mongodb+srv://laaria:laaria9251@cluster0.g9lsxqg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(conn, serverSelectionTimeoutMS=10000)
db = client.db

# Import routes
from application import routes