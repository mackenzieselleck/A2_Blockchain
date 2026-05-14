from flask import Flask, request, render_template

#imports all necessary python code to run
from task_1 import task_1
from task_2 import task_2
from task_2 import mal_input
from task_3 import get_query
from task_3 import task_3


app = Flask(__name__)


#renders HTML page
@app.route('/')
def home():

    return render_template('index.html')

#receives HTML POST input and runs Task 1
@app.route('/task1', methods=['POST'])
def run_task_1():

    #collects user input
    actual = request.form['actual']
    claim = request.form['claim']
    quantity = request.form['quantity']
    price = request.form['price']
    location = request.form['location']

    #keeps signature verification and record for Task 2 use
    global record
    global ver

    #runs Task 1
    ver, result, record = task_1(actual, claim, quantity, price, location)


    #displays Task 1 output to HTML
    return render_template(
        'index.html',
        task_1_result=result
    )



#receives HTML POST input and runs Task 2
@app.route('/task2', methods=['POST'])
def run_task_2():

    #receives malicious node input
    m = request.form['malicious']

    #runs basic input sanitisation
    valid, mal = mal_input(m)

    #if sanitisation error, display error
    if not valid:
        return render_template(
        'index.html',
        task_2_error=mal
    )

    #run Task 2
    result = task_2(mal, record, ver)
   
    #displays Task 2 output to HTML
    return render_template(
        'index.html',
        task_2_result=result
    )



#receives HTML POST input and runs Task 3
@app.route('/task3', methods=['POST'])
def run_task_3():

    #collects user input
    user = request.form['user']
    query = request.form['query']

    #runs basic input sanitisation
    valid, q = get_query(query)

    #if sanitisation error, display error
    if not valid:
         return render_template(
        'index.html',
        task_3_error=q
    )

    #runs Task 3
    result = task_3(user, query)

    #displays Task 3 output to HTML
    return render_template(
        'index.html',
        task_3_result=result
    )


#runs HTML program
if __name__ == "__main__":

    app.run(debug=True)