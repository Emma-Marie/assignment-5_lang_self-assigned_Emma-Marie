# assignment5_lang_self-assigned_Emma-Marie 

## 1. Contribution
I have developed the code for this assignment without other contributors. 

## 2. Description
This self-assigned assignment has two parts. The first is to train a classifier on Danish sermons, which can predict the gender of the pastor who has written the specific sermon. This prediction is a binary classification problem with the sermons either having the label 1 for male or 2 for female. The second part is to investigate gender differences using string processing. I created a script that makes it possible to investigate the co-occurrence of a parsed word in the male and female sermons respectively to see if some words are used in different contexts by male and female pastors.

## 3. Methods
For the classification script ```sermons_clf.py``` I merged the data and meta data, assigned the gender labels to y and the content of the sermons to x, and did a train-test split. Then I vectorized the sermons data with a CountVectorizer keeping the 100 most occurring features. I loaded a MLPclassifier and train it on the sermons data. The output of the script was a classification report and a confusion metrix, which are all saved in the out folder. This output is used to evaluate the model performance. The trained model and the vectorizer are saved in the ```models``` folder. 
The script ```string_processing.py``` splits the sermon data into a male and female corpus, and the text in each corpus are turned lowercase, the tokens are split, punctuation, and newline markers are removed using regex. The it finds every example of the keyword in the text and extract the five tokens before and the five tokens after it. Danish stop words from a stop words text file are removed from the corpuses, and the parsed number of co-occurring words are found. They are turned into a data frame alongside with the number of times the token co-occurs with the key word.  The output files are saved in the out folder in a subfolder by the same name of the keyword, and the output makes it possible to investigate the context in which the token appears. The keyword and the number of cooccurring words can be parsed as arguments when the script is run through the command line. 

## 4. Data
The dataset is a corpus of 11,955 sermons written by 95 pastors from the Evangelic Lutheran Church in Denmark. The sermons are written in Danish. The dataset contains different information about the pastors, but for this assignment I only use information about the content of the sermons and the gender of the pastors. The dataset has a data folder and a meta data folder. More information about the dataset can be found here: https://github.com/centre-for-humanities-computing/praedikener. 

### 4.1 Get the data
Because of GDPR regulations, the data set isn’t pushed to GitHub, and can’t be found online. Therefore, the dataset must be provided by my teacher Ross. For the code to run properly, please upload the data set to the repository, so you get the following folder structure:

    - 76870
        - data
            - content.dat
        - metadata  
            - Joined_Meta.xlsx
    - assignment-5_lang_self-assigned_Emma-Marie

NB the folder 76870 is the name of the sermons data folder, at least when I get it from GitHub. Make sure to check if your data folder has the same name. 

## 5. Usage

### 5.1 Prerequisites
For the scripts to run properly, please install Python 3 and Bash. The code for this assignment is created and tested using the app “Coder Python 1.73.1” on Ucloud.sdu.dk. The final step it to clone the GitHub repository on your own device.

### 5.2 Install packages
Run ”bash setup.sh” from the command line to create a virtual environment and install the required packages from requirements.txt:
		bash setup.sh

### 5.3 Run the scripts
To run the ```sermons_clf.py``` you need to run the command “bash run.sh” from the command line to activate the virtual environment, run the scripts and deactivate the environment again:

        bash run.sh

Running ```string_processing.py``` has two steps. First, run “source sermons_env/bin/activate” to manually activate the virtual environment. 

        source sermons_env/bin/activate

Then, run  “python3 src/string_processing.py --keyword  --cooccurring” from the command line. The --keyword argument is the word, which you want to investigate the co-occurrence of. Remember that the word must be written in small letters, because every token is turned into small letters in the data preprocessing function. The --cooccurring argument is the number of most co-occurring words you wish to get. If no number is specified, 10 is the default. The code below is an example with the word “kvinde” (woman) as keyword and 15 as the number of co-occurring words:

        python3 src/string_processing.py --keyword kvinderne --cooccurring 15


## 6. Discussion of results
Looking at the confusion metrix it seems like the model isn’t overfit. 153 male sermons are classified as female and 296 female sermons are classified as male. It is a good sign that some (but of cause not too many) of sermons are miss classified, because if the model is too “good” it can indicate, that the model can’t generalize, which means that it would have a hard time classifying sermons, which it hasn’t seen before. The accuracy of the model is 68%, which isn’t fantastic, but fine. The model is slightly better at predicting male sermons (72%) that female sermons (63%). 

For the string processing, I tried to parse "kvinde" (woman) as keyword and 15 as the number of co-occurring words. 
My hypothesis behind choosing this keyword was, that female pastors would mention the word "kvinde" more often than the male pastors, and that the context of "kvinde" would references more to passive female caracters in bible histories in the male sermons, while the "kvinde" would be used in a more active context in female sermons. I also thought that “kvinde” would be more likely to co-occur with words related to children or household in male sermons than in female sermons.

- Looking at the CSVs displaying the context of the keyword I found that female pastors used the word “kvinde” (woman) more often than men. Female pastors used it 18 times (in 5122 sermons) while the male pastors used it 16 times (in 6816 sermons). It seems like the female pastors mention "kvinde" in relation to a personal story which isn't from the bible more often than the male pastors do, while the male pastors more often use the word "kvinde" in relation to stories about women from the bible e.g. in relation to "kanaanæiske".
- Looking at the CSVs displaying co-occurring words, the  word “kvinde” is likely to co-occur with “barn” (child) in the male sermons, while "barn" isn't among the 15 most co-occurring words in the female sermons. In female sermons, "kvinde" are more likely to co-occur with "jesus" than in male sermons. This could indicate that the female pastors emphasize the presence of women around Jesus and their importance in relation to Jesu life and work more than male pastors, who relate the women more to the role of being a mother.

__Further notes__: I am aware, that my conclusions are very weak, and that I only point to some small indications from the output of the script.  My claims obviously need to be examined in way more depth for me to be able to conclude anything for real. The script should be seen as a helping tool which can be used to initiate an analysis process and give an idea of what could be investigated further in an analysis using a more in depth reading of the sermons. 
 

## 7. References
”Danish Sermons”, Center for Humanities Computing Aarhus, GitHub: 
https://github.com/centre-for-humanities-computing/praedikener

Centre-for-humanities-computing, Github: https://github.com/centre-for-humanities-computing/praedikener 

"stopord.txt": https://gist.github.com/berteltorp/0cf8a0c7afea7f25ed754f24cfc2467b


