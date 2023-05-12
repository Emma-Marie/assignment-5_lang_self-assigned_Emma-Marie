# load data
import pandas as pd
import openpyxl
# system tools
import os
import sys
sys.path.append(".") # necessary if I don't use utils?
# data munging tools
import pandas as pd
# Machine learning stuff
from sklearn.feature_extraction.text import CountVectorizer#, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, ShuffleSplit
from sklearn import metrics
# save model and vectorizer
from joblib import dump, load
# Shap values document classification
import shap
import tensorflow
# Visualisation
import matplotlib.pyplot as plt

def get_data():
    # load sermons data
    sermon_path = os.path.join("..", "..", "768706", "data", "content.dat")
    data = pd.read_csv(sermon_path, index_col=0) 
    # load metadata
    meta_path = os.path.join("..", "..", "768706", "metadata", "Joined_Meta.xlsx")
    meta = pd.read_excel(meta_path)
    # merge on document IDs
    full_data = data.merge(meta, left_on="id", right_on="ID-dok")
    # define X and y
    X = full_data["content"]
    y = full_data["køn"]
    labels = ["male", "female"]
    # train-test split
    X_train, X_test, y_train, y_test = train_test_split(X,           # texts for the model
                                                        y,          # classification labels
                                                        test_size=0.2,   # create an 80/20 split
                                                        random_state=42) # random state for reproducibility
    
    return X_train, X_test, y_train, y_test, labels

def sermon_vectorizer(X_train, X_test):
    # create vectorizer object using a bag-of-words model
    vectorizer = CountVectorizer(ngram_range = (1,2),     # unigrams and bigrams (1 word (e.g. York) and 2 word (e.g. New York) units)
                                lowercase =  True,       # make everything lower case
                                max_df = 0.95,           # remove very common words
                                min_df = 0.05,           # remove very rare words
                                max_features = 100)      # keep only top 100 features
    # fit vectorizer to training data
    X_train_feats = vectorizer.fit_transform(X_train)
    # transform test data
    X_test_feats = vectorizer.transform(X_test)
    # get feature names
    feature_names = vectorizer.get_feature_names_out()

    return X_train_feats, X_test_feats, vectorizer, feature_names

def sermon_classifier(X_train_feats, X_test_feats, y_train, y_test, labels):
    classifier = MLPClassifier(activation = "logistic",
                           hidden_layer_sizes = (30, 10), # number of notes in hidden layers 
                           max_iter=1000,
                           random_state = 42)
    # fit data to the classifier
    classifier.fit(X_train_feats, y_train)
    # Get predictions
    y_pred = classifier.predict(X_test_feats)
    # clasification report
    classifier_metrics = metrics.classification_report(y_test, y_pred, target_names=labels )
    print(classifier_metrics)
    
    return classifier, classifier_metrics
    
def shap_values(classifier, X_train_feats, X_test_feats, feature_names):
    # Shap values
    explainer = shap.KernelExplainer(classifier.predict, shap.sample(X_train_feats, 30))
    shap_values = explainer.shap_values(shap.sample(X_test_feats, 30))
    shap.summary_plot(shap_values, shap.sample(X_test_feats, 30), feature_names)
    # Save shap values plot
    shap_plot_path = os.path.join("out", "shap_plot.png")
    plt.savefig(shap_plot_path)

def main():
    # load and prepare data
    X_train, X_test, y_train, y_test, labels = get_data()
    print("Data prepared!")
    # vectorize data
    X_train_feats, X_test_feats, vectorizer, feature_names = sermon_vectorizer(X_train, X_test)
    print("Data vectorized!")
    # train classifier model
    classifier, classifier_metrics = sermon_classifier(X_train_feats, X_test_feats, y_train, y_test, labels)
    print("Model trained!")
    # shap values
    shap_values(classifier, X_train_feats, X_test_feats, feature_names)
    print("Shap values found and plot saved!")

    # Save classification report in "out"
    folder_path = os.path.join("out")
    file_name = "classificationreport.txt"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w") as f: #"writing" classifier report and saving it
        f.write(classifier_metrics)
    # save vectorizer
    vec_outpath = os.path.join("models", "sermon_vectorizer.joblib")
    dump(vectorizer, vec_outpath)
    # save classifier
    clf_outpath = os.path.join("models", "sermon_gender_clf")
    dump(classifier, clf_outpath)
    
    print("Models and report saved!")

if __name__ == "__main__":
    main()