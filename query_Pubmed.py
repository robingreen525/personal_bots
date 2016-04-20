#import libraries needed
import sys
import os
import argparse
from Bio import Entrez
import smtplib

def search(query):
    Entrez.email = 'greenro6@uw.edu'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='200',
                            retmode='xml', 
                            term=query)
    results = Entrez.read(handle)
    return results



mypubs=search('(Robin Green[Author]) AND (Shou[Author] OR Hegg[Author]) ')

#print mypubs.keys()
f= mypubs[ u'IdList'] # pubmed IDs

c=open('all_abstracts.txt','w')

### records of terms already searched for

dir='/home/robin/Github_Repos/personal_bots/search_records'
remove_cmd='rm '+dir+'/temp*'

os.system(remove_cmd)
searches=os.listdir('/home/robin/Github_Repos/personal_bots/search_records')
for search in searches:
	search_copy=search
	search=dir+'/'+search
	a=open(search,'r')
	ll=a.readlines()
	i=0
	#print ll
	#print searches
	ids=[]
	add_ids=[]
	for line in ll:
		i+=1
		#print line
		if i==1: # is the pubmed search term of interest
			print 'search pubmed for: '+ line
			key=line
		
		else:
			line=line.rstrip('\n')
			ids.append(line)
			#print line
	#now query search term and see if there is anything new
	key=str(key)
	#print key
	
	handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='200',
                            retmode='xml', 
                            term=key)
        
	results = Entrez.read(handle)
	#print results
	
	f= results[ u'IdList'] # pubmed IDs
	for id in f:
		if id not in ids:
			add_ids.append(id)
	
	#now create new file
	search=search_copy
	newfile=dir+'/temp_'+search
	newfile=str(newfile)
	
	#print newfile
	
	b=open(newfile,'w')
	#b.write(key)
	final=[]
	final.append(key)
	## add information to this new file
	for id in ids:
		if id != '':
			final.append(id)
	for id in add_ids:
		if id != '':
			final.append(id)
		
	for item in final:
		item=item.rstrip('\n')
		#print item
		b.write(item)
		b.write('\n')
	a.close()
	b.close()
	
	if ids != add_ids: # if there was a publication found not previously in my record, update my record!
		search=dir+'/'+search
		os.remove(search)
		os.rename(newfile,search)
		
	# the next thing I want to do is create a file with all the relevant publication information
	i=0
	for id in final:
	 i+=1
	 if (i >1 ):
	 	 handle = Entrez.esummary(db="pubmed", id=id)
	 	 print handle
	 	 record = Entrez.read(handle)
	 	 pub_dict=record[0]
	 	 print pub_dict.keys()
	 	 handle = Entrez.efetch(db='pubmed', id=id, retmode='text', rettype='abstract')
	 	 abstract=handle.read()
	 	 print pub_dict['DOI']
	 	 print pub_dict['Title']
	 	 print abstract
	 	 c.write('******************')
	 	 c.write(pub_dict['DOI'])
	 	 c.write(pub_dict['Title'])
	 	 c.write(abstract)
	 	 c.write('******************')

	 	 '''
	 	 for key in pub_dict.keys():
	 	 	 print key+':'
	 	 	 print pub_dict[key]
	 	 '''


c.close()