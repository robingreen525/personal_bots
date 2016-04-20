#import libraries needed
import sys
import os
import argparse
from Bio import Entrez


def search(query):
    Entrez.email = 'greenro6@uw.edu'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='200',
                            retmode='xml', 
                            term=query)
    results = Entrez.read(handle)
    return results


#r= search ('niche construction')
#print(r)

mypubs=search('(Robin Green[Author]) AND (Shou[Author] OR Hegg[Author]) ')

#print mypubs.keys()
f= mypubs[ u'IdList'] # pubmed IDs
print f

for id in f:
	 handle = Entrez.esummary(db="pubmed", id=id)
	 print handle
	 record = Entrez.read(handle)
	 pub_dict=record[0]
	 print pub_dict.keys()
	 for key in pub_dict.keys():
	 	print key+':'
	 	print pub_dict[key]