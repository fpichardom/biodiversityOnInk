from flask import Flask, render_template, request, redirect, url_for, flash
from webapp.dbmodels import mongo


app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

@app.route('/')

def home():