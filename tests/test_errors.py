import pandas as pd
import plotly.express as px
import pytest

from pandas_to_charts.core import make_chart_data
from pandas_to_charts.data_configs.constructors import Libraries, ChartTypes
from pandas_to_charts.exceptions import NoDataToDisplay, ChartTypeNotImplemented, LibraryNotImplemented

df = px.data.gapminder()


def test_empty_df():
    with pytest.raises(NoDataToDisplay):
        make_chart_data(df=pd.DataFrame(), x='country', y='gdpPercap', colors='continent',
                        library=Libraries.PLOTLY,
                        chart_type=ChartTypes.bar)


def test_wrong_library():
    with pytest.raises(LibraryNotImplemented):
        make_chart_data(df=df, x='country', y='gdpPercap', colors='continent',
                        library=10,
                        chart_type=ChartTypes.bar)


def test_wrong_chart_type():
    with pytest.raises(ChartTypeNotImplemented):
        make_chart_data(df=df, x='country', y='gdpPercap', colors='continent',
                        library=Libraries.PLOTLY,
                        chart_type=99)

    with pytest.raises(ChartTypeNotImplemented):
        make_chart_data(df=df, x='country', y='gdpPercap', colors='continent',
                        library=Libraries.HIGHCHARTS,
                        chart_type=99)


def test_heatmap_with_no_colors():
    with pytest.raises(ValueError):
        make_chart_data(df=df, x='country', y='gdpPercap',
                        library=Libraries.PLOTLY,
                        chart_type=ChartTypes.heatmap)

    with pytest.raises(ValueError):
        make_chart_data(df=df, x='country', y='gdpPercap',
                        library=Libraries.HIGHCHARTS,
                        chart_type=ChartTypes.heatmap)
