import decimal
from typing import List, Union, Optional
from pydantic import BaseModel

Number = Union[int, float, decimal.Decimal]


class Point2D(BaseModel):
    x: Union[str, Number, None]
    y: Number


class NamedPoint2D(Point2D):
    name: Optional[str]
    color: Optional[str]


class Point3D(Point2D):
    z: Number


class NamedPoint3D(Point3D):
    name: Optional[str]
    color: Optional[str]


class Series(BaseModel):
    name: Optional[str]
    type: Optional[str]
    data: List


class BasicSeries(Series):
    data: List[Number]


class XYSeries(Series):
    data: List[
        List[
            Union[str, Number]
        ]
    ]


class Point2DSeries(Series):
    data: List[Point2D]


class Point3DSeries(Series):
    data: List[Point3D]


class NamedPoint2DSeries(Series):
    data: List[NamedPoint2D]


class NamedPoint3DSeries(Series):
    data: List[NamedPoint3D]


class PlotlySeries(BaseModel):
    name: Optional[str]
    type: Optional[str]
    text: List[Union[str, Number]]


class Plotly2DSeries(PlotlySeries):
    x: List[Union[str, Number]]
    y: List[Number]


class Plotly3DSeries(Plotly2DSeries):
    z: List[List[Number]]
    text: List[List[Number]]


class PlotlyPieSeries(PlotlySeries):
    labels: List[Union[str, Number]]
    values: List[Number]
