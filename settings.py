class SettingsForFindOccupation:
	def __init__(self):
		self.firstline = True
		self.minCount = 5
		self.popularCount = [997,100]
class SettingsForQS:
	def __init__(self):
		self.firstline = True
		self.wikipediaOptions = [["en","Q328"],["es","Q8449"],["de","Q48183"],["fr","Q8447"],["pt","Q11921"]]
		self.popularCountSteps = [997,100]
		self.accuracy = 90
		self.minCount = 0
