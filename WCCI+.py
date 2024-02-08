from PolestarCore import CurrentBar, Close, High, Low, PlotDot, ColorUp
from PolestarPy.toolsfunc import SMA, AvgDeviation
from PolestarPy.Series import NumericSeries

def handle_WCCI(param):
    n = param[0]
    m = param[1]

    c = Close()
    h = High()
    l = Low()

    TYP = NumericSeries("WCCI")
    TYP[-1] = (float(h[-1]) + float(l[-1]) + float(c[-1])) / 3

    PrevWCCI = None
    if CurrentBar() > 0:
        try:
            # 确保所有操作数都转换为float
            Avg = SMA(TYP, n, Weight=2)
            AvgDev = AvgDeviation(TYP, n)
            if Avg is not None and AvgDev is not None and AvgDev > 0:
                PrevWCCI = (float(TYP[-2]) - float(Avg)) * 10000 / (float(m) * float(AvgDev))
        except TypeError:
            PrevWCCI = None

    WCCI = None
    WCCI_Val = None
    if TYP[-1] is not None:
        Avg = SMA(TYP, n, Weight=2)
        AvgDev = AvgDeviation(TYP, n)
        if Avg is not None and AvgDev is not None and AvgDev > 0:
            try:
                WCCI = (float(TYP[-1]) - float(Avg)) * 10000 / (float(m) * float(AvgDev))
            except TypeError:
                WCCI = None

            if PrevWCCI is not None:
                if PrevWCCI > 100 and WCCI <= 100:
                    WCCI_Val = h[-1]
                elif PrevWCCI < -100 and WCCI >= -100:
                    WCCI_Val = l[-1]

    return WCCI_Val

def handle_data(param):
    WCCI_Val = handle_WCCI(param)
    if WCCI_Val is not None:
        PlotDot("WCCI", WCCI_Val, 2, ColorUp())
        
