from flask import Flask, request, render_template


from task_2 import task_2
from task_2 import mal_input
from task_3 import get_query
from task_3 import task_3




app = Flask(__name__)


@app.route('/')
def home():

    return render_template('index.html')



@app.route('/task2', methods=['POST'])
def run_task_2():

    m = request.form['malicious']

    valid, mal = mal_input(m)

    if not valid:
         return render_template(
        'index.html',
        task_2_error=mal
    )

    result = task_2(mal)

    return render_template(
        'index.html',
        task_2_result=result
    )


@app.route('/task3', methods=['POST'])
def run_task_3():

    user = request.form['user']
    query = request.form['query']

    valid, q = get_query(query)

    if not valid:
         return render_template(
        'index.html',
        task_3_error=q
    )

    result = task_3(user, query)

    return render_template(
        'index.html',
        task_3_result=result
    )



if __name__ == "__main__":

    app.run(debug=True)