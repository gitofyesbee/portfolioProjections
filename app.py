from flask import Flask, render_template, request
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from simulateReturns import simulate_returns
import createreports as cr

app = Flask(__name__)


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
    return render_template("input.html")


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

        # run the returns
        current_age = relativedelta(date.today(), dob).years
        retirement_planned_age = int(request.form['retirement_age'])
        target_percentile_subset, pass_percentile, pass_percentile_value, final_year_median_value, verdict = \
            simulate_returns(request.form['iterations'],
                             request.form['present_value'],
                             request.form['expected_roi'],
                             request.form['standard_deviation_of_expected_returns'],
                             current_age,
                             retirement_planned_age,
                             request.form['annual_savings_till_retirement'],
                             request.form['annual_withdrawal_in_retirement'],
                             request.form['max_age'])
        chart_display, chart_div, cdn_js = cr.create_reports(target_percentile_subset)

        return render_template("output.html",
                               passing_percentile=pass_percentile,
                               passing_percentile_value=pass_percentile_value,
                               median_value_in_final_year=final_year_median_value,
                               percentile_dataset=target_percentile_subset,
                               plan_verdict=verdict,
                               chart_to_display=chart_display,
                               div_for_chart=chart_div,
                               chart_js=cdn_js[0], chart_js_tables=cdn_js[2], chart_js_widgets=cdn_js[1])


if __name__ == '__main__':
    app.run(debug=True)
