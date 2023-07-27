# -*- coding: utf-8 -*-
"""ADS_searcher.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12mtO1Y2ELEvAVyXGm3jeMy4W_GpqpcuJ

## ADS Searcher Notebook

This notebook includes all of the necessary functions to take a list of names or institutions and find the expertise of that author or the authors in that institution based on publications in ADS. It has the possibility to detect what researchers are from a target institution by querying NASA ADS using the institution name, then pulling out the author name of papers whose first author is affiliated with the target institution. It also has the possibility to take an author's name directly and find their publications (with the option of limiting by year or institution). The code then focuses on the astronomical expertise of each author through selecting publications in astronomical journals (e.g. ApJ, MNRAS, SPIE) and marking each publication with a "dirty" or "clean" label based on if it was published by those journals.

This code represents an updated version of the one developed by Màire Volz (https://github.com/maireav/NASA-Internship) and utilizes many of the functions already created.

Before the code begins here are the things needed:
1. The supporting file **TextAnalysis.py**.
2. A file of ignorable "stop words" and its directory path: **stopwords.txt**.
3. Your own **NASA ADS API token**. This is a long string of characters generated by ADS that gives you acces to their API (https://ui.adsabs.harvard.edu/help/api/)
4. Either an input author/institution or an input csv file that has all authors/institutions you want to run.

Set up of this notebook:
- The steps of the process are listed out in each individual function (make sure to run these cells)
- At the end is the final for loop that you will input the csv file containing the input and output information (e.g. name of the person, institution,...) This function contains multiple different pathways (see example notebook) to retrieve the final expertise table, depending on the input provided.

### Step 1: Import statements and getting all necessary files
"""

import requests
from urllib.parse import urlencode, quote_plus
import numpy as np

#We designed the code to work with Pandas 1.5.3

import pandas as pd
print(pd. __version__)

#If the Pandas version differs from 1.5.3, run the following:
#pip install pandas==1.5.3 --user

token= 'Your own personal token from ADS API page' #Insert your API token

#edit the following string pointing to the directory where the stopwords.txt file is
path= 'your directory goes here'

stop_file= '\stopwords.txt'
directory = path+stop_file

#For the TextAnalysis File, please refer to M. Volze et al. 2023
import sys
sys.path.append(path)
import TextAnalysis as TA
import ExpertiseFinder_MSI as EF_MSI

"""### Step 2: ADS Search function (retrieving the ADS info)

The function "ads_search" and the secondary function "ads_search_aff" are defined below.

**"ads_search"** is the first aspect of finding the expertise for the inputted authors. It creates a query string composed of the inputs (shown in example notebook). The function then takes the query based on the name, institution, year or refereed property and enters it into ADS with the API token defined earlier. ADS returns information regarding each publication by each author inputted. This information is then sorted into a 7 column data frame containing the Outputs listed below. Each publication at this stage is a new row in the dataframe.

For the second function defined here **"ads_search_aff"**, the query is edited to read 'aff: University' instead of 'institution: University'. This function is implemented when an ads search for an institution returns no authors. This is important because there are instances in ADS where a university is listed as an affiliation instead of an institution, so this ensures no authors are missed when searching a specific program. Besides this query change, the rest of the function is the same.

#### Optional Inputs:
name, institution, year, and refereed property
#### Outputs:
Title, First author, bibcode, abstract, affiliation, publication date and keywords of each publication by this specific author (IN A DATA FRAME)
"""

def ads_search(name=None, institution=None, year= None, refereed= 'property:notrefereed OR property:refereed'):

#editing query input here

    if name:
        if institution:
            query = 'pos(institution:"{}",1), author:"^{}"'.format(institution, name)
            print(query)
        else:
            query = 'author:"^{}"'.format(name)
            print(query)

    else:
        query = 'pos(institution:"{}",1)'.format(institution)
        print(query)

    if year_range:
        if year_range=='general':
            startd= str(2000)
            endd= str(2023)
            years= '['+startd+' TO '+endd+']'
            query += ', pubdate:{}'.format(years)
            print(query)

        else:
            startd=str(int(year)-1)
            endd=str(int(year)+4)
            years='['+startd+' TO '+endd+']'
            query += ', pubdate:{}'.format(years) #input year in function
            print(query)


#making and sending query to ADS

    encoded_query = urlencode({
        "q": query,
        "fl": "title, first_author, bibcode, abstract, aff, pubdate, keyword",
        "fq": "database:astronomy,"+str(refereed),
        "rows": 300,
        "sort": "date desc"
    })
    results = requests.get(
        "https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query),
        headers={'Authorization': 'Bearer ' + token}
    )

    data = results.json()["response"]["docs"]

