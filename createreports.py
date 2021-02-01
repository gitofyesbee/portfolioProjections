import pandas as pd
import bokeh as bk
from bokeh.plotting import figure
from bokeh.models import Band
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.layouts import gridplot
from bokeh.models import Title, NumeralTickFormatter
from flask import request
import locale


def set_chart_title_properties(chart_to_set):
    chart_to_set.title.align = "center"
    chart_to_set.title.text_font_size = "15px"
    return chart_to_set


def draw_span(span_at_value, span_color, span_direction='width', span_width=2, span_dash='solid'):
    span_to_return = bk.models.Span(location=span_at_value, line_color=span_color, dimension=span_direction,
                                    line_width=span_width, line_dash=span_dash)
    return span_to_return


def create_reports(simulated_returns):
    # get the final year simulation
    final_year = len(simulated_returns) - 1
    final_year_simulation = pd.DataFrame({'Simulation': simulated_returns.loc[final_year].index,
                                          'Ending Value': simulated_returns.loc[final_year].values})
    final_year_simulation = final_year_simulation.set_index('Simulation')

    # generate percentile report
    percentile_to_report = 0.05
    percentile_report = []
    for i in range(18):
        percentile_value = (1 - percentile_to_report)
        quantile_dollar = final_year_simulation['Ending Value'].quantile(percentile_to_report)
        percentile_report.append((percentile_value, quantile_dollar))
        percentile_to_report = percentile_to_report + 0.05
    df_percentile_report = pd.DataFrame(percentile_report, columns=['Probability', 'Ending $'])

    # get the highest probability of success
    probability_of_success_calc = df_percentile_report[df_percentile_report['Ending $'] > 0].min()

    try:
        probability_of_success = round((float(
            df_percentile_report.loc[df_percentile_report['Ending $'] == probability_of_success_calc['Ending $']][
                'Probability']) * 100), 2)
    except TypeError:
        probability_of_success = 0
    label_probability_of_success_value = (
            "Your plan's probability of success is " + str(probability_of_success) + "%")

    # Plan verdict
    if 0 <= probability_of_success < 60:
        label_success = "Guaranteed to fail. Rehash plan"
    elif 60 <= probability_of_success < 70:
        label_success = "Risky, recheck parameters. Exercise caution."
    elif 70 <= probability_of_success < 80:
        label_success = "Your plan is okay. Continue monitoring."
    elif 80 <= probability_of_success < 85:
        label_success = "Good Job. Your plan has a very high probability of success"
    else:
        label_success = "Congratulations. Unless there is a global catastrophe, your plan will succeed."

    # inputs for final year chart
    median_value = final_year_simulation['Ending Value'].median()
    percentile_target_value = float((df_percentile_report.loc[df_percentile_report['Probability'] == 0.85]['Ending $']))
    label_median = "After " + str(request.form['iterations']) + " simulations, the median is : " \
                   + (locale.currency(median_value, grouping=True))

    # Chart setup
    scatter_chart = figure(background_fill_color="#fafafa", tools="pan,wheel_zoom,box_zoom,reset,save")
    scatter_chart.add_layout(Title(text=label_median, text_font_size="15px", align="center"), 'above')
    percentile_chart = figure(background_fill_color="#fafafa", tools="pan,wheel_zoom,box_zoom,reset,save")
    percentile_chart.add_layout(Title(text=label_success, text_font_style="italic", align="center"), 'above')
    percentile_chart.add_layout(Title(text=label_probability_of_success_value,
                                      text_font_size="15px", align="center"), 'above')

    # Error Charts setup
    scatter_error_chart = figure(background_fill_color="#fafafa", title="Your plan fails, rerun with different data")
    percentile_error_chart = figure(background_fill_color="#fafafa", title="Your plan fails, rerun with different data")
    scatter_error_chart = set_chart_title_properties(scatter_error_chart)
    percentile_error_chart = set_chart_title_properties(percentile_error_chart)

    percentile_target_span = draw_span(percentile_target_value, 'brown', 'width', 2)
    median_span = draw_span(median_value, 'green', 'width', 2, 'dotted')
    zero_span = draw_span(0, 'darkgrey', 'width', 2, 'dotted')
    probability_of_success_span = draw_span(probability_of_success_calc['Ending $'], 'black', 'width', 1)

    # Chart 1: Final year simulated values
    scatter_chart.scatter(x=final_year_simulation.index, y=final_year_simulation['Ending Value'],
                          line_color=None, fill_color='blue', fill_alpha=0.3, size=10, legend_label="simulated end $")
    # scatter_chart.grid.bounds = (mean - std, mean + std)
    scatter_chart.xaxis.axis_label = "Simulations"
    scatter_chart.yaxis.axis_label = "Ending $"
    scatter_chart.xgrid.grid_line_color = None
    scatter_chart.yaxis[0].formatter = NumeralTickFormatter(format="($ 0.00 a)")
    scatter_chart.xaxis[0].formatter = NumeralTickFormatter(format="0,0")
    scatter_chart.renderers.extend([percentile_target_span, median_span])

    # Chart 1: Error chart
    scatter_error_chart.scatter(x=final_year_simulation.index, y=0,
                                line_color=None, fill_color='blue', fill_alpha=0.3, size=10)
    scatter_error_chart.xgrid.grid_line_color = None

    # Chart 2: Final year percentile graph
    percentile_chart.vbar(x=df_percentile_report.index, top=df_percentile_report['Ending $'], width=0.9)
    percentile_chart.xaxis.axis_label = "Success Percentile"
    percentile_chart.yaxis.axis_label = "Ending $"
    percentile_chart.xgrid.grid_line_color = None
    percentile_chart.yaxis[0].formatter = NumeralTickFormatter(format="($ 0.00 a)")
    percentile_chart.xaxis[0].ticker = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    percentile_chart.xaxis.major_label_overrides = {0: '95%', 1: '90%', 2: '85%', 3: '80%', 4: '75%', 5: '70%',
                                                    6: '65%',
                                                    7: '60%', 8: '55%', 9: '50%', 10: '45%', 11: '40%', 12: '35%',
                                                    13: '30%',
                                                    14: '25%', 15: '20%', 16: '15%', 17: '10%', 18: '5%', 19: '0%'}
    percentile_chart.renderers.extend([zero_span, probability_of_success_span])

    # Chart 2: Error chart
    percentile_error_chart.vbar(x=df_percentile_report.index, top=0, width=0.9)
    percentile_error_chart.xgrid.grid_line_color = None

    # write the outputs
    combine_charts = gridplot([scatter_chart, percentile_chart], ncols=1, merge_tools=False,
                              plot_height=200, sizing_mode="scale_width")
    combine_error_charts = gridplot([scatter_error_chart, percentile_error_chart], ncols=1,
                                    plot_height=200, sizing_mode="scale_width")
    try:
        chart_display, chart_div = components(combine_charts)
    except ValueError:
        chart_display, chart_div = components(combine_error_charts)

    cdn_js = CDN.js_files
    return_package = {"chart_to_display": chart_display,
                      "div_for_chart": chart_div,
                      "cdn_script": cdn_js}
    return return_package
