import os
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.svm import SVC
from sklearn.preprocessing import normalize
from sklearn.preprocessing import scale


text_dir = "/home/joan/Escritorio/Datasets/LiteraryDataset/chapter_divided/"
count_vect = CountVectorizer()
clf = TfidfVectorizer(input=u'filename', encoding=u'utf-8', decode_error=u'strict', strip_accents=None, lowercase=True, preprocessor=None, tokenizer=None, analyzer=u'word', stop_words=None, ngram_range=(1, 1), max_df=1.0, min_df=1, max_features=None, vocabulary=None, binary=False, norm=u'l2', use_idf=True, smooth_idf=True, sublinear_tf=False)
docs = []
labels = []
for fname in os.listdir(text_dir):
	raw = open(text_dir+fname,"r").read()
	docs.append(raw)
	label = fname.split("_")[1]
	labels.append(label)

X_train_counts = count_vect.fit_transform(docs)
tfidf_transformer = TfidfTransformer(norm='l1', use_idf=True, smooth_idf=True, sublinear_tf=False)
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

feature_array = np.array(count_vect.get_feature_names())
tfidf_sorting = np.argsort(X_train_tfidf.toarray()).flatten()[::-1]

ns = [1000]
for n in ns:
	out = open("./tfidfwords/tfidfBritish"+str(n),"w")
	top_n = feature_array[tfidf_sorting][:n]
	content = "\n".join(top_n)
	out.write(content)
	out.close()

exit()

'''
clf = SVC()
X_norm = scale(X_train_tfidf, axis=0, with_mean=False, with_std=True, copy=True)

out = cross_val_score(clf, X=X_norm, y=labels, scoring="accuracy", cv=10, n_jobs=-1, verbose=0, fit_params=None)
print "Mean " + str(np.mean(out)) + "\n"
print "Median " + str(np.median(out)) +"\n"
print "Std " + str(np.std(out)) + "\n"	
'''
