#Libraries used in this problem
import pandas as pd  
from textblob.classifiers import NaiveBayesClassifier


#Static Text for this specific csv file

main_language = 'English'
language_2 = 'Afrikaans'
language_3 = 'Nederlands'


url = 'lang_data.csv'
text_column = "text"
language_column = "language"

# This class opens the file and return all data except where text field = null

class LanguageFile:
    def __init__(self, url):
        self.url = url
    @property   
    def open_the_file(self):
        raw_data = pd.read_csv(self.url)
        languages = raw_data[language_column].unique()
        data = raw_data[pd.notnull(raw_data[text_column])]
        return data 

# This function converts the all the data to be used in texblob

def all_language_classification():
        all_languages = []
        file =LanguageFile(url).open_the_file
        for row in file.iterrows():
            index, data_ = row
            all_languages.append(data_.tolist())
        return all_languages
    
# This function converts non english language data to be used in texblob    

def non_main_language_classification():
        non_main_language = []
        file =LanguageFile(url).open_the_file
        for row in file[(file[language_column]!= main_language)].iterrows():
            index, data_ = row
            non_main_language.append(data_.tolist())
        return non_main_language

 # Training of all languages data
train_all_languages = NaiveBayesClassifier(all_language_classification())

 # Training of afrikaans and Nederlands language data
train_Afrikaans_and_Nederlands = NaiveBayesClassifier(non_main_language_classification()) 


# This function uses the training above to determine what language is the text

def WhatLangaugeIs(text_to_classify): 
    
    if (train_all_languages.classify(text_to_classify)== main_language):
        return main_language
    
    elif (train_Afrikaans_and_Nederlands.classify(text_to_classify) == language_2):
        return language_2
    else:
        return language_3

class ModelArchtecture:
    def __init__(self,length):
        self.length = length
    @property    
    def test_all(self):
        return train_all_languages.show_informative_features(self.length) 

all_language_analysis=[]

file = LanguageFile(url).open_the_file
languages = file[language_column].unique()

for i in languages:
    each_lang = file[file[language_column]==i]
    list_each_lang = each_lang[text_column].tolist()
    language_analysis = []
    count =0
    for x in range(len(each_lang)):
        if WhatLangaugeIs(list_each_lang[x])== str(i):
            count +=1
    percentage_accuracy = count/len(each_lang)
    language_analysis.append(i)
    language_analysis.append(len(each_lang))
    language_analysis.append(count)
    language_analysis.append(percentage_accuracy)
    all_language_analysis.append(language_analysis)

all_language_analysis
data_accuracy = pd.DataFrame(all_language_analysis, columns = ["Language", "Total text","Detected text","Percentage accuracy"])

print(data_accuracy)
print("**********   TEST   **************")
print("Write a text to check the language or 'exit' to close the language classification.")
while True:
	what_language = input("What language is this text: ")
	if what_language != 'exit':
		print(WhatLangaugeIs(what_language))
	elif what_language == "exit":
		print("--------DONE CLASSIFYING--------")
		break
		
	else: print('Incorrect input')
