
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

#Values used by property P172
# SELECT ?value ?valueLabel ?valueDescription ?valueAltLabel ?ct ?sampleitem ?sampleitemLabel
# WHERE
# {
#   {
#     SELECT ?value (count(*) as ?ct) (SAMPLE(?item) as ?sampleitem)
#     WHERE
#     {
#       ?item wdt:P172 ?value
#     }
#
#     GROUP BY ?value
#     ORDER BY DESC(?ct)
#   }
#   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
# }
# ORDER BY DESC(?ct) ASC(?value)
