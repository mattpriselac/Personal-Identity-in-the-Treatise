#Creating the Article and Citation Data structures
#and then populating the articles
import pandas as pd
import csv
from master_function_list import *

fileToPathDict = {}
fileToPaperDict = {}

class Citation:
    def __init__(self, paper, order_num, search_result):
        self.order = order_num
        self.paper = fileToPaperDict[paper]
        self.search_term = ""
        self.citationScores = []
        self.startPoint = 0
        self.endPoint = 0
        self.rawCitationText = search_result
        self.precedingText = ""
        self.trailingText = ""
        self.cleanedCitation = ""

    #this function pulls a given number of characters from before the citation starts up to the start
    #of the citation
    def FindPrecedingText(self, num_chars):
        #open the paper file
        paper_file = open(self.paper.path, "r")
        text_to_use = paper_file.readline()
        paper_file.close()
        #generate the buffer to get the appropriate slice in case it's around an edge of teh string
        buffer = self.startPoint - num_chars
        #set the proper text in the Citation
        if self.startPoint == 0:
            self.precedingText = ''
        elif buffer >= 0:
            self.precedingText = text_to_use[buffer:self.startPoint]
        elif buffer < 0:
            self.precedingText[:self.startPoint]

    #this function pulls a given number of characters from the end of the citation going forward
    def FindTrailingText(self, num_chars):
        #open the paper file
        paper_file = open(self.paper.path, "r")
        text_to_use = paper_file.readline()
        paper_file.close()
        #generate the buffer to get the appropriate slice in case it's around an edge of the string
        buffer = len(text_to_use) - (self.endPoint + num_chars)
        #set the proper text in the Citation
        if buffer == 0:
            self.trailingText = ""
        elif buffer > 0:
            self.trailingText = text_to_use[self.endPoint:(self.endPoint + num_chars)]
        elif buffer < 0:
            self.trailingText = text_to_use[self.endPoint:]

    #this function takes an integer as input and runs the previous two functions
    def PopulateSurroundingTexts(self, num_chars):
        self.FindPrecedingText(num_chars)
        self.FindTrailingText(num_chars)

    def calculateScore(self):
        self.citationScores = ultimateParser(self.cleanedCitation)
class Paper:
    def __init__(self, filename):
        self.name = filename
        self.path = fileToPathDict[filename]
        self.author = ''
        self.year = ''
        self.title = ''
        self.nortonCites = []
        self.sbnCites = []
        self.rawParenthesesCapture = []
        self.otherCites = []
        self.scoring_output = []

    def NortonSearch(self):
        citationCounter = 0 #citation counter to be used in numbering citations
        #create the citation search object
        #search pattern is
##        Capture Abstract cites with optional dash additions
##        Capture Appendix cites with optional dash additions
##        Capture Main body cites as follows:
##            Book. (capture both roman and arabic numeral versions)
##            Part. (capture both roman (capitalized and not) and arabic numerals)
##            Section (I left of the '.' here to be able to capture citations that are only Book.Part.Section with no paragraph citation)
##            optional .Paragraph(s with optional dash separator for a range of paragraphs
        nortonPattern = re.compile("""  T*Abs\d+
                                            ([-–—]\d{1,2}){0,1}|
                                        T*App\d+
                                            ([-–—]\d{1,2}){0,1}|
                                        ((I{1,3}|[123])\.)
                                        (([i]{1,3}|IV|[I]{1,3}|[1-4])\.)
                                        (\d{1,2})
                                        (\.[1-9]\d{0,2}
                                            ([-–—]\d{1,2}){0,1}
                                        ){0,1}""", re.X)
        #make the text of the paper accessible and generate the match objects
        paper_to_search = open(self.path, "r")
        text_to_search = paper_to_search.readline()
        paper_to_search.close()
        matchObjects = nortonPattern.finditer(text_to_search)
        #create a citation for each match object
        for match in matchObjects:
            citationCounter +=1
            citationObject = Citation(self.name, citationCounter, match.group())
            citationObject.startPoint = match.start()
            citationObject.endPoint = match.end()
            citationObject.search_term = match.re
            self.nortonCites.append(citationObject)
        if len(self.nortonCites) == 0:
            pass

    def SbnSearch(self):
        citationCounter = 0 #citation counter to be used in numbering citations
        #create the citation search object
