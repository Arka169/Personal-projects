#!/usr/bin/env python
# coding: utf-8

# In[1]:


#First we will be importing the libraries required for this project.
import nltk 
nltk.download('punkt')
from nltk import * 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import os
import csv
import pandas as pd
import glob
import requests
from bs4 import BeautifulSoup
import numpy as np


# Then I am loading the dataset using pandas and checking some info and structure of our dataset.

# In[2]:


df=pd.read_excel(r'C:\Users\Arkaj\Downloads\Input.xlsx')
df.columns


# In[3]:


df.head()


# In[4]:


df.shape


# In[5]:


df.iloc[65,1]


# In[6]:


link = df.iloc[65,1]


# In[7]:


#Using a request header to avoid any unwanted errors associated with data extraction.
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}


# In[8]:


source = requests.get(link, headers=headers).text
data = BeautifulSoup(source, 'lxml')
article = data.find('article')
title = article.h1.text
body =  article.find('div', class_='td-post-content').text
date = article.find('div', class_='td-module-meta-info').time.text


# In[9]:


title


# Now we will try to understand how our extracted data looks like and based on that we can perform the data cleaning.

# In[10]:


body


# In[11]:


footer = article.find('div', class_='td-post-content').pre.text 
footer


# In[12]:


body = body.replace(footer, '')


# In[13]:


new_body = body.replace('\n',' ')
new_body = new_body.replace('\xa0',' ')

new_body


# In[14]:


date


# In[15]:


def URL_data_extract(URL_link):
    #r = requests.get(url=urlLogin, params=params, headers=headers)
    headers = {'User-Agent': '98.0.4758.81'}
    page = requests.get(URL_link,headers=headers)
    soup = BeautifulSoup(page.content, 'html5lib')
    #print(soup)
    #print(soup.prettify())
    #print(r.content)
    soup.find_all('title', limit=1)
    title=soup.find_all("title")
    soup.find_all('p', limit=1)
    content=soup.find_all("p")
    p = soup.find_all("p")
    paragraphs = []
    for x in title:
        paragraphs.append(str(x))
    
    for x in p:
        paragraphs.append(str(x))

#     print(paragraphs)
    URL_data_extract.paragraph = ' '.join([str(elem) for elem in paragraphs])
    return URL_data_extract.paragraph


# In[16]:



def saving_file(ID):
    
    name='{}'.format(ID)+'.txt'
    with open(name , 'w+',encoding="utf-8") as file:
#     with open(name, 'w+') as file:
        file.write(URL_data_extract.paragraph)
    return file


# In[17]:


def word_extract(input_file):
    #file = open(input_file,newline='',encoding='latin-1')
    #result = input_file.read()
    word_extract.words = word_tokenize(input_file)
    
    #print(result)
    
    text = re.sub(r"[^a-zA-Z0-9]", " ", input_file.lower())
    words = text.split()
    special_char = '@_!#$%^&*()<>?/\|}{~:;.[]'
    word_extract.total_number_of_words=len(words)
    # using join() + generator to remove special characters
    out_list = [''.join(x for x in string if not x in special_char) for string in words]
    
    # print list without special characters
    #print('List after removal of special characters:\n', out_list)
    return out_list


# In[18]:


#master_dictionary
master_data=pd.read_csv(r'C:\Users\Arkaj\Downloads\Loughran-McDonald_MasterDictionary_1993-2021.csv')
#print(master_data)
positivedata=master_data[master_data.Positive>0]
# print(len(positivedata.Word))
negativedata=master_data[master_data.Negative>0]
# print(len(negativedata.Word))

pos=list(positivedata.Word)
neg=list(negativedata.Word)
for i in range(len(pos)):
     pos[i] = pos[i].lower()
        
for i in range(len(neg)):
     neg[i] = neg[i].lower()


# In[19]:


file_st=open(r"C:\Users\Arkaj\Downloads\StopWords_Generic.txt",newline='',encoding='latin-1')
input_data_stopwords=file_st.read()
stop_words_data=word_extract(input_data_stopwords)


# In[20]:


