from math import sqrt,pow
from PolestarCore import *
from Series import NumericSeries
"""
   求和
"""
def Summation(price,length):
    length = int(length)
    SumValue = 0
    for i in range(length==0 if 0 else max(0,len(price)-length), len(price)):
       if price[i] != None:
           SumValue+=price[i]
    return SumValue

"""
   求指数平均
"""

def XAverage(data, length):
    length = int(length)
    XAvgValue = NumericSeries("XAverage")
    sFcactor = 2 / ( length + 1 )
    if len(data) ==1:
        XAvgValue[-1] = data[0]
    else:
         XAvgValue[-1] = XAvgValue[-2] + sFcactor * (data[-1] - XAvgValue[-2])
    return XAvgValue()

"""
   求移动平均
"""
def Ma(data, length):
    length = int(length)
    if length==0:
        return None
    if len(data)<length:
        return Summation(data, len(data)) / len(data)
    ret = Summation(data, length) / length
    return ret
"""
 求指数平均
"""
def EMA(data, length):
    return XAverage(data,length)
"""
 求移动平均
"""
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
"""
 求最低
"""
def Lowest(Price, Length=5):
    Length = int(Length)
    LowestValue = Price[0];
    for i in range(max(0,len(Price)-Length),len(Price)):
       if(Price[i] < LowestValue):
            LowestValue = Price[i]
    return LowestValue;
"""
 求最高
"""
def Highest(Price, Length=5):
    Length = int(Length)
    HighestValue = Price[0];
    for i in range(max(0,len(Price)-Length),len(Price)):
       if(Price[i] > HighestValue):
            HighestValue = Price[i]
    return HighestValue;
"""
 求极值
"""
def Extremes(Price,Length,bMax,ExtremeBar):
    Length = int(Length)
    MyVal = NumericSeries("Extremes")
    MyBar = NumericSeries("Extremes")
    tmpMinMax = Price[-1]
    tmpBar = 0
    if CurrentBar() <= Length - 1 or MyBar[-2] == Length - 1:
        for i in range(max(0,len(Price)-Length),len(Price)):
            if bMax:
                if Price[i] > tmpMinMax:
                   tmpMinMax = Price[i]
                   tmpBar = len(Price) - 1-i
            else:
                if Price[i] < tmpMinMax:
                    tmpMinMax = Price[i]
                    tmpBar = len(Price) - 1-i
        MyVal[-1] = tmpMinMax
        MyBar[-1] = tmpBar
    else:
        if bMax:
            if Price[-1] >= MyVal[-2]:
                MyVal[-1] = Price[-1]
                MyBar[-1] = 0
            else:
                MyVal[-1] = MyVal[-2]
                MyBar[-1] = MyBar[-2]+1
        else:
            if Price[-1] <= MyVal[-2]:
                MyVal[-1] = Price[-1]
                MyBar[-1] = 0
            else:
                MyVal[-1] = MyVal[-2]
                MyBar[-1] = MyBar[-2]+1
    ExtremeBar =  MyBar()
    return MyVal()
"""
 快速计算最低
"""
def LowestFC(Price,Length=10):
    ExtremesBar = 0
    return Extremes(Price, Length, False, ExtremesBar)
"""
 快速计算最高
"""
def HighestFC(Price,Length=10):
    ExtremesBar = 0
    return Extremes(Price, Length, True, ExtremesBar)
"""
快速求和
"""
def SummationFC(Price,Length):
    Length = int(Length)
    SumValue = NumericSeries("SummationFC")
    if Length == 0:
        if len(SumValue) ==0:
            SumValue[-1] = Price[-1]
        else:
            SumValue[-1] = SumValue[-2]+Price[-1]
    else:
        if len(SumValue) < Length:
           sum = 0
           for i in range(max(0,len(Price)-Length),len(Price)):
              sum+=Price[i]
           SumValue[-1] = sum
        else:
           SumValue[-1] = SumValue[-2]+Price[-1]-Price[-1-Length]
    return SumValue();
"""
 快速计算平均值
"""
def AverageFC(Price,Length):
    Length = int(Length)
    if Length==0:
        return None
    if len(Price)<Length:
        return SummationFC(Price, Length) / len(Price)
    else:
        return SummationFC(Price, Length) / Length
"""
 数据回溯
"""
def REF(Price,N):
    N = int(N)
    if N >= len(Price):
        return Price[-1]
    else:
        return Price[-N-1]
"""
求估计方差
"""
def VariancePS(Price,Length):
    Divisor = Length-1;
    if Divisor > 0:
       Mean = Ma(Price, Length)
       if Mean is None or len(Price) < Length :
           return 0
       else:
           SumSqr = 0
           for i in range(max(0,len(Price)-Length), len(Price)):
              SumSqr += pow((Price[i] - Mean),2)
           return SumSqr / Divisor 
    else:
        return 0
"""
求标准差
"""
def STD(Price,Length):
    Length = int(Length)
    VarPSValue = VariancePS(Price, Length)
    if VarPSValue >0:
        return sqrt(VarPSValue)
    else:
        return None
