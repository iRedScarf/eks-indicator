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
