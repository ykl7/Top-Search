import rank
import re

class Search:

	def __init__(self, list_of_files):
		self.filenames = list_of_files
		self.index = rank.rank(self.filenames)
		self.invertedIndex = self.index.totalIndex
		self.regularIndex = self.index.regdex

	def make_vectors(self, documents):
		vectors = {}
		for doc in documents:
			docVector = [0]*len(self.index.getUniques())
			for ind, term in enumerate(self.index.getUniques()):
				docVector[ind] = self.index.generateScore(term, doc)
			vectors[doc] = docVector
		return vectors

	def queryFreq(self, term, query):
		count = 0
		for word in query.split():
			if word == term:
				count += 1
		return count

	def termfreq(self, terms, query):
		temp = [0]*len(terms)
		for i,term in enumerate(terms):
			temp[i] = self.queryFreq(term, query)
		return temp

	def dotProduct(self, doc1, doc2):
		if len(doc1) != len(doc2):
			return 0
		return sum([x*y for x,y in zip(doc1, doc2)])

	def query_vec(self, query):
		pattern = re.compile('[\W_]+')
		query = pattern.sub(' ',query)
		queryls = query.split()
		queryVec = [0]*len(queryls)
		index = 0
		for ind, word in enumerate(queryls):
			queryVec[index] = self.queryFreq(word, query)
			index += 1
		queryidf = [self.index.idf[word] for word in self.index.getUniques()]
		magnitude = pow(sum(map(lambda x: x**2, queryVec)),.5)
		freq = self.termfreq(self.index.getUniques(), query)
		tf = [x/magnitude for x in freq]
		final = [tf[i]*queryidf[i] for i in range(len(self.index.getUniques()))]
		return final

	def rankResults(self, resultDocs, query):
		vectors = self.make_vectors(resultDocs)
		queryVec = self.query_vec(query)]
		results = [[self.dotProduct(vectors[result], queryVec), result] for result in resultDocs]
		results.sort(key=lambda x: x[0])
		results = [x[1] for x in results]
		return results

	def one_word_query(self, word):
		pattern = re.compile('[\W_]+')
		word = pattern.sub(' ',word)
		if word in self.invertedIndex.keys():
			return self.rankResults([filename for filename in self.invertedIndex[word].keys()], word)
		else:
			return []
			
