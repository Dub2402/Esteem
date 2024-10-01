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
		self.MD = self.__ReadExcel(Settings["mens"], column = "Доза")
		self.MR = self.__ReadExcel(Settings["mens"], column = "Послания")
		self.WD = self.__ReadExcel(Settings["womens"], column = "Доза")
		self.WR = self.__ReadExcel(Settings["womens"], column = "Послания")

	def __ReadExcel(self, path_file: str, column: str) -> list:
		
		exceldata = pandas.read_excel(path_file)
		Products = pandas.DataFrame(exceldata, columns=[column])
		reading_data = Products[column].tolist()
	
		return reading_data
	