def Calculation(text_document):
    global Average_size_of_word
    global Personal_pronouns_count
    global Positive_Score
    global Negative_Score
    global polarity
    global subjectivity
    global Average_sentence_length
    global complex_count
    global syllable_count_per_word
    global percentage_of_complex_words
    global word_count_after_removing_stop_words
    global fog_index
    
    data_file=word_extract(text_document)
    extracted_list = [x for x in data_file if x not in stop_words_data]
    total_words_after_cleaning=len(extracted_list)

    sent_p=0
    sent_n=0
    for word_s in extracted_list:
        if word_s in pos:
            sent_p+=1
        elif word_s in neg:
            sent_n-=1
    #positive_score
    
    #negative_score
    sent_n=sent_n*(-1)
    
    Positive_Score=sent_p
    Negative_Score=sent_n
    
    #polarity_score
    polarity=(sent_p-sent_n)/((sent_p+sent_n)-0.000001)
    
    #subjectivity_score
    subjectivity=(sent_p+sent_n)/((total_words_after_cleaning)+0.000001)

    
    #total_sentences
    total_sentences=text_document.count(".")
    total_word=word_extract.total_number_of_words


    #average_number_of_words_sentence_length
    Average_sentence_length=total_word/total_sentences
  

    #complex_word_count
    def syllable_count(word):
       # word = word.lower()
        count = 0
        vowels = "aeiouy"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        return count
    #syllable_per_word
    complex_count=0
    syllable_count_per_word=[]
    for x in word_extract.words:
        k=syllable_count(x)
        syllable_count_per_word.append(k)
        if k>2:
            complex_count+=1
    
    syllable_count_per_word=sum(syllable_count_per_word)
   
    #(word_extract.words)
    #print(syllable_count_per_word)
    
    #percentage_of_complex_words
    percentage_of_complex_words=complex_count/total_word
   

    #Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
    fog_index=0.4*(Average_sentence_length+percentage_of_complex_words)
   

    #word_count_after_removing_stop_words
    stop_words_nltk=stopwords.words('english')
    word_count_after_removing_stop_words = len([x for x in data_file if x not in stop_words_nltk])
   
    #Personal_pronouns_count
    value=0
    #print(word_extract.words)
    for x in word_extract.words:
        pattern=r"(\b(I|we|my|us|ours)\b)"
        r1 = re.match(pattern, x)
        if r1:
            value+=1
          #  print(x)
   
    Personal_pronouns_count=value

    #Average_size_of_word
    size_of_word=0
    for x in data_file:
        size_of_word=size_of_word+len(x)
    

    Average_size_of_word=size_of_word/total_word
    


# In[21]:



column_names = ['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE',
       'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH',
       'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
       'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
       'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']

output_data_frame = pd.DataFrame(columns = column_names)



#URL_DATA= pd.DataFrame(data)
#URL_DATA.iloc[1]=data_2
#output_data_frame

for x in range(0,len(df)-1):
    URL_data_extract(df.URL[x])
    saving_file(df.URL_ID[x])
    Calculation(URL_data_extract.paragraph)
    data = {'URL_ID':df.URL_ID[x], 'URL':df.URL[x], 'POSITIVE SCORE':Positive_Score, 'NEGATIVE SCORE':Negative_Score, 'POLARITY SCORE':polarity,
       'SUBJECTIVITY SCORE':subjectivity, 'AVG SENTENCE LENGTH':Average_sentence_length,
       'PERCENTAGE OF COMPLEX WORDS':percentage_of_complex_words, 'FOG INDEX':fog_index,
       'AVG NUMBER OF WORDS PER SENTENCE':Average_sentence_length, 'COMPLEX WORD COUNT':complex_count, 'WORD COUNT':word_count_after_removing_stop_words,
       'SYLLABLE PER WORD':syllable_count_per_word, 'PERSONAL PRONOUNS':Personal_pronouns_count, 'AVG WORD LENGTH':Average_size_of_word,
       }
    output_data_frame = output_data_frame.append(data, ignore_index = True)


output_data_frame.to_csv('output_file.csv',index = False)


# In[ ]:





# In[ ]:




