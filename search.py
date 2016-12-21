import rank
import re

class Search:

	def __init__(self, list_of_files):
		self.filenames = list_of_files
		self.index = rank.rank(self.filenames)
		self.invertedIndex = self.index.totalIndex
		self.regularIndex = self.index.regdex

