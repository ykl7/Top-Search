import re
import math

class Rank:

	def __init__(self, files):
		self.file_list = files
		self.terms = self.file_processing()
		self.regdex = self.regIndex()
		self.tf = {}
		self.df = {}
		self.idf = {}
		self.totalIndex = self.execute()
		self.vectors = self.vectorize()
		self.mags = self.magnitudes(self.file_list)
		self.populateScores()

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

	def vectorize(self):
		vectors = {}
		for filename in self.file_list:
			vectors[filename] = [len(self.regdex[filename][word]) for word in self.regdex[filename].keys()]
		return vectors

	def document_frequency(self, term):
		if term in self.totalIndex.keys():
			return len(self.totalIndex[term].keys()) 
		else:
			return 0

	def collection_size(self):
		return len(self.file_list)

	# check score calculation again, lambda function might be wrong
	def magnitudes(self, documents):
		mags = {}
		for document in documents:
			mags[document] = pow(sum(map(lambda x: x**2, self.vectors[document])), .5)
		return mags

	def term_frequency(self, term, document):
		return self.tf[document][term]/self.mags[document] if term in self.tf[document].keys() else 0

	def populateScores(self):
		for filename in self.file_list:
			for term in self.getUniques():
				self.tf[filename][term] = self.term_frequency(term, filename)
				if term in self.df.keys():
					self.idf[term] = self.idf_func(self.collection_size(), self.df[term]) 
				else:
					self.idf[term] = 0
		return self.df, self.tf, self.idf

	def idf_func(self, N, N_t):
		if N_t != 0:
			return math.log(N/N_t)
		else:
		 	return 0

	def generateScore(self, term, document):
		return self.tf[document][term] * self.idf[term]

	def execute(self):
		return self.fullIndex()

	def regIndex(self):
		return self.make_indices(self.file_processing)

	def getUniques(self):
		return self.totalIndex.keys()
