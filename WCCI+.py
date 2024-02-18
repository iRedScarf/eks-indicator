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


def WCCI(close_prices, high_prices, low_prices, n, m):
    # 确保输入数据有效
    if len(close_prices) == 0 or len(high_prices) == 0 or len(low_prices) == 0:
        return None

    # 计算TYP价格
    typ_prices = [(h + l + c) / 3 for h, l, c in zip(high_prices, low_prices, close_prices)]

    # 计算WCCI
    wcci_val = None

    if len(typ_prices) > 1:
        # 计算前一周期的WCCI值
        avg_prev = SMA(typ_prices[:-1], n)
        avg_dev_prev = AvgDeviation(typ_prices[:-1], n)
        if avg_prev is not None and avg_dev_prev is not None and avg_dev_prev > 0:
            prev_wcci = (typ_prices[-2] - avg_prev) * 10000 / (m * avg_dev_prev)
        else:
            prev_wcci = None

        # 计算当前周期的WCCI值
        avg = SMA(typ_prices, n)
        avg_dev = AvgDeviation(typ_prices, n)
        if avg is not None and avg_dev is not None and avg_dev > 0:
            wcci = (typ_prices[-1] - avg) * 10000 / (m * avg_dev)
            # 根据前一周期和当前周期的WCCI值，确定返回值
            if prev_wcci is not None:
                if prev_wcci > 100 and wcci <= 100:
                    wcci_val = high_prices[-1]  # 当前周期的最高价
                elif prev_wcci < -100 and wcci >= -100:
                    wcci_val = low_prices[-1]  # 当前周期的最低价

    return wcci_val