##        the search pattern this time is to start with SBN
##        then cover page numbers (I got rid of 0 as a starting point because a file happened to have a weird SBN0 followed by a long string of numbers
##        next I have an optional dash and comma separator that can be repeated to capture the multiple pages and ranges that get cited
##        this will require some cleaning because sometimes you get a random 'i' following the comma
        sbnPattern = re.compile(""" (?<!I)
                                    (SBN)
                                    ([1-9]\d+|[xvi]+|[XVI]+)
                                    ([-–—,](\d+|[xvi]+|[XVI]+))*""", re.X)
        #make the text of the paper accessible and generate the match objects
        paper_to_search = open(self.path, "r")
        text_to_search = paper_to_search.readline()
        paper_to_search.close()
        matchObjects = sbnPattern.finditer(text_to_search)
        #create a citation for each match object
        for match in matchObjects:
            citationCounter +=1
            citationObject = Citation(self.name, citationCounter, match.group())
            citationObject.startPoint = match.start()
            citationObject.endPoint = match.end()
            citationObject.search_term = match.re
            self.sbnCites.append(citationObject)
        if len(self.sbnCites) == 0:
            pass

    def parenthesesCapture(self):
        citationCounter = 0 #citation counter to be used in numbering citations
        #create the citation search object
        #This idea behind this search string is to get anything in parentheses with the following structure:
            #First, it can optionally start with either a 'T', 'THN', 'Treatise', or 'Hume'
            #Second, there can be a run of some intervening text but not a close parens or any numbers
            #Third, we get a page number citation with an optional p, p., or pp.
            #fourth, we get up to a three digit page number or range of up to 3 digit page numbers in either
                #roman or arabic numerals
            #The only thing I haven't figured out how to capture yet is a brief comment that appears in a few
            #cases where the authro says something like, 'my emphases' or 'italics mine'. I think that might
            #require a different search with a more restrictive start to the parentheses
        pattern = re.compile('\((T|THN|Treatise|Hume)*([A-Z]|[a-z]|[,.])*(p*\.{0,1}(\d{1,3}|[xvi]+|[XVI]+)([-–—,](\d+|[xvi]{1,5}|[XVI]{1,5}))*)\)')
        #make the text of the paper accessible and generate the match objects
        paper_to_search = open(self.path, "r")
        text_to_search = paper_to_search.readline()
        paper_to_search.close()
        matchObjects = pattern.finditer(text_to_search)
        #create a citation for each match object
        for match in matchObjects:
            citationCounter +=1
            citationObject = Citation(self.name, citationCounter, match.group())
            citationObject.startPoint = match.start()
            citationObject.endPoint = match.end()
            citationObject.search_term = match.re
            self.rawParenthesesCapture.append(citationObject)
        if len(self.rawParenthesesCapture) == 0:
            pass

    #this method takes a search string and will return a list of citation objects that match the string.
    def otherSearch(self, search_term):
        citationCounter = 0 #citation counter to be used in numbering citations
        #create the citation search object
        pattern = re.compile(search_term)
        #make the text of the paper accessible and generate the match objects
        paper_to_search = open(self.path, "r")
        text_to_search = paper_to_search.readline()
        paper_to_search.close()
        matchObjects = pattern.finditer(text_to_search)
        #create a citation for each match object
        for match in matchObjects:
            citationCounter +=1
            citationObject = Citation(self.name, citationCounter, match.group())
            citationObject.startPoint = match.start()
            citationObject.endPoint = match.end()
            citationObject.search_term = match.re
            self.otherCites.append(citationObject)
        if len(self.otherCites) == 0:
            pass

#First, get a list of the downloaded files
#To do that we need all of the fiels in the list from PhilPapers
biblio_info = pd.read_csv("biblio_info.csv", index_col=False, header=0)
#Next we just filter out all the downloaded files
downloaded_files_list = biblio_info.loc[biblio_info['Downloaded?'].str.match("yes", case=False)==True]

#Next we can construct the fileToPathDictionary, this will let us access the PhilPapers
#by using their file name from the biblio_info source
path = 'search_texts/'

for index in downloaded_files_list.index:
    fileToPathDict[str(downloaded_files_list.loc[index]['Filename'])[:-4]] = path+str(downloaded_files_list.loc[index]['Filename'])[:-4]+'.txt'

#Next we can construct the fileToPaperDict that will allow us to access paper objects
#by using their file name

for index in downloaded_files_list.index:
    try:
        file =  str(downloaded_files_list.loc[index]['Filename'])[:-4]
        fileToPaperDict[file] = Paper(file)
        fileToPaperDict[file].author = downloaded_files_list.loc[index]['Author']
        fileToPaperDict[file].title = downloaded_files_list.loc[index]['Title of Work']
        fileToPaperDict[file].year = downloaded_files_list.loc[index]['Year']
    except Exception as error:
        print(index, 'generated the following error when trying:')
        print(error)
