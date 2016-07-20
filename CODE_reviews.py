import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import lxml.html
import operator
import plotly.plotly as py
#py.sign_in('username', 'api_key')
import plotly.graph_objs as go
import numpy
import pylab as pl
import enchant
import plotly.tools as tls


#tls.set_credentials_file(username='username', api_key='api-key')

d=enchant.Dict("en_US")


#tree = ET.parse('books.negative.review.xml')
#tree =
tree = lxml.html.parse('electronics.negative.review.xml')#Electronics department only for now
root = tree.getroot()

numreviews = tree.xpath('count(//review)')
print 'num of reviews = ',numreviews

#_rating=[]
#for rating in root.iter('rating'):
#	_rating.append(float(rating.text))	
#print _rating

ignore = ['the', 'as', 'or', 'they', 'if', 'so', 'just', 'you', 'but', 'i', 'to', 
'and', 'a', 'an', 'we', 'me', 'for', 'are', 'on', 'of', 'this', 'that', 'is', 'it', 
'in', 'my', 'their', 'when', 'from', 'which', 'who', 'after', 'about', 'your', 'its',
'with', 'be', 'at', 'then', 'said', 'think', 'thought', 'why', 'came', 'one', 'two', 
'three','there', 'them', 'thing', 'through', 'thing', 'something', 'where', 'what',
'know']
#words to be deleted
#will be refined


wordcounts=dict()
wordcounts1=dict()
wordcounts2=dict()
wordcounts3=dict()
wordcounts4=dict()
wordcounts5=dict()
wordcounts6=dict()
wordcounts7=dict()

products=dict()

reasons=dict()

service=['bad service', 'poor service', 'worst service','bad customer service', 'poor customer service', 'worst customer service']
quality=['low quality', 'bad quality', 'worst quality', 'cheap design', 'waste of money', 'bad product', 'worst product', 'cheaply made','quality is bad', 'quality is low', 'not good', 'worse than expected']
price=['too expensive', 'overpriced', 'very expensive', 'high cost', 'costly', 'costs too much']
defect=['defective product', 'defect', 'defective', 'damaged','arrived broken']
wrong=['wrong product', 'wrong device'] 
warranty =['no warranty']
#will be more refined and more categories will be added


for product in root.iter('product_name'):
	product=product.text.rstrip()
	product=product.lstrip()
	products[product]=products.get(product,0)+1

numproducts=len(products)
print 'num of products = ', numproducts
		


		

for review_text in root.iter('review_text'):
	review=review_text.text.rstrip()
	review=review.lstrip()
	review=review.lower()
	
	if any(w in review for w in service):
		reasons['service']=reasons.get('service',0)+1
	if any(w in review for w in quality):
		reasons['quality']=reasons.get('quality',0)+1
	if any(w in review for w in price):
		reasons['price']=reasons.get('price',0)+1
	if any(w in review for w in defect):
		reasons['defect']=reasons.get('defect',0)+1
	if any(w in review for w in wrong):
		reasons['wrong']=reasons.get('wrong',0)+1
	if any(w in review for w in warranty):
		reasons['warranty']=reasons.get('warranty',0)+1
	
	reviewwords=review.split()
	resultwords=[word for word in reviewwords if word not in ignore]
	resultreview=''.join(resultwords)
	
	for word in resultwords: 
		#if not(d.check(word)): print 'misspelled = ', word, 'replace by = ', d.suggest(word)[0] #d.store_replacement(word, d.suggest(word)[0])
		word.replace( "(","")
		word.replace(")" ,"")
		word.replace("." ,"")
		word.replace("," ,"")
		word.replace("?" ,"")
		word.replace( "!","")
		word.replace( "'","")
		
		if word in ignore: continue
		elif (word.isalpha() and d.check(word)):
			if (word.endswith(('s', 'ies', 'ed', 'ied', 'ing'))): 
				if (word[0:len(word)-4] in resultwords): wordcounts[word[0:(len(word)-4)]]=wordcounts.get(word[0:(len(word)-4)],0)+1
				elif (word[0:len(word)-5] in resultwords): wordcounts[word[0:(len(word)-5)]]=wordcounts.get(word[0:(len(word)-5)],0)+1
				elif (word[0:len(word)-4]+'y' in resultwords): wordcounts[(word[0:(len(word)-4)]+'y')]=wordcounts.get((word[0:(len(word)-4)]+'y'),0)+1
				elif (word[0:len(word)-3] in resultwords): wordcounts[word[0:(len(word)-3)]]=wordcounts.get(word[0:(len(word)-3)],0)+1
				elif (word[0:len(word)-2] in resultwords): wordcounts[word[0:(len(word)-4)]]=wordcounts.get(word[0:(len(word)-2)],0)+1
			else: wordcounts[word]=wordcounts.get(word,0)+1


