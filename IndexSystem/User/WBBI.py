from PolestarCore import Close,PlotNumeric
from PolestarPy.toolsfunc import SMA
from PolestarPy.Series import NumericSeries

def handle_data(param):

    n1 = param[0]
    n2 = param[1]
    n3 = param[2]
    n4 = param[3]

    c = Close()

    sma1 = SMA(c,n1,Weight=1)
    sma2 = SMA(c,n2,Weight=2)
    sma3 = SMA(c,n3,Weight=3)
    sma4 = SMA(c,n4,Weight=4)
    WBBI = (sma1 + sma2 + sma3 + sma4) / 4
    PlotNumeric("WBBI",WBBI)
