from PolestarCore import CurrentBar,Close,Vol,PlotNumeric
from PolestarPy.toolsfunc import REF,SummationFC
from PolestarPy.Series import NumericSeries

def handle_data(param):

    n = param[0]
    c = Close()
    v = Vol()

    LC = REF(c, 1) if CurrentBar() >= 1 else None

    sUp = NumericSeries("VR")
    sUp[-1] = v[-1] if LC is not None and c[-1] > LC else 0

    sDown = NumericSeries("VR")
    sDown[-1] = v[-1] if LC is not None and c[-1] <= LC else 0

    Num = SummationFC(sUp, n)
    Den = SummationFC(sDown, n)

    VR = Num / Den * 100 if Den != 0 and Den is not None else None

    PlotNumeric("VR", VR)
    PlotNumeric("A", 100)
    PlotNumeric("B", 200)
