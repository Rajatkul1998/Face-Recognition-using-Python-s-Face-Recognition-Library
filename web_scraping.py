# -*- coding: utf-8 -*-
"""web scraping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19oKqWgrv0pOqVcVj2yb9cA8Ujps_97g-
"""

#from selenium import webdriver
#from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import requests

!pip install selenium
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
#wd.get("https://www.webite-url.com")

url = 'https://in.linkedin.com/jobs/search?keywords=machine%20learning&location=Pune%2C%20Maharashtra%2C%20India&trk=homepage-jobseeker_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&currentJobId=1645890290'

#driver = webdriver.Chrome('/content/gdrive/My Drive/colab Notebooks/chromedriver.exe')
wd.get(url)

get_element  = wd.find_elements_by_css_selector("a[class='result-card__full-card-link']")
print(len(get_element))

li =[]
for i in range(0,52):
    li.append(get_element[i].get_attribute('href'))

print(li)

import time
li1=[]
for i in range(0,20):
    url = li[i]
    
    wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    #window_before = driver.window_handles[0]
   # time.sleep(3)
    wd.get(url)
   # window_after = driver.window_handles[1]
    ele =  wd.find_elements_by_css_selector("div[class = 'description__text description__text--rich']")
    for users in  ele:
        li1.append(users.text)
    wd.close()    


    
print(li1)



#print(li1[1])
#df = pd.DataFrame(li1) 
#df
with open('element.txt', 'w') as f:
    for item in li1:
        f.write("%s\n" % item)

filename = 'element.txt'
file = open(filename, 'rt')
text = file.read()
#print(text)
file.close()
#type(text)

words = text.split()

print(words[:200])

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

stop_words = set(stopwords.words('english')) 
filtered_sentence = [] 


for w in words: 
        if w not in stop_words: 
            filtered_sentence.append(w) 

print(filtered_sentence)

nltk.download('averaged_perceptron_tagger')

import nltk
tagged = nltk.pos_tag(filtered_sentence)
#print(tagged)

a=[]

for item in tagged:
    if item[:][1]=="NNP":
        a.append(item[0])
#print(a)

a = [key.capitalize() for key in a]
print(a)

#Use to import pandas
import pandas as pd
#Use to import the file into google Colab drive
from google.colab import files 
#Use to import io, which opens the file from the Colab drive
import io

# This will open a widget when run that will enable you to browse the files on your local storage drive.
uploaded = files.upload()

df = pd.read_excel('Book1.xlsx')
#print(df)
Custom_data=df.iloc[:,0].tolist()
#print(Custom_data)
#Capitalizing custom data
Custom_data = [word.capitalize() for word in Custom_data]
print(Custom_data)

import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

class EntityMatcher(object):
    name = "entity_matcher"

    def __init__(self, nlp, terms, label):
        patterns = [nlp.make_doc(text) for text in terms]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add(label, None, *patterns)

    def __call__(self, doc):
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            span = Span(doc, start, end, label=match_id)
            doc.ents = list(doc.ents) + [span]
        return doc

nlp = spacy.blank('en')
#terms = ("Tensorflow", "NLP", "MongoDB", "MySQL","NVIDIA","Machine Learning")
entity_matcher = EntityMatcher(nlp, Custom_data, "Technology")

nlp.add_pipe(entity_matcher)

#print(nlp.pipe_names)  # The components in the pipeline
doc = " "
for words in a:
  doc = doc +" "+words
doc1 = nlp(doc)
#print(doc1)
#doc = nlp("We provide technologies Machine ")
#print([(ent.text, ent.label_) for ent in doc1.ents])
l2 =[]
for ent in doc1.ents:
  l2.append(ent.text)
print(l2)
  
#for word in doc1.ents:
#  l=str(word)
#  s=list2.append(l)

#print(s)
#import itertools
#out = list(itertools.chain(*(doc1.ent)))

#print(out)

from  collections import Counter
counts = Counter(l2)
counts.most_common()
#print(counts)
df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
df.rename(columns={ df.columns[1]: "freq" }, inplace = True)
df.sort_values(by=["freq"],ascending=False)















