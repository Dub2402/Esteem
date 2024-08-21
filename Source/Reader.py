import pandas

class Reader:
    @property
    def GetMD(self):
        return self.MD
    
    @property
    def GetMR(self):
        return self.MR
    
    @property
    def GetWD(self):
        return self.WD
    
    @property
    def GetWR(self):
        return self.WR
    
    def __init__(self, Settings) -> None:
        self.MD = self.__ReadExcel(Settings["men_dose"])
        self.MR = self.__ReadExcel(Settings["men_reminders"])
        self.WD = self.__ReadExcel(Settings["women_dose"])
        self.WR = self.__ReadExcel(Settings["women_reminders"])

    def __ReadExcel(self, path_file: str) -> list:
        exceldata = pandas.read_csv(path_file)
        Products = pandas.DataFrame(exceldata, columns=['Данные'])
        reading_data = Products["Данные"].tolist()

        return reading_data
    