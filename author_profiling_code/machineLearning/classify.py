from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import numpy as np
from sklearn.preprocessing import scale
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier

class SupervisedLearning:

	def __init__(self, iC):
		self.featureVectors, self.labels = iC.getSklearnInput()
		self.normalize()

	def normalize(self):
		self.normalizedFeatureVectors = scale(self.featureVectors, axis=0, with_mean=True, with_std=True, copy=True)

	'''
		kernel: linear, poly, rbf, sigmoid, precomputed or a callable
		outProbs: boolean whether to output the probabilities or not. Default False
		decision_function_shape: ovo (one vs one), ovr (one vs rest). Default ovr
	'''
	def SVM(self, kernel = "linear", outProbs = False, decision_function_shape=None):
		clf = SVC(C=1.0, kernel=kernel, degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=outProbs, tol=0.001, cache_size=200, class_weight=None, verbose=False, decision_function_shape=decision_function_shape)
		return clf

	'''
		n_estimators: number of decision trees
		criterion: gini, entropy. entropy => information gain. Split quality metric.
		max_features: number of features considered. int (specific number), float (specific percentage), auto (sqrt num feats), log2 o None (all)
		http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier
	'''
	def RandomForests(self):
		clf = RandomForestClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, min_impurity_split=1e-07, bootstrap=True, oob_score=False, n_jobs=-1, random_state=None, verbose=0, warm_start=False, class_weight=None)
		return clf

	'''
		metric: accuracy, average_precision, f1, f1_micro, f1_macro, f1_weighted, f1_samples, 
				precision, precision_micro, precision_macro, precision_weighted, precision_samples, recall, 
				recall_micro, recall_macro, recall_weighted, recall_samples, roc_auc
	'''
	def cross_validation(self, clf, folds = 10):
		metrics = ["accuracy","f1_weighted","recall_weighted","precision_weighted"]
		for metric in metrics:
			out = cross_val_score(clf, X=self.normalizedFeatureVectors, y=self.labels, scoring=metric, cv=folds, n_jobs=-1, verbose=0, fit_params=None)
			self.show_results(out, metric)
		

	def show_results(self, out, metric):
		print "Results using the following metric: " + metric + "\n"
		print "Fold Results" + "\n"
		print out
		print "Mean " + str(np.mean(out)) + "\n"
		print "Median " + str(np.median(out)) +"\n"
		print "Std " + str(np.std(out)) + "\n"

	def save_model(self, clf, pathPickle):
		joblib.dump(clf, pathPickle)

	def load_model(self, pathPickle):
		clf = joblib.load(pathPickle)
		return clf