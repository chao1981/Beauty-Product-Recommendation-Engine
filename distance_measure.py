from __future__ import division, unicode_literals
import nltk

#This function measure the how the two paragraph 
#are closely related, however, one paragraph is treated
#as a based paragraph (for future comparision with other paragraphs)
def two_paragraph_distance(based_p,other_p):
    stopword = nltk.corpus.stopwords.words('english')
    based_p_list = "".join(based_p).split()
    based_p_set = set([word for word in based_p_list if word not in stopword])
    other_p_list = "".join(other_p).split()
    other_p_set = set([term for term in other_p_list if term not in stopword])
    nom = len(based_p_set.intersection(other_p_set))
    denom = len(based_p_set) + 1
    return nom/denom