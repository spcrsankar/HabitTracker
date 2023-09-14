from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
app = Flask(__name__)

habits = []
habits_completion = {}  #{"2019-09-8":[list of habits],"2019-09-9":[list of habits]}

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

@app.route('/',methods=['GET','POST'])
def index():
    date = request.args.get("date")
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")
    print(date)
    if date not in habits_completion:
        habits_completion[date] = []
    print(habits_completion)
    return render_template('index.html',habits=habits,selected_date=date,habits_completion=habits_completion)


@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        habit = request.form.get('habit')
        habits.append(habit)
        return redirect(url_for('index'))
    return render_template('add.html',selected_date = datetime.today().strftime("%Y-%m-%d"))

@app.route('/complete',methods=['POST'])
def complete():
    habit = request.form.get('habit').strip()
    date = request.form.get('date')
    habits_completion[date].append(habit)
    print(habits_completion[date],habits_completion)
    return redirect(url_for('index',date=date))