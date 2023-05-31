# load data
import openpyxl
# system tools
import os
import sys
sys.path.append(".")
# data munging tools
import pandas as pd
# Machine learning stuff
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
# save model and vectorizer
from joblib import dump
# Visualisation
import matplotlib.pyplot as plt

sermon_path = os.path.join("..", "768706", "data", "content.dat")
meta_sermon_path = os.path.join("..", "768706", "metadata", "Joined_Meta.xlsx")

def get_data(data_path, meta_path):
    # load sermons data
    data = pd.read_csv(sermon_path, index_col=0) 
    meta = pd.read_excel(meta_path)
    # merge on document IDs
    full_data = data.merge(meta, left_on="id", right_on="ID-dok")
    # define X and y
    X = full_data["content"]
    y = full_data["køn"]
    labels = ["male", "female"]
    # train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, # texts for the model
                                                        y, # classification labels
                                                        test_size=0.2,   # create an 80/20 split
                                                        random_state=42) # random state for reproducibility
    print("Data prepared!")

    return X_train, X_test, y_train, y_test, labels

def sermon_vectorizer(X_train, X_test):
    # create vectorizer object using a bag-of-words model
    vectorizer = CountVectorizer(ngram_range = (1,2), # unigrams and bigrams (1 word (e.g. York) and 2 word (e.g. New York) units)
                                lowercase =  True, # make everything lower case
                                max_df = 0.95, # remove very common words
                                min_df = 0.05, # remove very rare words
                                max_features = 100) # keep only top 100 features
    # fit vectorizer to training data
    X_train_feats = vectorizer.fit_transform(X_train)
    # transform test data
    X_test_feats = vectorizer.transform(X_test)
    # get feature names
    feature_names = vectorizer.get_feature_names_out()
    # save vectorizer
    vec_outpath = os.path.join("models", "sermon_gender_vectorizer.joblib")
    dump(vectorizer, vec_outpath)
    print("Vectorizer saved")

    return X_train_feats, X_test_feats, vectorizer, feature_names

def sermon_classifier(X_train_feats, X_test_feats, y_train, y_test, labels):
    # set up a MLPClassifier
    classifier = MLPClassifier(activation = "relu",
                           hidden_layer_sizes = (30, 10), # number of notes in hidden layers 
                           max_iter=500, # number of iterations
                           random_state = 42)
    # fit data to the classifier
    history = classifier.fit(X_train_feats, y_train)
    # Get predictions
    y_pred = classifier.predict(X_test_feats)
    # save classifier
    clf_outpath = os.path.join("models", "sermon_gender_clf.joblib")
    dump(classifier, clf_outpath)
    print("Trained model saved!")
    
    # Evaluation with confusion matrix 
    confusion_metrix = metrics.ConfusionMatrixDisplay.from_estimator(classifier,
                                                X_train_feats, # the training data features         
                                                y_train, # the training labels
                                                cmap=plt.cm.Blues, # set colours
                                                labels=[1, 2])# the labels in the data arranged
    # save confusion metrix
    metrix_path = os.path.join("out", "confusion_matrix.png")
    plt.savefig(metrix_path)
    
    # clasification report
    classifier_report = metrics.classification_report(y_test, y_pred, target_names=labels )
    print(classifier_report)
    # Save classification report in "out"
    report_path = os.path.join("out", "classificationreport.txt")
    #"writing" classifier report and saving it
    with open(report_path, "w") as f: 
        f.write(classifier_report)
    print("Classification report saved")
    
    return classifier, classifier_report

def main():
    # load and prepare data
    X_train, X_test, y_train, y_test, labels = get_data(sermon_path, meta_sermon_path)
    # vectorize data
    X_train_feats, X_test_feats, vectorizer, feature_names = sermon_vectorizer(X_train, X_test)
    # train classifier model
    classifier, classifier_report = sermon_classifier(X_train_feats, X_test_feats, y_train, y_test, labels)

if __name__ == "__main__":
    main()