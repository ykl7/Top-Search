class Rank:

	def __init__(self, files):
		self.file_list = files
		self.terms = self.file_processing()


	def file_processing(self):
		terms = {}
		for file in self.file_list:
			pattern = re.compile('[\W_]+')
			terms[file] = open(file, 'r').read().lower();
			terms[file] = pattern.sub(' ', terms[file])
			re.sub(r'[\W_]+','', terms[file])
			terms[file] = terms[file].split()
		return terms