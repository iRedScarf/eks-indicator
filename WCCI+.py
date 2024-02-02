from PolestarCore import Close, High, Low, PlotDot, ColorUp
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

    TYP = NumericSeries("TYP")
    TYP[-1] = (h[-1] + l[-1] + c[-1]) / 3

    WCCI = NumericSeries("WCCI")
    if TYP[-1] is not None:
        Avg = SMA(TYP, n, Weight=2)
        AvgDev = AvgDeviation(TYP, n)
        if Avg is not None and AvgDev is not None and AvgDev != 0:
            WCCI[-1] = (TYP[-1] - Avg) * 10000 / (m * AvgDev)
        else:
            WCCI[-1] = None
    else:
        WCCI[-1] = None

    signalPoint = None
    if len(WCCI) > 1 and WCCI[-2] is not None and WCCI[-1] is not None:
        previous_WCCI = WCCI[-2]
        current_WCCI = WCCI[-1]

        if previous_WCCI >= 100 and current_WCCI < 100:
            signalPoint = h[-1] + 1
        elif previous_WCCI <= -100 and current_WCCI > -100:
            signalPoint = l[-1] - 1

    if signalPoint is not None:
        PlotDot("WCCI", signalPoint, 2, ColorUp())

    return WCCI, signalPoint
