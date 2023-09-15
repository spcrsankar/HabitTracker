from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)


    app.client = MongoClient(os.getenv("Mongo_URI"))
    app.db = app.client.Habit_tracker

    @app.context_processor
    def date_processor():
        def date_range(date):
            days = []
            date =  datetime.strptime(date, "%Y-%m-%d")
            for i in range(-3,4):
                temp =[]
                temp.extend((date + timedelta(days=i)).strftime("%b %d").split(" "))
                temp.append((date + timedelta(days=i)).strftime("%Y-%m-%d"))
                days.append(temp)
            return days
        return {"date_range":date_range}

    @app.route('/',methods=['GET'])
    def index():

        # load date 
        data = {}
        for d in app.db.habits.find({}):
            data = d
    
        habits = data["habit"] or []
        habits_completion = data["completed"] or {}

        date = request.args.get("date")
        if not date:
            date = datetime.today().strftime("%Y-%m-%d")

        if date not in habits_completion:
            habits_completion[date] = []

        return render_template('index.html',habits=habits,selected_date=date,habits_completion=habits_completion)


    @app.route('/add',methods=['GET','POST'])
    def add():
        if request.method == 'POST':
            habit = request.form.get('habit')

            # insert into db
            data = {}
            for d in app.db.habits.find({}):
                data = d

            data["habit"].append(habit)
            app.db.habits.delete_many({})
            app.db.habits.insert_one(data)

            return redirect(url_for('index'))
        return render_template('add.html',selected_date = datetime.today().strftime("%Y-%m-%d"))

    @app.route('/complete',methods=['POST'])
    def complete():
        habit = request.form.get('habit').strip()
        date = request.form.get('date')

        # insert into db
        data = {}
        for d in app.db.habits.find({}):
            data = d

        if date not in data["completed"]:
            data["completed"][date] = []
        completed = data["completed"][date]
        completed.append(habit)
        data["completed"][date] = completed
        app.db.habits.delete_many({})
        app.db.habits.insert_one(data)

        return redirect(url_for('index',date=date))
    return app