"""
求抛物线转向
"""
def ParabolicSAR(AfStep,AfLimit):
    oParClose = None
    oParOpen = None
    oPosition = None
    oTransition = None

    Af = NumericSeries("ParabolicSAR")
    ParOpen = NumericSeries("ParabolicSAR")
    Position = NumericSeries("ParabolicSAR")
    HHValue = NumericSeries("ParabolicSAR")
    LLValue = NumericSeries("ParabolicSAR")
    if CurrentBar()==0:
        Position[-1] = 1
        oTransition = 1
        Af[-1] = AfStep
        HHValue[-1] = High()[-1]
        LLValue[-1] = Low()[-1]
        oParClose = LLValue[-1]
        ParOpen[-1] = oParClose + Af[-1] * (HHValue[-1] - oParClose)
        if ParOpen[-1] > LLValue[-1]:
            ParOpen[-1] = LLValue[-1]
    else:
        oTransition = 0
        HHValue[-1] = HHValue[-2] if HHValue[-2] > High()[-1] else High()[-1]
        LLValue[-1] = LLValue[-2] if LLValue[-2] < Low()[-1] else Low()[-1]
        if Position[-2] == 1:
            if Low()[-1] <= ParOpen[-2]:
                Position[-1] = -1
                oTransition = -1
                oParClose = HHValue[-1]
                HHValue[-1] = High()[-1]
                LLValue[-1]  = Low()[-1]
                Af[-1] = AfStep
                ParOpen[-1] = oParClose + Af[-1] * (LLValue[-1] - oParClose)

                if ParOpen[-1] < High()[-1]:
                   ParOpen[-1] = High()[-1]

                if ParOpen[-1] < High()[-2]:
                   ParOpen[-1] = High()[-2]
            else:
                Position[-1] = Position[-2]
                oParClose = ParOpen[-2]
                if HHValue[-1] > HHValue[-2] and Af[-2] < AfLimit:
                    if Af[-2] + AfStep > AfLimit:
                       Af[-1] = AfLimit
                    else:
                       Af[-1] = Af[-2] + AfStep
                else:
                    Af[-1] = Af[-2]
                ParOpen[-1] = oParClose + Af[-1] * (HHValue[-1] - oParClose)
                if ParOpen[-1] > Low()[-1]:
                    ParOpen[-1] = Low()[-1]
                if ParOpen[-1] > Low()[-2]:
                    ParOpen[-1] = Low()[-2]
        else:
            if High()[-1] >= ParOpen[-2]:
               Position[-1] = 1
               oTransition = 1

               oParClose = LLValue[-1]
               HHValue[-1] = High()[-1]
               LLValue[-1] = Low()[-1]

               Af[-1] = AfStep
               ParOpen[-1] = oParClose + Af[-1] * ( HHValue[-1] - oParClose)
               if ParOpen[-1] > Low()[-1]:
                  ParOpen[-1] = Low()[-1]

               if ParOpen[-1] > Low()[-2]:
                  ParOpen[-1] = Low()[-2]
            else:
                Position[-1] = Position[-2]
                oParClose = ParOpen[-2]
                if LLValue[-1] < LLValue[-2] and Af[-2] < AfLimit:
                   if Af[-2] + AfStep > AfLimit:
                      Af[-1] = AfLimit
                   else:
                      Af[-1] = Af[-2] + AfStep
                else:
                    Af[-1] = Af[-2]
                ParOpen[-1] = oParClose + Af[-1] * ( LLValue[-1] - oParClose )
                if ParOpen[-1] < High()[-1]:
                   ParOpen[-1] = High()[-1]

                if ParOpen[-1] < High()[-2]:
                   ParOpen[-1] = High()[-2]
    oParOpen = ParOpen[-1]
    oPosition = Position[-1]
    return oParClose,oParOpen,oPosition,oTransition
"""
求平均背离
"""
def AvgDeviation(data, length):
    Mean = Ma(data, length)
    if Mean==None:
        return None
    SumValue = 0
    length = int(length)
    for i in range(max(0,len(data)-length), len(data)):
           SumValue +=abs(data[i] - Mean)
    return SumValue / length 
"""
 获取最近N周期条件满足的计数
"""
def CountIf(cond, period):
    sum = 0
    period = int(period)
    if len(cond)<period or period==0:
       return None
    for i in range(len(cond)-period, len(cond)):
       if cond[i]: 
           sum += 1          
    return sum
"""
   求是否上穿
"""
def CrossOver(price1, price2):
    '''price1是否上穿price2,前一个在下，当前跟在上'''
    # 只有一根线，不做比较
    if len(price1) <= 1 or len(price2) <= 1:
        return False
    
    if price1[-1]==None or price2[-1]==None:
        return False

    if price1[-1] <= price2[-1]:
        return False

    # 如果前一根相等，则继续往前找上一根
    pos = -2 
    while price1[pos] == price2[pos]:
        pos = pos - 1
        if pos < -len(price1) or pos < -len(price2):
            break
    if price1[pos]==None or price2[pos]==None:
        return False
    return price1[pos] < price2[pos]
"""
   求是否下穿
"""
def CrossUnder(price1, price2):
    '''price1是否下破price2,前一个在上，当前跟在下'''
    # 只有一根线，不做比较
    if len(price1) <= 1 or len(price2) <= 1:
        return False

    if price1[-1]==None or price2[-1]==None:
        return False

    if price1[-1] >= price2[-1]:
        return False

    # 如果前一根相等，则继续往前找上一根
    pos = -2;
    while price1[pos] == price2[pos]:
        pos = pos - 1
        if pos < -len(price1) or pos < -len(price2):
            break
    if price1[pos]==None or price2[pos]==None:
        return False
    return price1[pos] > price2[pos]
if __name__ == "__main__": 
    data = [100,101,102,103,104,105,106]
    print(Lowest(data,6))