for key,value in wordcounts.items():
	if (len(key)<3 or value<20 or not(d.check(key))): 
		del wordcounts[key]

print 'num words = ',len(wordcounts)

num=dict()
for k in wordcounts.values():
	num[k]=num.get(k,0)+1
	
	
print reasons
X=numpy.arange(len(reasons))
pl.bar(X, reasons.values(), align='center', width=0.5)
pl.xticks(X, reasons.keys())
ymax=max(reasons.values())+1
pl.ylim(0, ymax)
pl.title('Negative review reason by category')
pl.show()		
	
#keysorted_num = sorted(num.items(), key=operator.itemgetter(0))
#print keysorted_num	

for key,value in wordcounts.items():
	if value<25: wordcounts1[key]=value	
	elif value<30: wordcounts2[key]=value
	elif value<38: wordcounts3[key]=value	
	elif value<49: wordcounts4[key]=value
	elif value<69: wordcounts5[key]=value
	elif value<129: wordcounts6[key]=value
	else: wordcounts7[key]=value

#valuesorted_wordcounts = sorted(wordcounts.items(), key=operator.itemgetter(1))
#print valuesorted_wordcounts	

#keysorted_wordcounts = sorted(wordcounts.items(), key=operator.itemgetter(0))
#print keysorted_wordcounts	

print 'dictionary length =', len(wordcounts)


import matplotlib
from pylab import *

val = y=wordcounts7.values()    # the bar lengths
pos = arange(len(wordcounts7))+.5    # the bar centers on the y axis
figure(7)
barh(pos,val, align='center')
yticks(pos, (wordcounts7.keys()))
xlabel('Frequency')
title('Word Frequency')
grid(True)
show()	

val = y=wordcounts6.values()    # the bar lengths
pos = arange(len(wordcounts6))+.5    # the bar centers on the y axis
figure(6)
barh(pos,val, align='center')
yticks(pos, (wordcounts6.keys()))
xlabel('Frequency')
title('Word Frequency')
grid(True)
show()

val = y=wordcounts5.values()    # the bar lengths
pos = arange(len(wordcounts5))+.5    # the bar centers on the y axis
figure(5)
barh(pos,val, align='center')
yticks(pos, (wordcounts5.keys()))
xlabel('Frequency')
title('Word Frequency')
grid(True)
show()

val = y=wordcounts4.values()    # the bar lengths
pos = arange(len(wordcounts4))+.5    # the bar centers on the y axis
figure(4)
barh(pos,val, align='center')
yticks(pos, (wordcounts4.keys()))
xlabel('Frequency')
title('Word Frequency')
grid(True)
show()	

val = y=wordcounts3.values()    # the bar lengths
pos = arange(len(wordcounts3))+.5    # the bar centers on the y axis
figure(3)
barh(pos,val, align='center')
yticks(pos, (wordcounts3.keys()))
xlabel('Frequency')
title('Word Frequency')
grid(True)
show()			

val = y=wordcounts2.values()    # the bar lengths
pos = arange(len(wordcounts2))+.5    # the bar centers on the y axis
figure(2)
barh(pos,val, align='center')
yticks(pos, (wordcounts2.keys()))
xlabel('Frequency')
title('Word Frequency')
grid(True)
show()	

val = y=wordcounts1.values()    # the bar lengths
pos = arange(len(wordcounts1))+.5    # the bar centers on the y axis
figure(1)
barh(pos,val, align='center')
yticks(pos, (wordcounts1.keys()))
xlabel('Frequency')
title('Word Frequency')
grid(True)
show()	
