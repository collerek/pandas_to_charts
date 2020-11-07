from enum import Enum, auto
from typing import List

import pandas as pd

from pandas_to_charts.data_configs.basic_types import (
    Plotly2DSeries,
    Plotly3DSeries,
    PlotlyPieSeries,
    NamedPoint2DSeries,
    NamedPoint2D,
    NamedPoint3DSeries,
    NamedPoint3D,
)
from pandas_to_charts.exceptions import ChartTypeNotImplemented, LibraryNotImplemented


class Libraries(Enum):
    PLOTLY = auto()
    HIGHCHARTS = auto()
    CHARTSJS = auto()


class ChartTypes(Enum):
    bar = auto()
    column = auto()
    line = auto()
    scatter = auto()
    area = auto()
    pie = auto()
    doughnut = auto()
    heatmap = auto()


def get_chart_constructor(chart_type: ChartTypes, library: Libraries, data_type=None):
    if library == Libraries.PLOTLY:
        if chart_type == ChartTypes.heatmap:
            return get_plotly_3d_constructor
        elif chart_type in [ChartTypes.pie, ChartTypes.doughnut]:
            return get_plotly_pie_constructor
        elif chart_type in (k for k in ChartTypes):
            return get_plotly_2d_constructor
        raise ChartTypeNotImplemented(
            f"{chart_type} is not implemented for library {Libraries.PLOTLY}"
        )
    elif library == Libraries.HIGHCHARTS:
        if chart_type == ChartTypes.heatmap:
            return get_highcharts_3d_constructor
        elif chart_type in (k for k in ChartTypes):
            return get_highcharts_2d_constructor
        raise ChartTypeNotImplemented(
            f"{chart_type} is not implemented for library {Libraries.HIGHCHARTS}"
        )

    raise LibraryNotImplemented(f"Library {library} is not supported")


def get_plotly_2d_constructor(df: pd.DataFrame, x: str, y: str) -> Plotly2DSeries:
    y_vals = df[y].values.tolist()
    return Plotly2DSeries(x=df[x].values.tolist(), y=y_vals, text=y_vals)


def get_plotly_pie_constructor(df: pd.DataFrame, x: str, y: str) -> PlotlyPieSeries:
    y_vals = df[y].values.tolist()
    return PlotlyPieSeries(labels=df[x].values.tolist(), values=y_vals, text=y_vals)


def get_plotly_3d_constructor(
    df: pd.DataFrame, raw_df: pd.DataFrame, x: str, z: List[str]
) -> Plotly3DSeries:
    if not z or not z[0]:
        raise ValueError("The colors variable is not set - not enough arguments")

    y_vals = df.drop(x, axis=1).T.values.tolist()  # type: ignore
    return Plotly3DSeries(
        x=df[x].values.tolist(),
        y=raw_df[z[0]].dropna().unique().tolist(),
        z=y_vals,
        text=y_vals,
    )


def get_highcharts_2d_constructor(
    df: pd.DataFrame, x: str, y: str
) -> NamedPoint2DSeries:
    return NamedPoint2DSeries(
        data=[
            NamedPoint2D(name=x_, y=y_)
            for x_, y_ in zip(df[x].values.tolist(), df[y].values.tolist())
        ]
    )


def get_highcharts_3d_constructor(
    df: pd.DataFrame, raw_df: pd.DataFrame, x: str, z: List[str]
) -> NamedPoint3DSeries:
    if not z or not z[0]:
        raise ValueError("The colors variable is not set - not enough arguments")

    x_axis_vals = df[x].astype("category")
    by_ser_vals = raw_df[z[0]].dropna().astype("category")

    x_val = x_axis_vals.cat.codes.tolist()
    y_val = by_ser_vals.cat.codes.unique().tolist()
    z = df.drop(x, axis=1).T.values.tolist()  # type: ignore

    return NamedPoint3DSeries(
        data=[
            NamedPoint3D(x=x_[0][0], y=x_[0][1], z=x_[1])
            for x_ in zip(
                [(i, j) for j in y_val for i in x_val],
                [val for sublist in z for val in sublist],
            )
        ]
    )
