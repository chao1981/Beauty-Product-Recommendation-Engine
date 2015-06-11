import nltk
import numpy as np

def _score_sentences(sentences, important_words,Cluster_threshold = 5):
    scores = []
    sentence_idx = -1
    
    #word_tokenize(s) split a sentence and find all the words and punctuations
    for s in [nltk.tokenize.word_tokenize(s) for s in sentences]:
        sentence_idx += 1
        word_idx =[]
        
        # This function check whether any important words occur in the sentence
        # if  there is, record the location of the important word in the sentence
        for w in important_words:
            try:
                word_idx.append(s.index(w))
            except ValueError, e:
                pass
        word_idx.sort()
        
        #If there is no important words in the sentence, skip the rest of the loop
        #and goes on to next sentence
        if len(word_idx) == 0 : continue
        
        #compute clusters by using a max distance threshold for any two consecutive words
        clusters = []
        cluster = [word_idx[0]]
        
        i = 1
        while i < len(word_idx):
            if word_idx[i] - word_idx[i-1] < Cluster_threshold:
                cluster.append(word_idx[i])
            else:
                clusters.append(cluster[:])
                cluster = [word_idx[i]]
            i += 1
        clusters.append(cluster)
        
        #now score each cluster. The max score for any give cluster is the score for the 
        #sentence
        
        max_cluster_score = 0
        for c in clusters:
            num_important_words_in_cluster = len(c)
            total_words_in_cluster = c[-1] - c[0] + 1
            score = 1.0 * num_important_words_in_cluster\
                    *(num_important_words_in_cluster/total_words_in_cluster)
            
            if score > max_cluster_score:
                max_cluster_score = score 
        scores.append((sentence_idx,score))
    return scores
        

def summarize(txt, N=100, Top_sentences = 5):
    # creat a list of sentences from text file and normalize those sentences
    sentences = [s.lower() for s in nltk.tokenize.sent_tokenize(txt)]
    
    #create a list of words from the entire text file
    words = [w.lower() for sentence in sentences for w in nltk.tokenize.word_tokenize(sentence)]
    fqdist = nltk.FreqDist(words)
    
    #create a list of stop_words  (word that are not important that they appear)
    #because this is a beauty product recommendation app, I don't want the summary
    #to talk about the seller or delivery system
    stop_words = nltk.corpus.stopwords.words('english') \
                + ['usps','shipping','$','#', 
                   '&','order','seller','packaging','manufacture',
                   'package','cute','delivery', '.',',',
                   '?','...']
######################################################################    
    top_n_words = [w[0] for w in fqdist.items() 
                  if w[0] not in stop_words][:N]
######################################################################

#CUSTOMIZE important words:
#     top_n_words = ['skin','mosturizer', 'smooth','care', 
#                   'dry', 'breakout', 'pimples','good',
#                   'greasy','effective', 'great','restoration',
#                   'expensive', 'cheap','works','relief',
#                   'well', 'fast', 'young', 'wrinkle','itching',
#                   'awesome','love', 'mosturizing','glow','miracle',
#                   'healthy','white','bright','shine','cream','red',
#                   'terrible','creams','absorb','smell','smelly','natural',
#                   'organic', 'hydrate', 'light', 'effects', 'change', 'soft',
#                   'non','inexpensive','worthless', 'wonderful','soothing',
#                   'clear', 'dull', 'cheap', 'combination']
    
    scored_sentences = _score_sentences(sentences, top_n_words)
    
    #Summarization Approach 1:
    avg = np.mean([s[1] for s in scored_sentences])
    std = np.std([s[1] for s in scored_sentences])
    mean_scored = [(sent_idx, score) for (sent_idx, score) in scored_sentences 
                    if score > avg + 0.5 *std ]

    
    #Summarization Approach 2:
    top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-Top_sentences:]
    top_n_scored = sorted(top_n_scored, key=lambda s: s[0])
    
    return dict(top_n_summary=[sentences[idx] for (idx,score) in top_n_scored],
                mean_score_summary=[sentences[idx] for (idx,score) in mean_scored])