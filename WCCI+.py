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
    TYP[-1] = (h[-1] + l[-1] + c[-1]) / 3

    PrevWCCI = None
    if CurrentBar() > 0:
        try:
            Avg = SMA(TYP, n, Weight=2)
            AvgDev = AvgDeviation(TYP, n)
            if Avg is not None and AvgDev is not None and AvgDev > 0:
                PrevWCCI = (TYP[-2] - Avg) * 10000 / (m * AvgDev)
        except TypeError:
            PrevWCCI = None

    WCCI = None
    WCCI_Val = None
    if TYP[-1] is not None:
        Avg = SMA(TYP, n, Weight=2)
        AvgDev = AvgDeviation(TYP, n)
        if Avg is not None and AvgDev is not None and AvgDev > 0:
            try:
                WCCI = (TYP[-1] - (Avg) * 10000 / (m * AvgDev)
            except TypeError:
                WCCI = None

            if PrevWCCI is not None:
                if PrevWCCI > 100 and WCCI <= 100:
                    WCCI_Val = h[-1]
                elif PrevWCCI < -100 and WCCI >= -100:
                    WCCI_Val = l[-1]

    return WCCI_Val

def SMA(Price, Length,Weight=1):
    Length = int(Length)
    if Length==0:
        return None
    SMAValue = NumericSeries("SMA")
    if len(Price) == 1:
        SMAValue[-1] = Price[0]
    else: 
        SMAValue[-1] = (SMAValue[-2]*(Length-Weight)+Price[-1]*Weight)/Length
    return SMAValue()

def AvgDeviation(data, length):
    Mean = Ma(data, length)
    if Mean==None:
        return None
    SumValue = 0
    length = int(length)
    for i in range(max(0,len(data)-length), len(data)):
           SumValue +=abs(data[i] - Mean)
    return SumValue / length 
