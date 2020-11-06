class PandasToChartsException(Exception):
    pass


class NoDataToDisplay(PandasToChartsException):
    pass


class ChartTypeNotImplemented(PandasToChartsException):
    pass


class LibraryNotImplemented(PandasToChartsException):
    pass
