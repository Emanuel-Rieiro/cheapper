import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False

def remove_stopwords(texts):
    stop_words = set(stopwords.words('spanish'))
    stop_words.add('gr')
    stop_words.add('g')
    stop_words.add('grs.')
    stop_words.add('grs')
    stop_words.add('kg')
    stop_words.add('kg.')
    stop_words.add('&')
    stop_words.add('+')
    stop_words.add('.')
    stop_words.add('%')
    stop_words.add('clasica')
    cleaned_texts = []
    for text in texts:
        cleaned_text = [word for word in text.split() if word.lower() not in stop_words]
        cleaned_texts.append(' '.join(cleaned_text))
    return cleaned_texts

def remove_stopwords_together(texts):
    
    new_names = []
    for names in texts:
        
        new_name = []
        for name in names.split():
            
            if containsNumber(name):
                new_name.append(re.findall(r'\d+', name)[0])
            else:
                new_name.append(name)
        
        new_names.append(' '.join(new_name))
    return new_names

def remove_yerba_mate(texts):
    if 'yerba' in texts.split() and 'mate' in texts.split():
            return texts.replace('mate ','')
    else:
        return texts

def clean_description(text):

    text = str(text) # get everything to str
    text = text.lower() # lowercase everything
    text = text.replace('c/','') # get rid of the c/
    text = text.replace('(','')
    text = text.replace(')','')
    text = text.replace('/',' ')
    text = text.replace('á','a')
    text = text.replace('é','e')
    text = text.replace('í','i')
    text = text.replace('ó','o')
    text = text.replace('ú','u')

    text = remove_stopwords(pd.Series(text)) # stopwords
    text = remove_stopwords_together(pd.Series(text)) # clean "500g" like descriptions
    text = [remove_yerba_mate(descriptions) for descriptions in pd.Series(text)] # remove mate from yerba mate

    return text