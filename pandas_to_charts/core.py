from inspect import signature
from typing import List, Union, NamedTuple, Dict

import pandas as pd
from pandas.core.groupby import DataFrameGroupBy

from pandas_to_charts.data_configs.constructors import ChartTypes, get_chart_constructor, Libraries
from pandas_to_charts.exceptions import NoDataToDisplay


def one_group(x):
    return ""


class DataSerie(NamedTuple):
    grouped_data: DataFrameGroupBy
    group_names: List


def make_chart_data(
        df: pd.DataFrame,
        x: str,
        y: Union[str, List[str]],
        chart_type: ChartTypes,
        library: Libraries,
        colors: Union[str, List[str]] = None,
):
    if not isinstance(colors, list):
        colors = [colors]

    if not isinstance(y, list):
        y = [y]

    names = []
    traces = []

    grouper = [x or one_group for x in colors] or [one_group]
    if df is None or df.empty:
        raise NoDataToDisplay('No data for given filters')
    grouped = df.groupby(grouper, sort=False)
    group_names = []
    for group_name in grouped.groups:
        if len(grouper) == 1:
            group_name = (group_name,)
        group_names.append(group_name)

    data_series = DataSerie(grouped_data=grouped, group_names=group_names)

    for group_name in group_names:
        if len(grouper) == 1 and grouper[0] == one_group:
            for serie_name in y:
                names.append(serie_name)
        else:
            names.append(', '.join(['{}'.format(b) for a, b in zip(grouper, group_name)]))

    if chart_type == ChartTypes.heatmap:
        index_df = pd.DataFrame(df[x].dropna().unique(), columns=[x])
        for i, group_name in enumerate(data_series.group_names):
            group = data_series.grouped_data.get_group(group_name if len(group_name) > 1 else group_name[0])
            index_df = pd.merge(index_df, group[[x, y[0]]], how='left')
            index_df.columns = [x] + [y[0] + '_' + str(z) for z in range(i + 1)]

        index_df.fillna(0, inplace=True)
        trace = generate_trace(index_df, df, x, chart_type, library, colors=colors)
        trace.type = ChartTypes._value2member_map_[chart_type.value].name
        traces.append(trace.dict())

    else:
        for i, group_name in enumerate(data_series.group_names):
            for serie in y:
                final_group = fill_missing_values(df, data_series, group_name, x)
                trace = generate_trace(final_group, df, x, chart_type, library, serie=serie)
                trace.name = group_name[0]
                trace.type = ChartTypes._value2member_map_[chart_type.value].name
                traces.append(trace.dict())

    return traces


def generate_trace(data: pd.DataFrame,
                   raw_data: pd.DataFrame,
                   x: str,
                   chart_type: ChartTypes,
                   library: Libraries,
                   serie=None,
                   colors=None):
    constructor = get_chart_constructor(chart_type=chart_type, library=library)
    if 'raw_df' in signature(constructor).parameters:
        result = constructor(df=data, raw_df=raw_data, x=x, z=colors)
    else:
        result = constructor(df=data, x=x, y=serie)
    return result


def fill_missing_values(df: pd.DataFrame, data_series: DataSerie, group_name: list, x: str) -> pd.DataFrame:
    group = data_series.grouped_data.get_group(
        group_name if len(group_name) > 1 else group_name[0])
    if group_name[0] != '':
        # need to deal with missing axis labels which are added at the end if happens in first serie
        axis_df = pd.DataFrame(df[x].dropna().unique(), columns=[x])
        final_group = axis_df.merge(group, how='left', on=x)

        for column in final_group.columns:
            if final_group[column].dtype == 'object':
                final_group[column] = final_group[column].ffill()
            else:
                final_group[column] = final_group[column].fillna(0)
    else:
        final_group = group

    final_group.fillna(0, inplace=True)
    return final_group
