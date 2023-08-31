# NASA_Internship
Code from my NASA internship Summer 2023 on Expanding Diversity in the NASA Astrophysics Panel

**Purpose:** 
This repository of functions and files was built in response to NASA’s call to expand and improve the diversity of its pool of potential proposal reviewers. To expand the diversity, this code provides a method of finding experts in specific matters no matter their institution, and it is used specifically throughout my internship to provide information on MSIs (Minority Serving Institutions) and the published authors located at these programs. 

**What the code does:** 
The main project was the production of the notebook "ads_searcher.ipynb". This is the file that access ADS API and searches for the specifics that the user inputs. The way "ads_searcher" works is that it takes in an argument by the user- which could be a variety of things such as a singular author, an institution, an author and institution, or a list of multiple authors and institutions. It then, using the user's ADS API Access Token (can be found here: https://ui.adsabs.harvard.edu/help/api/), searches the input into ADS. It retrieves important information including 'First Author', 'Bibcode', 'Title', 'Publication Date', 'Keywords', 'Affiliations', and 'Abstract'. Then- through a series of functions in the notebook, it cleans up the final datasheet to include the necessary information and to allow the user to easily (manually) determine the expertise of each author ADS returned.  


**Current files:**
This repo contains files to assist in finding the expertise of specific authors (or to find authors from specific institutions) through their NASA ADS publications. The following files are located here: 
- ads_searcher.ipynb: Python file that has all of the functions used to find the expertises of the authors and produce an organized data frame with each row being an individual author and columns: 'Input Author','Input Institution', 'First Author', 'Bibcode', 'Title', 'Publication Date', 'Keywords', 'Affiliations', 'Abstract', 'Data Type'
- TextAnalysis.py: Python file that has all the functions in order to determine the top words, bigrams and trigrams in each publication.
- stopwords.txt: Text file that has a list of the stop words for language processing. A user may provide their own or use the file in this repository.
- search_examples.ipynb: A notebook that contains 3 different examples of how to use the ads_searcher functions with different input cases. These input cases include just an author, just an institution, and a csv file of 3 authors with their corresponding institutions.

  **Required Input:**
- Personal ADS API Access Token: https://ui.adsabs.harvard.edu/help/api/
- Directory paths to the stopwords.txt and TextAnalysis.py files
- Input arguments of the users choice (can be an input author or an input .csv file)

**Possible Uses:**
This program can be used in multiple ways (as shown in the search examples notebook) 
Possible Inputs include: 
- An input file that contains an authors name
- An input file that contains a list of multiple authors names
- An input file that contains a list of authors and their institutions
- An input file that contains a list of institutions and a specific year range
- A singular name or institution (year as an optional argument as well)
These inputs would all return a datasheet of the information mentioned earlier for each publication found from authors listed or authors at the institution(s).

This code represents an updated version of the one developed by Màire Volz (https://github.com/maireav/NASA-Internship) and utilizes many of the functions already created. A huge thanks to Maire for the beginning of the code development as well as the TextAnalysis file and stopwords file used, also to my internship mentor Antonino Cucchiara for the constant assistance and guidance throughout this process. 
