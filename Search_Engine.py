#Search Engine 0.2 - sushi

import urllib2
import operator

def get_next_target(page): 
	start_link = page.find('<a href=')
	if start_link == -1:
		return None, 0
	start_quote = page.find('"',start_link)
	end_quote = page.find('"',start_quote+1)
	url = page[start_quote+1:end_quote]
	return url, end_quote;


def get_all_links(page):
	links=[]
	while True:
		url, endpos=get_next_target(page)
		if url:
			links.append(url)
			page= page[endpos:]
		else:
			break
	return links


def get_page(link):
	try:
		
		if link.find('mailto')!=-1:
			return ''
		req = urllib2.Request(link, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' })
		html = urllib2.urlopen(req).read()
		return html
	except (urllib2.URLError,urllib2.HTTPError,ValueError) as e:
				return ''

def split_string(source):
	splitlist= ",!-.;/?@ #"
	output=[]
	atsplit = True 
	for char in source:
		if char in splitlist:
			atsplit=True
		else:
			if atsplit:
				output.append(char)
				atsplit= False
			else:
				output[-1] = output[-1] +char
	return output

def add_to_index(index,keyword,url):  
    if keyword in index:
    	values=[]
    	values=lookup(index,keyword)
    	if url not in values:
    		values.append(url)
    else:
    	values=[]
    	values.append(url)
	index[keyword]=values

def add_page_to_index(index,url,content):	
    words=split_string(content)	
    for word in words:
        add_to_index(index,word,url)

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

	"""ranked_results=[]#contains ranks
	new_rr={}#contains the ranks pointing to url
	for e in rr:
		ranked_results=rr[e]
		new_rr[ranked_results]=e
	ranked_results.sort()
	output=[]
	i=0
	for e in ranked_results:
		output[i]=new_rr[e]
		i+=1
	return output"""

def union(p,q):
	for e in q:
		if e not in p:
			p.append(e)

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
            	if page in graph[node]:
            		newrank+=d*(ranks[node]/len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

def crawl_web(seed,max_depth):  
	tocrawl=[seed];
	crawled=[]
	sum_depth=[0]
	sum_each=0
	i=0
	index={}
	graph={}
	depth=0
	next_depth=[]
	while tocrawl and depth<= max_depth:
		page= tocrawl.pop()
		if page not in crawled:
			content= get_page(page)
			add_page_to_index(index,page,content)
			outlinks=get_all_links(content)
			graph[page]=outlinks
			union(next_depth,outlinks)
			crawled.append(page)
		if not tocrawl:
			tocrawl,next_depth= next_depth,[]
			depth=depth+1
		
	#ranks=compute_ranks(graph)
	return index,graph

#seed='http://xkcd.com/353'
#index= crawl_web(seed,1)
#print lookup(index,'contact')
