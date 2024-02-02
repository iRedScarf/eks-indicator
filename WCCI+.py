from PolestarCore import Close, High, Low, PlotDot, ColorUp, ColorDown
from PolestarPy.toolsfunc import SMA, AvgDeviation
from PolestarPy.Series import NumericSeries

def handle_data(param):

    if len(param) < 2:
        return None, None

    n = param[0]
    m = param[1]

    c = Close()
    h = High()
    l = Low()

    TYP = NumericSeries("WCCI")
    TYP[-1] = (h[-1] + l[-1] + c[-1]) / 3

    if TYP[-1] is not None:
        Avg = SMA(TYP, n, Weight=2)
        AvgDev = AvgDeviation(TYP, n)
        if Avg is not None and AvgDev is not None and AvgDev != 0:
            WCCI = (TYP[-1] - Avg) * 10000 / (m * AvgDev)
        else:
            WCCI = None
    else:
        WCCI = None
