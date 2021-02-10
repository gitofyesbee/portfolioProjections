from flask import Flask, render_template, request, session
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from simulateReturns import simulate_returns
import createreports as cr
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)


@app.route('/', methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
@app.route("/home.html", methods=['POST', 'GET'])
@app.route("/index.html", methods=['POST', 'GET'])
def home():
    return render_template("index.html")


@app.route('/input/')
@app.route("/input.html/")
def input_data():
    present_value = ""
    if 'present_value' in session:
        present_value = str(session["present_value"])
        print(present_value)
        print(session)
    return render_template("input.html", current_val=present_value)


@app.route('/output/', methods=['POST', 'GET'])
@app.route("/output.html/", methods=['POST', 'GET'])
def results():
    if request.method == 'GET':
        # redirect to input html if output is typed directly
        return render_template("input.html")
    if request.method == 'POST':

        # check DOB format and update to right one, if required
        dob = request.form['date_of_birth']
        if len(dob) == 10:
            dob = datetime.strptime(dob, '%Y-%m-%d')
        # user has entered only year and month, append 1st date of the month
        elif len(dob) == 7:
            dob = dob + "-01"
            dob = datetime.strptime(dob, '%Y-%m-%d')
        # user has entered only year , append 1st date of the month and 1st month of the year
        else:
            dob = dob + "-01-01"
            dob = datetime.strptime(dob, '%Y-%m-%d')

        # get user input
        current_age = relativedelta(date.today(), dob).years
        retirement_planned_age = int(request.form['retirement_age'])
        iterations = int(request.form['iterations'])
        present_value = float(request.form['present_value'])
        expected_roi = float(request.form['expected_roi'])
        standard_deviation = float(request.form['standard_deviation_of_expected_returns'])
        annual_savings_till_retirement = float(request.form['annual_savings_till_retirement'])
        annual_withdrawal_in_retirement = float(request.form['annual_withdrawal_in_retirement'])
        max_age = int(request.form['max_age'])

        # setup session variables
        session['current_age'] = current_age
        session['retirement_planned_age'] = retirement_planned_age
        session['iterations'] = iterations
        session['present_value'] = present_value
        session['expected_roi'] = expected_roi
        session['standard_deviation'] = standard_deviation
        session['annual_savings_till_retirement'] = annual_savings_till_retirement
        session['annual_withdrawal_in_retirement'] = annual_withdrawal_in_retirement
        session['max_age'] = max_age

        # run the returns
        target_percentile_subset, pass_percentile, pass_percentile_value, final_year_median_value, verdict, improve = simulate_returns(
            iterations, present_value, expected_roi, standard_deviation, current_age, retirement_planned_age,
            annual_savings_till_retirement, annual_withdrawal_in_retirement, max_age)
        chart_display, chart_div, cdn_js = cr.create_reports(target_percentile_subset)

        if improve:
            set_hidden = ""
        else:
            set_hidden = "hidden"

        return render_template("output.html",
                               passing_percentile=pass_percentile,
                               passing_percentile_value=pass_percentile_value,
                               median_value_in_final_year=final_year_median_value,
                               percentile_dataset=target_percentile_subset,
                               plan_verdict=verdict,
                               chart_to_display=chart_display,
                               div_for_chart=chart_div,
                               suggest_improvements=set_hidden,
                               chart_js=cdn_js[0], chart_js_tables=cdn_js[2], chart_js_widgets=cdn_js[1])


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
