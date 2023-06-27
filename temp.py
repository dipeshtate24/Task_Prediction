import pickle
from flask import Flask, request, render_template
import pandas as pd
import gspread

SHEET_ID = '1fT9DAsWvy2m9a-m6G3qzPko5DTZutSaf9tjqKIm9Af8'
SHEET_NAME1 = 'Task Description'
gc = gspread.service_account('task-390105-15d7ca9eff5c.json')

app = Flask(__name__)

model = pickle.load(open('models/predict_model.pkl', 'rb'))

def get_description():
    spreadsheet = gc.open_by_key(SHEET_ID)
    worksheet = spreadsheet.worksheet(SHEET_NAME1)
    df = worksheet.get_all_records()
    task_description = pd.DataFrame(df)
    return task_description

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods = ['POST'])
def predict():
    course = request.form['Course']
    int_task = int(request.form['Task'])
    completion = request.form['Completion']

    int_course = 0
    if course == 'Full Stack Stack Developer':
        int_course = 1
    elif course == 'Digital Marketing':
        int_course = 2

    int_completion = 0
    if completion == 'Yes':
        int_completion = 1


    next_task = model.predict([[int_course, int_task, int_completion]])

    output = round(next_task[0][0])



    task_description = get_description()
    name = ' '
    desc = ' '
    for x in task_description['Task Id']:
        if x == output:
            name = task_description.loc[task_description['Task Id'] == x, ['Task Name']]
            desc = task_description.loc[task_description['Task Id'] == x, ['Task Description']]
            break
    else:
        print("Please check if the given number is valid or not")

    return render_template('result.html', Prediction_Tasks='Next task is {}'.format(output), Task_Name=name.iloc[0, 0], Task_Description=desc.iloc[0, 0])

if __name__  == "__main__":
    app.run(debug=True)

