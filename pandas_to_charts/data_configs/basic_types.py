from typing import List, Union, Optional
from numbers import Number

from pydantic import BaseModel


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
    data: List


class BasicSeries(Series):
    data: List[Number]


class XYSeries(Series):
    data: List[
        List[
            Union[str, Number],
            Number
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


class Plotly2DSeries(BaseModel):
    x: List[Union[str, Number]]
    y: List[Number]
    text: List[Union[str, Number]]


class PlotlyPieSeries(BaseModel):
    labels: List[Union[str, Number]]
    values: List[Number]
    text: List[Union[str, Number]]


class Plotly3DSeries(BaseModel):
    x: List[Union[str, Number]]
    y: List[Union[str, Number]]
    z: List[Number]
    text: List[Union[str, Number]]
