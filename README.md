# assignment5_lang_self-assigned_Emma-Marie 

## Description and purpose
Self-assigned assignment for language analytics. A classifier trained on danish sermons to predicting the gender of the priest writing the specific sermon. This prediction is a binary classification problem with the seromns either having the label 1 for male or 2 for female. I use the ```shap``` package to get knowledge about which words had themost inpact on the output of the model. If a word has a positive SHAP vaue, the word has a possitive impact which leads the model to predict class 1. A negative SHAP value means that the word has a negative value, and that it leads the model to predict class 0.

if the model predicts 0 or 1, WHICH LEADS TO PREDICTING MALE (1) AND WHICH TO FEMALE (2)?

The purpose of the assignment is to do the following:
- train a MLP classifier model to distinguish between sermons written by male and female pastors.
- save a classification report
- save the trained model and the vectorizer
- Get the Shap values and save visualisation of them.

## Data
The data used for this assignemnet is a corpus of 11,955 sermons by 95 pastors from the Evangelical Lutheran Church in Denmark. The data set contains different information about the pastors and the day the sermon was held, but for my classifier I only need the gender (1 = male, 2 = female), and the sermon content. More information about the dataset can be found here: https://github.com/centre-for-humanities-computing/praedikener 

__NB__ Due to GDPR rules, I haven't pushed the data set to Github. You must get the data from my teacher Ross to be able to run the script. For the code to run properly, the folder with the data must be placed outside the assignment folder. Your folder structure should looks like this:

    - 76870
        - data
            - content.dat
        - metadata  
            - Joined_Meta.xlsx
    - cds-language
        - assignment-5_lang_self-assigned_Emma-Marie

or this???? --> then change paths!!

    - 76870
        - data
            - content.dat
        - metadata  
            - Joined_Meta.xlsx
    - assignment-5_lang_self-assigned_Emma-Marie

## Script
The main script of this assignent is called ```sermons_clf.py```, and can be found in the ```src``` folder. The script consists of the following parts:
- __get_data()__ loads in the sermons data and split it into train and test data and labels
- __sermon_vectorizer()___ vectorizes the train and test data, and creates the train and test features in the two new variables ```X_train_feats``` and ```X_test_feats```. 
- __sermon_classifier()__ 
- __shap_values()__ calculate the shap values and plot them.
- __main()__ ... A cLassification report saved in ```out``` folder, and the classifier and vectoriser are both saved in the ```models``` folder. 

## How to run script

### Prerequisites
Please install Bash and Python 3 before running the code. I created and tested the code using the app "Coder Python 1.73.1" on Ucloud.sdu.dk. 

### Running the script
The script is run from the commandline by running the following commands:

- "bash setup.sh" creates a virtual environment, and installs the requirements.txt. 

        bash setup.sh

- "run.sh" activates the virtual environment, runs the ```sermons_clf.py``` script and deactivates the environment again. 

        bash run.sh

## Discussion of results
The model has an accuracy of 80% in predicting male and female pastors from their sermons. The shap value plot shows, that the most ...

Shap plot: 
The y-axis indicates the variable name, in order of importance from top to bottom (omformuler)

## References
Centre-for-humanities-computing, Github: https://github.com/centre-for-humanities-computing/praedikener 
