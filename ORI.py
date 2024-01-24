from PolestarCore import CurrentBar,Open,Close,High,Low,Vol,PlotNumeric,PlotIcon
from PolestarPy.toolsfunc import SMA,REF,AvgDeviation,SummationFC,CrossOver,CrossUnder
from PolestarPy.Series import NumericSeries

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

    # WCCI
    TYP = NumericSeries("WCCI")
    TYP[-1] = (h[-1] + l[-1] + c[-1]) / 3

    WCCI = None
    if TYP[-1] is not None:
        Avg = SMA(TYP, n1, Weight=2)
        AvgDev = AvgDeviation(TYP, n1)
        if Avg is not None and AvgDev is not None and AvgDev != 0:
            WCCI = (TYP[-1] - Avg) / (m / 1000 * AvgDev)

    # VR
    LC = REF(c, 1) if CurrentBar() >= 1 else None

    sUp = NumericSeries("VR")
    sUp[-1] = v[-1] if LC is not None and c[-1] > LC else 0

    sDown = NumericSeries("VR")
    sDown[-1] = v[-1] if LC is not None and c[-1] <= LC else 0

    Num = SummationFC(sUp, n2)
    Den = SummationFC(sDown, n2)

    VR = Num / Den * 100 if Den != 0 and Den is not None else None

    # 绘制信号图标
    if WCCI[-1] is not None:
        # 当WCCI下穿+100
        if CrossUnder(WCCI[-1], 100):
            PlotIcon(True, h[-1], 1)

        # 当WCCI上穿-100
        if CrossOver(WCCI[-1], -100):
            PlotIcon(True, l[-1], 2)

            # 当WCCI上穿-100且VR的值小于或等于100
            if VR[-1] is not None and VR[-1] <= 100:
                PlotIcon(True, l[-1], 3)
