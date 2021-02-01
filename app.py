from flask import Flask, render_template, request
from dateutil.relativedelta import relativedelta
from datetime import date, datetime


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
@app.route("/home.html", methods=['POST', 'GET'])
@app.route("/index.html", methods=['POST', 'GET'])
def home():
        return render_template("index.html")

@app.route('/output/', methods=['POST', 'GET'])
@app.route("/output.html/", methods=['POST', 'GET'])
def results():
    if request.method == 'GET':
        # return f"The URL /output is accessed directly. Try going to 'home' to submit form"
        return render_template("inputdata.html")
    if request.method == 'POST':
        # run the returns

        dob = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d')
        print(type(dob))
        current_age = relativedelta(date.today(),dob).years

        value_entered = [request.form['iterations'],
                         request.form['present_value'],
                         request.form['expected_roi'],
                         request.form['standard_deviation_of_expected_returns'],
                         current_age,
                         request.form['retirement_age'],
                         request.form['annual_savings_till_retirement'],
                         request.form['annual_withdrawal_in_retirement'],
                         request.form['max_age']]
        value_to_be_returned = "<p> The entered value from previous screen is: " + str(
            value_entered) + ".</p>"
        return render_template("output.html", div=value_to_be_returned)


@app.route('/input/')
@app.route("/inputdata.html/")
@app.route("/input.html/")
@app.route("/inputdata")
def inputdata():
    return render_template("inputdata.html")


if __name__ == '__main__':
    app.run(debug=True)
