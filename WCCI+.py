from PolestarCore import Close, High, Low, PlotDot, ColorUp, PlotNumeric
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

    if TYP[-1] == None:
        WCCI = None

    else:
        Avg = SMA(TYP, n, Weight=2)
        AvgDev = AvgDeviation(TYP, n)
        if Avg == None or AvgDev == None or AvgDev == 0:
            WCCI = None
        else:
            WCCI = (TYP[-1] - Avg) * 10000 / (m * AvgDev)
            
    PlotNumeric("WCCI", WCCI)
