from PolestarCore import LoadSeries,SetSeriesData,GetSeriesData

class NumericSeries(object):
    def __init__(self, name):
      self.Series = LoadSeries(name)

    def __setitem__(self,name, value):
      SetSeriesData(self.Series,value)

    def __getitem__(self,name):
      return GetSeriesData(self.Series,name)

    def __call__(self):
      return GetSeriesData(self.Series,-1)

    def __len__(self):
        return len(self.Series)
