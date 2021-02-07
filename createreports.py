import bokeh as bk
from bokeh.plotting import figure
from bokeh.models import Band, Range1d
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.palettes import Spectral11
from bokeh.models import NumeralTickFormatter
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def set_chart_title_properties(chart_to_set):
    chart_to_set.title.align = "center"
    chart_to_set.title.text_font_size = "15px"
    return chart_to_set


def draw_span(span_at_value, span_color, span_direction='width', span_width=2, span_dash='solid'):
    span_to_return = bk.models.Span(location=span_at_value, line_color=span_color, dimension=span_direction,
                                    line_width=span_width, line_dash=span_dash)
    return span_to_return


def create_reports(simulated_returns):
    returns_to_chart = simulated_returns.transpose()

    # Chart setup
    plan_chart = figure(width=700, height=400)
    plan_chart.x_range = Range1d(0, len(returns_to_chart.index))
    # plan_chart.add_layout(Title(text="Plan", text_font_size="15px", align="center"), 'above')

    # Error Charts setup
    plan_error_chart = figure(width=500, height=300, title="Your plan fails, rerun with different data")
    plan_error_chart = set_chart_title_properties(plan_error_chart)

    zero_span = draw_span(0, 'green', 'width', 2, 'dashed')

    # Chart 1: Final year simulated values
    number_of_lines = len(returns_to_chart.columns)
    my_palette = Spectral11[0:number_of_lines]
    plan_chart.multi_line(xs=[returns_to_chart.index.values] * number_of_lines,
                          ys=[returns_to_chart[years].values for years in returns_to_chart], line_color=my_palette,
                          line_width=2)
    plan_chart.renderers.extend([zero_span])
    plan_chart.yaxis[0].formatter = NumeralTickFormatter(format="($ 0.00 a)")
    plan_chart.xaxis[0].formatter = NumeralTickFormatter(format="0,0")
    # Chart 1: Error chart
    plan_chart.line(x=100, y=0)

    try:
        chart_display, chart_div = components(plan_chart)
    except ValueError:
        chart_display, chart_div = components(plan_error_chart)

    cdn_js = CDN.js_files
    return chart_display, chart_div, cdn_js
