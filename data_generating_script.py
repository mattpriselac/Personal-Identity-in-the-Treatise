#Write the script to output a CSV
import os
import pandas as pd
import csv
from treatise_reference_data import *
from master_function_list import *
from Article_and_Citation_Classes import *


#now let's loop through through the papers and conduct searches for Norton, SBN and Parens
for paper in fileToPaperDict.keys():
    try:
        fileToPaperDict[paper].NortonSearch()
        fileToPaperDict[paper].SbnSearch()
        fileToPaperDict[paper].parenthesesCapture()
    except Exception as error:
        print(fileToPaperDict[paper].name, 'generated the following error when trying to search:')
        print(error)

print('done searching papers')

#now let's collect all the papers with norton cites
papers_w_nortons = []
for paper in fileToPaperDict.keys():
    try:
        if len(fileToPaperDict[paper].nortonCites)>0:
            print(paper)
            papers_w_nortons.append(paper)
    except Exception as error:
        print(error)
print("there are", str(len(papers_w_nortons)), "papers with norton cites")
#next we can collect all the norton citations themselves:
all_norton_cites = []
for paper in papers_w_nortons:
    for cite in fileToPaperDict[paper].nortonCites:
        all_norton_cites.append(cite)
print("There are a total of", len(all_norton_cites), "norton citations")

#last, we can clean the norton citations and then process them to get their scores
for cite in all_norton_cites:
    try:
        cite.cleanedCitation = cite.rawCitationText
        cite.calculateScore()
    except Exception as error:
        print(cite.paper.name, 'generated the following error')
        print(error)

#let's collect and process the SBN citations now
#first, gather the papers with SBN citations
papers_w_sbns = []
for paper in fileToPaperDict.keys():
    try:
        if len(fileToPaperDict[paper].sbnCites)>0:
            print(paper)
            papers_w_sbns.append(paper)
    except Exception as error:
        print(error)
print(str(len(papers_w_sbns)), "papers had SBN citations")

#second, clean the SBN citations to make them scorable
for paper in papers_w_sbns:
    for cite in fileToPaperDict[paper].sbnCites:
        cite.cleanedCitation = cite.rawCitationText[3:]

#third, let's calculate their scores
for paper in papers_w_sbns:
    for cite in fileToPaperDict[paper].sbnCites:
        try:
            cite.calculateScore()
        except Exception as error:
            print(error)

#let's put all the sbn cites in a single list and count it
all_sbn_cites = []
for paper in papers_w_sbns:
    for cite in fileToPaperDict[paper].sbnCites:
        all_sbn_cites.append(cite)
print("There are", str(len(all_sbn_cites)), "SBN citations")

#Now we can start collecting, cleaning, and scoring easy Parens citations
#first, gather the papers w parens
papers_w_parens = []
for paper in fileToPaperDict.keys():
    try:
        if len(fileToPaperDict[paper].rawParenthesesCapture)>0:
            print(paper)
            papers_w_parens.append(paper)
    except Exception as error:
        print(error)
print("there are", str(len(papers_w_parens)), 'papers with parens citations')

#second, we have to clean those to get just the ones with T at the start
num_check = re.compile('(\d{1,3})+([-–—,](\d{1,3}))*')
for paper in papers_w_parens:
    for cite in fileToPaperDict[paper].rawParenthesesCapture:
        if cite.rawCitationText[1] == "T":
            #print('found a T cite in', paper)
            if num_check.search(cite.rawCitationText) != None:
                #print('found a T cite with a page num in', paper)
                pageNum = num_check.search(cite.rawCitationText).group()
                cite.cleanedCitation = pageNum

#third, we can gather the papers with clean easy parens citations
clean_parens_papers = []
for paper in papers_w_parens:
    for cite in fileToPaperDict[paper].rawParenthesesCapture:
        if cite.cleanedCitation != "":
            if not paper in clean_parens_papers:
                clean_parens_papers.append(paper)
print("there are", str(len(clean_parens_papers)), "papers with easy parens")

#fourth, we can gather the cites from the cleand parens papers
clean_parens_cites = []
for paper in clean_parens_papers:
    for cite in fileToPaperDict[paper].rawParenthesesCapture:
        if cite.cleanedCitation != "":
            try:
                clean_parens_cites.append(cite)
            except Exception as error:
                print(paper, cite.cleanedCitation, 'generated an error:')
                print('error')
print("there are", str(len(clean_parens_cites)), "clean parens cites")

#fifth, we can calculate the scores from the clean parens
for cite in clean_parens_cites:
    cite.calculateScore()

num_nortons = len(all_norton_cites)
num_sbn = len(all_sbn_cites)
num_parens = len(clean_parens_cites)

total_cites = num_nortons+num_sbn+num_parens
print('There are', str(total_cites), 'total cites')
master_citation_list = []
for cite in all_norton_cites:
    master_citation_list.append(cite)
for cite in all_sbn_cites:
    master_citation_list.append(cite)
for cite in clean_parens_cites:
    master_citation_list.append(cite)

print("we've made a master list of", str(len(master_citation_list)), 'cites')

#finally, let's write it all to the csv file
import csv
output_file = open('data_out/citation_data.csv','w')
writing_object = csv.writer(output_file)

header = ['filename', 'title', 'author', 'year', 'citation order', 'citation text', 'citation scoring']
writing_object.writerow(header)
for citation in master_citation_list:
    output = []
    output.append(citation.paper.name)
    output.append(citation.paper.title)
    output.append(citation.paper.author)
    output.append(citation.paper.year)
    output.append(citation.order)
    output.append(citation.cleanedCitation)
    output.append(citation.citationScores)
    writing_object.writerow(output)
output_file.close()
print('done')
