import plotly.express as px

from pandas_to_charts.core import make_chart_data
from pandas_to_charts.data_configs.constructors import Libraries, ChartTypes

# get sample data from plotly express
df = px.data.gapminder()


def test_simple_bar_chart():
    fig = make_chart_data(df[df['year'] == 2007], x='country', y='gdpPercap', library=Libraries.HIGHCHARTS,
                          chart_type=ChartTypes.bar)
    assert len(fig) == 1
    assert len(fig[0]['data']) == 142
    assert fig[0]['type'] == 'bar'
    countries_sample = ['Australia', 'Austria', 'Bahrain', 'Bangladesh', 'Belgium', 'Benin', 'Bolivia',
                        'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Burundi',
                        'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China',
                        'Colombia', 'Comoros', 'Congo, Dem. Rep.', 'Congo, Rep.', 'Costa Rica', "Cote d'Ivoire",
                        'Croatia', 'Cuba', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominican Republic', 'Ecuador',
                        'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Ethiopia', 'Finland', 'France',
                        'Gabon', 'Gambia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Guinea', 'Guinea-Bissau']
    assert all(x in [a['name'] for a in fig[0]['data']] for x in countries_sample)


def test_stacked_bar_chart():
    fig = make_chart_data(df[df['year'] == 2007], x='country', y='gdpPercap', colors='continent',
                          library=Libraries.HIGHCHARTS,
                          chart_type=ChartTypes.bar)
    assert len(fig) == 5
    assert len(fig[1]['data']) == len(fig[2]['data']) == 142
    vals_oceania = [(x['name'], x['y']) for x in fig[4]['data'] if x['y'] != 0]
    assert len(vals_oceania) == 2
    assert vals_oceania == [('Australia', 34435), ('New Zealand', 25185)]
    assert fig[0]['type'] == 'bar'


def test_pie_chart():
    fig = make_chart_data(df[df['year'] == 2007], x='country', y='gdpPercap',
                          library=Libraries.HIGHCHARTS,
                          chart_type=ChartTypes.pie)
    assert len(fig) == 1
    assert len(fig[0]['data']) == 142
    assert fig[0]['type'] == 'pie'


def test_heatmap_chart():
    fig = make_chart_data(df[(df['year'] == 2007) | (df['year'] == 1962)], x='country', y='gdpPercap', colors='year',
                          library=Libraries.HIGHCHARTS,
                          chart_type=ChartTypes.heatmap)
    assert len(fig[0]['data']) == 284
    assert fig[0]['type'] == 'heatmap'
