from flask import Flask, render_template, request
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from simulateReturns import simulate_returns

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
        return render_template("input.html")
    if request.method == 'POST':
        # run the returns
        dob = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d')
        print(type(dob))
        current_age = relativedelta(date.today(), dob).years

        simulated_returns = simulate_returns(request.form['iterations'],
                                             request.form['present_value'],
                                             request.form['expected_roi'],
                                             request.form['standard_deviation_of_expected_returns'],
                                             current_age,
                                             request.form['retirement_age'],
                                             request.form['annual_savings_till_retirement'],
                                             request.form['annual_withdrawal_in_retirement'],
                                             request.form['max_age'])
        value_to_be_returned = "<div class='container-info'><p> The entered value from previous screen is: " + str(
            simulated_returns) + ".</p></div>"
        return render_template("output.html", div2=value_to_be_returned, div1=current_age)


@app.route('/input/')
@app.route("/input.html/")
def input_data():
    return render_template("input.html")


if __name__ == '__main__':
    app.run(debug=True)
