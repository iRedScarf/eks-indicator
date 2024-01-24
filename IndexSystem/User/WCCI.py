from PolestarCore import Close,High,Low,PlotNumeric
from PolestarPy.toolsfunc import SMA,AvgDeviation
from PolestarPy.Series import NumericSeries

def handle_data(param):

    n = param[0]
    m = param[1]

    c = Close()
    h = High()
    l = Low()

    TYP = NumericSeries("WCCI")
    TYP[-1] = (h[-1] + l[-1] + c[-1]) / 3

    WCCI = None
    if TYP[-1] is not None:
        Avg = SMA(TYP, n, Weight=2)
        AvgDev = AvgDeviation(TYP, n)
        if Avg is not None and AvgDev is not None and AvgDev != 0:
            WCCI = (TYP[-1] - Avg) / (m / 1000 * AvgDev)

    PlotNumeric("WCCI", WCCI)
    PlotNumeric("A1", 100)
    PlotNumeric("A2", 200)
    PlotNumeric("B1", -100)
    PlotNumeric("B2", -200)
    PlotNumeric("Z", 0)
    