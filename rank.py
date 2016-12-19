import re

class Rank:

	def __init__(self, files):
		self.file_list = files
		self.terms = self.file_processing()
		self.regdex = self.regIndex()
		self.tf = {}
		self.df = {}


	def file_processing(self):
		terms = {}
		for file in self.file_list:
			pattern = re.compile('[\W_]+')
			terms[file] = open(file, 'r').read().lower();
			terms[file] = pattern.sub(' ', terms[file])
			re.sub(r'[\W_]+','', terms[file])
			terms[file] = terms[file].split()
		return terms

	def index_one_file(self, list_of_terms):
		fileIndex = {}
		for index, word in enumerate(list_of_terms):
			if word in fileIndex.keys():
				fileIndex[word].append(index)
			else:
				fileIndex[word] = [index]
		return fileIndex

	def make_indices(self, lists_of_terms):
		total = {}
		for filename in lists_of_terms.keys():
			total[filename] = self.index_one_file(lists_of_terms[filename])
		return total

	def fullIndex(self):
		total_index = {}
		indie_indices = self.regdex
		for filename in indie_indices.keys():
			self.tf[filename] = {}
			for word in indie_indices[filename].keys():
				self.tf[filename][word] = len(indie_indices[filename][word])
				if word in self.df.keys():
					self.df[word] += 1
				else:
					self.df[word] = 1 
				if word in total_index.keys():
					if filename in total_index[word].keys():
						total_index[word][filename].append(indie_indices[filename][word][:])
					else:
						total_index[word][filename] = indie_indices[filename][word]
				else:
					total_index[word] = {filename: indie_indices[filename][word]}
		return total_index


