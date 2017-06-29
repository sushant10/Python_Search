#Search

import urllib2
import operator
import json

def lookup(index, keyword):  
    if keyword in index:
        return index[keyword]
    return None

def lookup_ranked(index,keyword,ranks):
	results=lookup(index,keyword)
	if results== None:
		return "no results :("
	rr={}
	for e in results:
		rr[e]= ranks[e]
	values= sorted(rr.items(),key=operator.itemgetter(1),reverse=True)
	output=[]
	i=0
	for e in values:
		output.append(e[0])
		i+=1
	return output

#open index and ranks

with open("index.txt") as indexfile:
    index = json.load(indexfile)
with open("ranks.txt") as ranksfile:
    ranks = json.load(ranksfile)
 
print "\n"
#search loop
while True:
	search_term= raw_input("Enter Search:")
	results= lookup_ranked(index,search_term,ranks)
	i=1
	for result in results:
		print "{}. {} \n".format(i,result)
		i+=1
	choice= raw_input("Y/N to keep going :")
	if choice=='n' or choice=='N':
		break;	
