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
    TYP[-2] = (h[-2] + l[-2] + c[-2]) / 3

    if TYP[-1] is not None and TYP[-2] is not None:
        Avg = SMA(TYP, n, Weight=2)
        AvgDev = AvgDeviation(TYP, n)
        if Avg is not None and AvgDev is not None and AvgDev != 0:
            WCCI_1 = (TYP[-1] - Avg) * 10000 / (m * AvgDev)
            WCCI_2 = (TYP[-2] - Avg) * 10000 / (m * AvgDev)
        else:
            WCCI_1 = None
            WCCI_2 = None
    else:
        WCCI_1 = None
        WCCI_2 = None

    if WCCI_1 is not None and WCCI_2 is not None:
        if WCCI_2 >=100 and WCCI_1 < 100:
            PlotDot("WCCI", h[-1], 2, ColorDown())
        if WCCI_2 <= -100 and WCCI_1 > -100:
            PlotDot("WCCI", l[-1], 2, ColorUp())
