# NASA_Internship
Code from my NASA internship Summer 2023 

Purpose: 
This repository of functions and files was built in response to NASA’s call to expand and improve the diversity of its pool of potential proposal reviewers. To expand the diversity, this code provides a method of finding experts in specific matters no matter their institution, and it is used specifically throughout my internship to provide information on MSIs (Minority Serving Institutions) and the published authors located at these programs. 


This repo contains files to assist in finding the expertise of specific authors (or to find authors from specific institutions) through their NASA ADS publications. The following files are located here: 
- ads_searcher.py: Python file that has all of the functions used to find the expertises of the authors and produce an organized data frame with each row being an individual author and columns: 'Input Author','Input Institution', 'First Author', 'Bibcode', 'Title', 'Publication Date', 'Keywords', 'Affiliations', 'Abstract', 'Data Type'
- TextAnalysis.py: Python file that has all the functions in order to determine the top words, bigrams and trigrams in each publication.
- stopwords.txt: Text file that has a list of the stop words for language processing. A user may provide their own or use the file in this repository.
- search_examples.ipynb: A notebook that contains 3 different examples of how to use the ads_searcher functions with different input cases. These input cases include just an author, just an institution, and a csv file of 3 authors with their corresponding institutions. 

This code represents an updated version of the one developed by Màire Volz (https://github.com/maireav/NASA-Internship) and utilizes many of the functions already created. A huge thanks to Maire for the beginning of the code development as well as the TextAnalysis file and stopwords file used, also to my internship mentor Antonino Cucchiara for the constant assistance and guidance throughout this process. 