#extract results into each separate detail

    pdates = [d['pubdate'] for d in data]
    affiliations = [d['aff'][0] for d in data]
    bibcodes = [d['bibcode'] for d in data]
    f_auth = [d['first_author'] for d in data]
    keysw = [d.get('keyword', []) for d in data]
    titles = [d.get('title', '') for d in data]
    abstracts = [d.get('abstract', '') for d in data]

#define data frame

    df = pd.DataFrame({
        'Input Author': [name] * len(data),
        'Input Institution': [institution] * len(data),
        'First Author': f_auth,
        'Bibcode': bibcodes,
        'Title': titles,
        'Publication Date': pdates,
        'Keywords': keysw,
        'Affiliations': affiliations,
        'Abstract': abstracts,
        'Data Type': [[]]*len(data)
    })

    if name==None:
        df['Input Author']= f_auth


    return df




def ads_search_aff(name=None, institution=None, year= None, refereed= 'property:notrefereed OR property:refereed'):

#editing query input here
    if name:

        if institution:
            query = 'pos(aff:"{}",1), author:"^{}"'.format(institution, name)
            print(query)
        else:
            query = 'author:"^{}"'.format(name)
            print(query)

    else:
        query = 'pos(aff:"{}",1)'.format(institution)
        print(query)

    if year_range:
        if year_range=='general':
            startd= str(2000)
            endd= str(2023)
            years= '['+startd+' TO '+endd+']'
            query += ', pubdate:{}'.format(years)
            print(query)

        else:
            startd=str(int(year)-1)
            endd=str(int(year)+4)
            years='['+startd+' TO '+endd+']'
            query += ', pubdate:{}'.format(years) #input year in function
            print(query)


#making and sending query to ADS

    encoded_query = urlencode({
        "q": query,
        "fl": "title, first_author, bibcode, abstract, aff, pubdate, keyword",
        "fq": "database:astronomy,"+str(refereed),
        "rows": 300,
        "sort": "date desc"
    })
    results = requests.get(
        "https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query),
        headers={'Authorization': 'Bearer ' + token}
    )

    data = results.json()["response"]["docs"]

#extract results into each separate detail

    pdates = [d['pubdate'] for d in data]
    affiliations = [d['aff'][0] for d in data]
    bibcodes = [d['bibcode'] for d in data]
    f_auth = [d['first_author'] for d in data]
    keysw = [d.get('keyword', []) for d in data]
    titles = [d.get('title', '') for d in data]
    abstracts = [d.get('abstract', '') for d in data]

#define data frame

    df = pd.DataFrame({
        'Input Author': [name] * len(data),
        'Input Institution': [institution] * len(data),
        'First Author': f_auth,
        'Bibcode': bibcodes,
        'Title': titles,
        'Publication Date': pdates,
        'Keywords': keysw,
        'Affiliations': affiliations,
        'Abstract': abstracts,
        'Data Type': [[]]*len(data)
    })

    if name==None:
        df['Input Author']= f_auth


    return df

"""### Step 3: Defining data type (dirty vs clean)
This here will label the data as "clean" vs "dirty" based on if it is published in one of the chosen astronomical journals, if the listed first author matches the input author and if the listed affiliations includes the input institution. If any of these constraints are not met then the publication is marked as "Dirty".

This is important because in this program we specifically want authors that are published in astronomical journals and we want accurate information regarding where they have worked and what level of information each author knows regarding their specific expertises. By ensuring they are the first author and at the assumed institution, we can trust the data given. We can also decide how to value the publication depending on the journal it is published in (dirty vs clean).


The input is a dataframe with the defined columns as created in the ads_search function.
"""

def data_type(df):

    journals = ['ApJ', 'MNRAS', 'AJ', 'Nature', 'Science', 'PASP', 'AAS', 'arXiv', 'SPIE', 'A&A']

    for index, row in df.iterrows():

        flag= 0

# Journal check
        if any(journal in row['Bibcode'] for journal in journals):
            data_type_label = 'Clean'
        else:
            flag= flag+1

#Author check
        if row['First Author'].lower() == row['Input Author'].lower():
            data_type_label = 'Clean'
        else:
            flag=flag+2

# Inst check
        if institution and institution in row['Affiliations']:
            data_type_label = 'Clean'
        elif not institution:
            data_type_label = 'Clean'
        else:
            flag=flag+4

# Update the 'Data Type' column
        if flag==0:
            data_type_label = 'Clean'
        else:
            data_type_label = 'Dirty'

        df.at[index, 'Data Type'] = data_type_label

    print(flag) #this lets the user know what aspect of the data made it 'dirty'

#flag= 1 just the journal aspect is dirty,
#flag= 2 just the author aspect is dirty,
#flag=3 the author and journal are dirty,
#flag=4 just the inst is dirty, etc.

    return df

