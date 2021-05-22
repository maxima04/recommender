'''
DataFrame Manipulation functions should be here

Create folder for csv files

!!! Note !!!

Download in your free time "python -m spacy download en_core_web_sm" needed for aspect extraction

'''
'''
DataFrame Manipulation functions should be here

Create folder for csv files
'''
import os
import pandas as pd
import numpy as np
import re
from pathlib import Path
import json
import spacy

from .commons import *

import nltk

from nltk import word_tokenize, pos_tag, pos_tag_sents
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet 
from sklearn.feature_extraction.text import CountVectorizer

import csv


BASE_DIR = Path(__file__).resolve().parent.parent

COMMONS_DIR = os.path.join(BASE_DIR, 'app/commons')

OPINION_SURVEY_DIR = os.path.join(COMMONS_DIR,'opinion_survey.csv')
LIKERT_SURVEY_DIR = os.path.join(COMMONS_DIR,'likert_survey.csv')

def uploadDataSentiment(data):

    with open(OPINION_SURVEY_DIR, 'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(data)
        

    return None

def uploadDataLikert(data):

    with open(LIKERT_SURVEY_DIR, 'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(data)
        

    return None

def countLikert():

    df = pd.read_csv(LIKERT_SURVEY_DIR)

    agg_results = pd.get_dummies(df.stack()).groupby(level=1).sum().reset_index()

    sorter = df.columns.tolist() ### List of correctly positioned titles
    sorterIndex = dict(zip(sorter, range(len(sorter)))) ## Dictionary of titles with corresponding position number


    agg_results['ID'] = agg_results['index'].map(sorterIndex) ### Create ID Column where its number will be based on 
                                                          ### the position number of the original positioning
                                                          ### of the titles
    agg_results = agg_results.sort_values('ID',ascending = True) ## Sort DF by ID Column
    agg_results = agg_results.drop('ID',axis=1) ## Drop ID column
    agg_results = agg_results.reset_index() ## Reset index due to the original index numbers will be scrambled
    agg_results = agg_results.drop(agg_results.columns[[0]], axis=1)

    order = ['index','Strongly Agree', 'Agree', 'Disagree','Strongly Disagree'] ## Original Order
    agg_results = agg_results.reindex(columns=order) ## Reindexing
    agg_results.reset_index(drop=True)


    likert_list = agg_results.values.tolist()
    likert_results = [i[1:] for i in likert_list]

    agg_results.columns = ['index','StronglyAgree', 'Agree', 'Disagree','StronglyDisagree']
    to_df = agg_results.to_json(orient ='records')
    to_dct = agg_results.to_dict()
    data = json.loads(to_df)

    return likert_results, data, to_dct


def calculateSentiment():
    stoplist = stopwords.words('english') + ['though']
    c_vec = CountVectorizer(stop_words=stoplist, ngram_range=(3,5))

    sid = SentimentIntensityAnalyzer()
    lemmatizer = WordNetLemmatizer() 

    df = pd.read_csv(OPINION_SURVEY_DIR)

    df = df.replace(np.nan, 'Neutral', regex=True)

    col_range = len(df.columns) # number of columns
    stored_pos = []
    for i in range(0,col_range):
        col = df.columns[i] # The current column
        df.loc[:,col] = df[col].apply(lambda x : str.lower(str(x))) ## To Lower Case
        df.loc[:,col] = df[col].apply(lambda x : " ".join(re.findall('[\w]+',x))) # Remove Punctuations
        df.loc[:,col] = df[col].apply(lambda x : remove_stopWords(x)) # Remove Stop words
        
        ##POS TAGGING
        texts = df.loc[:,col].tolist()
        tagged_texts = pos_tag_sents(map(word_tokenize, texts)) ### Tag every word in a row with POS
        
        ### Lemmatization
        new = []

        stored_pos.append(tagged_texts)
        for i in tagged_texts:
            #if len(i) > 0:
            lemmatized_sentence = []
            for word, tag in i:
                tag = pos_tagger(tag) ### Convert POS Tag to known POS for simplification
                if tag is None: 
        # if there is no available tag, append the token as is 
                    lemmatized_sentence.append(word) 
                else:         
        # else use the tag to lemmatize the token 
                    lemmatized_sentence.append(lemmatizer.lemmatize(word, tag)) 

            lemmatized_sentence = " ".join(lemmatized_sentence) 
            #print(lemmatized_sentence)
            new.append(lemmatized_sentence)
            
        else:
            pass
    
    
        df['POS'] = new ## Store tagged words
    
    
    df = df.replace(r'^\s*$', "neutral", regex=True) ## If row value is null, replace with neutral string
    df = df.iloc[:,:-1]
    static_df = df

    

    comp = []
    col_range = len(static_df.columns) # number of columns
    
    for i in range(0,col_range):
        col = static_df.columns[i] # The current column
        ngrams = c_vec.fit_transform(static_df[col])
        vocab = c_vec.vocabulary_
        vocab = vocab.keys()

        df = pd.DataFrame(vocab, columns = ['ngram'])

        df['scores'] = df['ngram'].apply(lambda x: sid.polarity_scores(x)) ## Get polarity score of every Column
        compound = df['scores'].apply(lambda score_dict: score_dict['compound']) ## Extract the compound from the results
        ave = np.average(compound)# Get the mean compound of each columns
        comp.append(ave)
    
    labels = static_df.columns
    labels = list(labels)

    new_sent = [dict(zip(labels, datum)) for datum in [comp]]
    
    return new_sent[0], comp
    

def getAspect():

    df = pd.read_csv(OPINION_SURVEY_DIR)
    ndf = df
    nlp = spacy.load('en_core_web_sm')

    col_range = len(ndf.columns) # number of columns
    stored_pos = []
    tokens = []
    aspect_terms = []
    for i in range(0,col_range):
        col = df.columns[i] # The current column
        ndf.loc[:,col] = ndf[col].apply(lambda x : str.lower(str(x))) ## To Lower Case
        ndf.loc[:,col] = ndf[col].apply(lambda x : " ".join(re.findall('[\w]+',x))) # Remove Punctuations
        ndf[col + "(CLEANSED TEXT)"] = ndf[col].apply(lambda x : remove_stopWords(x)) # Remove Stop words
        ndf.loc[:,col] = ndf[col].apply(lambda x : remove_stopWords(x))
        ndf[col + "(TOKENIZED)"] = ndf[col].apply(lambda x : word_tokenize(x))
        ndf.loc[:,col] = ndf[col].apply(lambda x : word_tokenize(x))
        ndf[col + "(POS_TAGGED)"] = ndf[col].apply(lambda x : pos_tag(x))   

    col_range = len(df.columns) # number of columns

    for i in range(0,col_range):
        aspect_terms = []
        col = ndf.columns[i]
        for x in range(len(ndf.loc[:,col])):
            amod_pairs = []
            advmod_pairs = []
            compound_pairs = []
            xcomp_pairs = []
            neg_pairs = []

            if len(str(df[col][x])) != 0:
                lines = str(df[col][x]).replace('*',' ').replace('-',' ').replace('so ',' ').replace('be ',' ').replace('are ',' ').replace('just ',' ').replace('get ','').replace('were ',' ').replace('When ','').replace('when ','').replace('again ',' ').replace('where ','').replace('how ',' ').replace('has ',' ').replace('Here ',' ').replace('here ',' ').replace('now ',' ').replace('see ',' ').replace('why ',' ').split('.')       
                for line in lines:
                    doc = nlp(line)
                    str1=''
                    str2=''
                    for token in doc:
                        if token.pos_ == 'NOUN':
                            for j in token.lefts:
                                if j.dep_ == 'compound':
                                    compound_pairs.append((j.text+' '+token.text,token.text))
                                if j.dep_ == 'amod' and j.pos_ == 'ADJ': #primary condition
                                    str1 = j.text+' '+token.text
                                    amod_pairs.append(j.text+' '+token.text)
                                    for k in j.lefts:
                                        if k.dep_ == 'advmod': #secondary condition to get adjective of adjectives
                                            str2 = k.text+' '+j.text+' '+token.text
                                            amod_pairs.append(k.text+' '+j.text+' '+token.text)
                                    mtch = re.search(re.escape(str1),re.escape(str2))
                                    if mtch is not None:
                                        amod_pairs.remove(str1)
                        if token.pos_ == 'VERB':
                            for j in token.lefts:
                                if j.dep_ == 'advmod' and j.pos_ == 'ADV':
                                    advmod_pairs.append(j.text+' '+token.text)
                                if j.dep_ == 'neg' and j.pos_ == 'ADV':
                                    neg_pairs.append(j.text+' '+token.text)
                            for j in token.rights:
                                if j.dep_ == 'advmod'and j.pos_ == 'ADV':
                                    advmod_pairs.append(token.text+' '+j.text)
                        if token.pos_ == 'ADJ':
                            for j,h in zip(token.rights,token.lefts):
                                if j.dep_ == 'xcomp' and h.dep_ != 'neg':
                                    for k in j.lefts:
                                        if k.dep_ == 'aux':
                                            xcomp_pairs.append(token.text+' '+k.text+' '+j.text)
                                elif j.dep_ == 'xcomp' and h.dep_ == 'neg':
                                    if k.dep_ == 'aux':
                                            neg_pairs.append(h.text +' '+token.text+' '+k.text+' '+j.text)


                pairs = list(set(amod_pairs+advmod_pairs+neg_pairs+xcomp_pairs))

                for i in range(len(pairs)):
                    if len(compound_pairs)!=0:
                        for comp in compound_pairs:
                            mtch = re.search(re.escape(comp[1]),re.escape(pairs[i]))
                            if mtch is not None:
                                pairs[i] = pairs[i].replace(mtch.group(),comp[0])


            aspect_terms.append(pairs)
        
        ndf[col] = aspect_terms

    ndf = ndf.iloc[:,:21]

    aspects = ndf.to_dict()
    df = pd.read_csv(OPINION_SURVEY_DIR)
    original_value = df.to_dict()


    return aspects, original_value

def summarized_aspect(filterVal, sentiment,aspect):
	#nlp = spacy.load('en_core_web_sm')


	df = pd.DataFrame(list(aspect.items()),columns=['Question','Aspect'])
	asp_dept = [findAc(filterVal,i) for i in df['Aspect']]

	df.insert(loc=2, column='Sentiment_Score', value=sentiment)

	df.insert(loc=2, column='Dept_aspect', value=asp_dept)

	for i in range(0, 21):
		df['Sentiments'] = df['Sentiment_Score'].apply(parse_values)

	nndf = df[df.astype(str)['Dept_aspect'] != '[]']

	for i in range(0, len(nndf['Question'])):
		nndf['Action_Plan'] = df.apply(lambda row: plan(row.Sentiments,str(row.Dept_aspect)), axis=1)   

	nndf = nndf.drop(['Aspect'], axis = 1)
	
	ndf_json = nndf.to_json(orient ='records')

	parsed = json.loads(ndf_json)

	return parsed





### Functions used in functions ####

def plan(sentiment,answer):
    if sentiment == 'POSITIVE':
        return "The students enjoyed the services of: " + answer
    elif sentiment == 'NEGATIVE':
        return "There is significant unsatisfaction in terms of "+ answer + " provide immediate intervention" 
    elif sentiment == 'NEUTRAL':
        return "There is no immediate action needed for " + answer +" but needs improvement"
    else:
        return "No Aspect and Comment to decide on"


def parse_values(x):
    if x>= 0.05 :
        return 'POSITIVE'
    elif x<= 0.03:
        return 'NEGATIVE'
    else:
        return 'NEUTRAL'
    
def parse_actionPlan(df):
    nlp = spacy.load('en_core_web_sm')
    tok = ''
    for ap in (df['Dept_aspect']):

        if len(str(ap)) != 0:
            doc = nlp(str(ap))

            for token in doc:
                if token.pos_ == 'NOUN':
                    tok += token.text +' ' 
                    #print(token.text)
                if token.pos == 'ADJ':
                    print(token)
                if token.pos == 'VERB':
                    print(token)

    answer =' '.join(unique_list(tok.split()))
    return answer

def pos_tagger(nltk_tag): 
    if nltk_tag.startswith('J'): 
        return wordnet.ADJ 
    elif nltk_tag.startswith('V'): 
        return wordnet.VERB 
    elif nltk_tag.startswith('N'): 
        return wordnet.NOUN 
    elif nltk_tag.startswith('R'): 
        return wordnet.ADV 
    else:           
        return None

def remove_stopWords(w): 
    stoplist = stopwords.words('english') + ['though']
    w = ' '.join(word for word in w.split() if word not in stoplist)
    return w

def findAc(filtr, word):
    r = re.compile('|'.join([r'\b%s\b' % w for w in filtr]), flags=re.I)
    results = r.findall(str(word))
    
    return results

def remove_parenthesis(value):
    res = re.sub(r"\([^()]*\)", "", value)
    return res

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def actionPlan(aspect,sentiment):
    nlp = spacy.load('en_core_web_sm')
    tok = ''
    for ap in aspect.values():

        if len(str(ap)) != 0:
            doc = nlp(str(ap))

            for token in doc:
                if token.pos_ == 'NOUN':
                    tok += token.text +' ' 
                    #print(token.text)
                if token.pos == 'ADJ':
                    print(token)
                if token.pos == 'VERB':
                    print(token)

    answer =' '.join(unique_list(tok.split()))

    if sentiment >= 0.05 and len(answer) != 0:
        return "The students enjoyed the services of: " + answer
    elif sentiment <= 0.03 and len(answer) != 0:
        return "There is significant unsatisfaction in terms of ["+ answer + "] provide immediate intervention" 
    elif sentiment < 0.05 and sentiment > 0.03 and len(answer) != 0:
        return "There is no immediate action needed for [" + answer +"] but needs improvement"
    else:
        return "No Aspect and Comment to decide on"
