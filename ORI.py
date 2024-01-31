from PolestarCore import Open,Close,High,Low,Vol,PlotNumeric,PlotDot,ColorUp
from PolestarPy.toolsfunc import SMA,AvgDeviation
from PolestarPy.Series import NumericSeries

def handle_WCCI(param):

    n = param[0]
    m = param[4]

    c = Close()
    h = High()
    l = Low()

    # WCCI
    TYP = NumericSeries("WCCI")
    TYP[-1] = (h[-1] + l[-1] + c[-1]) / 3

    WCCI = None
    if TYP[-1] is not None:
        Avg = SMA(TYP, n, Weight=2)
        AvgDev = AvgDeviation(TYP, n)
        if Avg is not None and AvgDev is not None and AvgDev != 0:
            WCCI = (TYP[-1] - Avg) * 10000 / (m * AvgDev)

    signalPoint = None
    if WCCI is not None and len(WCCI) > 1:
        previous_WCCI = WCCI[-2]
        current_WCCI = WCCI[-1]

        if previous_WCCI >= 100 and current_WCCI < 100:
            signalPoint = High[-1]
        elif previous_WCCI <= -100 and current_WCCI > -100:
            signalPoint = Low[-1]

    return WCCI, signalPoint

def handle_data(param):

    n1 = param[0]
    n2 = param[1]
    n3 = param[2]
    n4 = param[3]
    m = param[4]

    o = Open()
    c = Close()
    h = High()
    l = Low()
    v = Vol()

    # WBBI
    sma1 = SMA(c,n1,Weight=1)
    sma2 = SMA(c,n2,Weight=2)
    sma3 = SMA(c,n3,Weight=3)
    sma4 = SMA(c,n4,Weight=4)
    WBBI = (sma1 + sma2 + sma3 + sma4) / 4
    PlotNumeric("WBBI",WBBI)

    signalPoint = handle_WCCI(param)
    if signalPoint is not None:
        PlotDot("WCCI",signalPoint,2,ColorUp())
        