"""### Step 4: Merge the publications for individual authors into one row
Before this step the dataframe will have each publication by each author in separate rows, here we want to combine the publications by author, i.e if an author publishes 5 times then all 5 publications are in one row with that author.

Input here is the dataframe with the columns defined in the ads_search function as well as the data type column
"""

def merge(df):

    df['Publication Date']= df['Publication Date'].astype(str)
    df['Abstract']= df['Abstract'].astype(str)
    df['Keywords'] = df['Keywords'].apply(lambda keywords: ', '.join(keywords) if keywords else '')
    df['Title'] = df['Title'].apply(lambda titles: ', '.join(titles) if titles else '')

# if the dataframe is missing any information it is labeled as "None"

    df.fillna('None', inplace=True)

    merged= df.groupby('Input Author').aggregate({'Input Institution':', '.join, 'First Author':', '.join, 'Bibcode':', '.join,
                                                 'Title':', '.join,'Publication Date':', '.join, 'Keywords':', '.join,
                                                 'Affiliations':', '.join,'Abstract':', '.join, 'Data Type':', '.join}).reset_index()

    return merged

"""### Step 5: Defining the n_grams for each publication  
This final step is to define the N_grams for each paper, meaning the top words, bigrams and trigrams found (using the TextAnalysis file)
"""

def n_grams(df, directorypath): #directory path should lead to TextAnalysis.py
    top10Dict = {'Top 10 Words':[],
                 'Top 10 Bigrams':[],
                 'Top 10 Trigrams':[]}

    for i in df.values:
        abstracts = i[8]

        top10words = TA.topwords(abstracts, directorypath)
        top10bigrams = TA.topbigrams(abstracts, directorypath)
        top10trigrams = TA.toptrigrams(abstracts, directorypath)

        top10Dict['Top 10 Words'].append(top10words)
        top10Dict['Top 10 Bigrams'].append(top10bigrams)
        top10Dict['Top 10 Trigrams'].append(top10trigrams)

    top10Df = df
    top10Df['Top 10 Words'] = top10Dict['Top 10 Words']
    top10Df['Top 10 Bigrams'] = top10Dict['Top 10 Bigrams']
    top10Df['Top 10 Trigrams'] = top10Dict['Top 10 Trigrams']

    top10Df = top10Df[['Input Author', 'Input Institution', 'First Author', 'Bibcode', 'Title', 'Publication Date',
             'Keywords', 'Affiliations', 'Abstract', 'Top 10 Words', 'Top 10 Bigrams', 'Top 10 Trigrams', 'Data Type']]

    return top10Df

"""### Step 6: Putting it all together
This function (final) takes in one file that has all of the authors or institutions you want to test and completes each step on each author or individual institution.

**Important to note** you need to edit the 'final' function statement below based on what your personal file contains- see below in comments the details of what you may need to replace. Reference the examples notebook to see possible ways to use these functions.
"""

def final(file):
    dataframe= pd.read_csv(file)

    #replace inside the brackets below with the arguments you want to use
    institutions= dataframe['Institution Name']
    names= dataframe['Author'] #format must be Last, First
    start_years= dataframe['Fellowship Year']
    referee= 'property:notrefereed OR property:refereed'

    final_df= pd.DataFrame()
    count= 0

    #starting for loop to go through the input csv file
    for i in np.arange(len(dataframe)):

        #edit for what your argument will be in step 2- comment out the aspects of the dataframe that will not be included in the function
        inst= institutions[i]
        name= names[i]
        year= start_years[i]

        #inputting into step 2
        data1= ads_search(name= name, institution= inst, year=year, refereed=referee)

        #if the dataframe is empty and there is an author inputted into the function
        if name and data1.empty:

            #if the year is an inputted argument then drop the institutution from the search
            if year:
                data1= ads_search(name=name, year=year, refereed=referee)

                #if the dataframe is still empty for just the name and year then search for a larger year range (2000 to 2023)
                if data1.empty:
                      data1= ads_search(name=name, year='general', refereed=referee)

            #no year input then just search  name without institution
            else:
                data1= ads_search(name, refereed=referee)

        #if there is no name input
        if name==None and data1.empty:
            if year:
                data1= ads_search_aff(institution= inst, year=year, refereed=referee)
            else:
                data1= ads_search_aff(institution= inst, refereed=referee)

        data1['Input Institution']=inst

        data2= data_type(data1)
        data3= merge(data2)
        data4= n_grams(data3, directory)

        final_df= final_df.append(data4, ignore_index= True)
        count+=1
        print(str(count)+' iterations done')

    return final_df

"""## Examples!

Now that you understand how the functions all work and the necessary steps to find the desired expertise of an author or authors or a list of authors expertises from a desired institution, you can view the examples notebook located in this folder to see the possibilities of the function and the ways the different inputs change the output!
"""