# -*- coding: utf-8 -*
"""
Spyder Editor

Written by: Laura Pemberton

This programme is a submission for course GEOG5955 at the univerisity of Leeds 
for assignment 2.

The programme takes the data collected by the ELSA study on ageing, cleans this data
performs some data analysis, and then finally prints out the results. 


"""

# =============================================================================
# Import statements 
# =============================================================================
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.formula.api import ols
import time 
from matplotlib.backends.backend_pdf import PdfPages


#start timer 
start = time.process_time()

# =============================================================================
# Read in dataset
# =============================================================================
df = pd.read_csv("elsawave1.csv")  # df stands for dataframe. This is a type of 
# df pandas object  returns output in an object with rows and columns

# =============================================================================
# Data Cleaning
# =============================================================================

# create new data frame that will be edited. 
#remove all columns after position 500 
"""PLEASE EDIT THIS TO ONLY INCLUDED USED COLUMNS LAURA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
df1 = df.drop(df.iloc[:, 500:].columns, axis = 1)

#Create new age variable. This is the age of participant at time survey taken.
df1['age'] = 2011 - df['dhdobyr']

#remove all rows in columnn dhdobyr with values -9,-1 or -7
removed_rows = df1[ (df1['dhdobyr'] == -7) | (df1['dhdobyr'] == -1)].index
df1.drop(removed_rows, inplace = True)

#remove all rows in columnn psold with values -9,-1 or -7
removed_rows = df1[ (df1['psold'] == -7) | (df1['psold'] == -1)].index
df1.drop(removed_rows, inplace = True)
print(df1['psold'])

#remove all rows where any column contains the value -9 AKA 'refused to answer'. 
df1 = df1.replace(to_replace= -9, value=np.nan).dropna()
#remove all rows where any column contains the value -8 AKA 'Don't know'. 
df1 = df1.replace(to_replace= -8, value=np.nan).dropna()
#print(df1)

# =============================================================================
# PIE CHART https://chrisalbon.com/python/data_visualization/matplotlib_pie_chart/
# =============================================================================

#print (count(df1['dimar'].value_counts()))

# counts num of each instance of relationship status.
num_of_widowed = np.count_nonzero(df1['dimar'] == 6)
divorced = np.count_nonzero(df1['dimar'] == 5)
legally_separated = np.count_nonzero(df1['dimar'] == 4)
remarried = np.count_nonzero(df1['dimar'] == 3)
married = np.count_nonzero(df1['dimar'] == 2)
single = np.count_nonzero(df1['dimar'] == 1)

# Test
print(num_of_widowed, divorced, legally_separated, remarried, married, single)

# Test count of variables work as should add to 1667. 
print(num_of_widowed + divorced + legally_separated + remarried + married + single) 


age_values = [num_of_widowed, divorced, legally_separated, remarried, married, single]
labels = ['Widowed', 'Divorced', 'Legally Separated', 'Remarried', 'Married', 'Single']
colors = ["tan", "lemonchiffon", "orange", "peachpuff", "peru", "rosybrown", "lightcoral"]

#Create the pie chart
plt.pie(age_values, labels=labels, shadow=False, colors=colors,
        startangle=90, autopct='%1.1f%%')
plt.title('Visualisation of Relationship Status')
plt.axis('equal')
plt.tight_layout()
plt.figure()
plt.show(block=False)

# =============================================================================
# Contingency Table to show counts of men and women vs relationship status
# =============================================================================

sex_relationship = pd.crosstab(df1['disex'], df1['dimar'], margins = True, 
                               margins_name = "Total", rownames = ['Gender (1=M, 2=F)'],
                               colnames=['Relationship Status'])

#print(sex_relationship)

# =============================================================================
# Histogram of age variable with a KDE line.
# =============================================================================

# descriptive statistics of age variable
age_described = df1['age'].describe()
#print('descriptive statistics of age variable:', '\n', age_described)

# creates histogram of age variable
ax = df1['age'].hist(bins=30, color = 'LightSteelBlue', normed=True)
# plots a KDE line
df1['age'].plot(kind= 'kde', lw=2, color = 'Green', ax=ax)
plt.grid()
plt.title('Histogrm of age with kde')
plt.locator_params(nbins=5)
plt.xlabel('age (years)')
#plt.figure()
plt.show(block=False)

# =============================================================================
# compare actual age with age that people consider old. Program creates two
# histograms which are displayed side by side. A new dataframe variable is 
# created that just incldues the age and age considered old (psold) variables.
# =============================================================================

age_psold = df1[['age', 'psold']]
print(age_psold.head(20))


#Create histograms
ax_list = age_psold.hist(bins=40, figsize=(8,3), xrot=45, color = 'Green')
ax1, ax2 = ax_list[0]
ax1.set_title('Age (years)')
ax2.set_title('age considered old')
for ax in ax_list[0]:
    ax.grid()
    ax.locator_params(axis='x', nbins=10)
    ax.locator_params(axis='y', nbins=3)
   
    
# =============================================================================
# Linear Regression Analysis
# =============================================================================
linear_regression_model = ols("disex ~ dhdobyr + psold", df1, weight=df1.digran).fit()
model_summary = linear_regression_model.summary()
#print(model_summary)

# =============================================================================
# Write to excel file with pandas
# =============================================================================
df1.to_excel('cleaned_data_python.xlsx', sheet_name='sheet1', index=False)

# =============================================================================
# Save graphical plots to a pdf file
# =============================================================================
pdf = PdfPages('plots.pdf')
pdf.savefig(1)
pdf.savefig(2)
pdf.savefig(3)
pdf.close()


# =============================================================================
# Save textual command line outputs to a txt file. Program uses open function
# to create a new file object that the program can write to. The program will
# write each of the 3 pieces of analysis to a txt file.  
# =============================================================================
with open('output.txt', 'w') as f:
    print('ELSA Wave 1 data python output', file=f)
    print('\n', 'Logistic Regression Analysis:','\n', model_summary, file=f)
    print('\n', 'Contingency table(sex and relationship status):', '\n', sex_relationship, file=f)
    print('\n', 'Descriptive Statistics for age variable:', '\n', age_described, file=f)


# calculate time taken for programme to run - efficiency measure. This will just
# be printed to the CL. 
end = time.process_time()
print ("time completed in: "+ str(round(end-start, 3)))



"""NOTES""""""

#average participant considers old to be 'difference' years older than they are. 
difference = df1['age'] - df1['psold']
print(difference.head(20))
print(difference.mean())

print(df1['age'])


# =============================================================================
# Table
# =============================================================================

# =============================================================================
# # Count plot of drug use split by gender
# ax = sns.countplot(x='dimar', hue='disex', data=df1)
# # Change handle labels
# handles = ax.get_legend_handles_labels()[0]
# ax.legend(handles, ['Female', 'Male'], title='Gender')
# #Set labels, save and show plot
# plt.title('Number of pupils with reported drug use where 0=no and 1=yes')
# plt.xlabel('Ever used any drugs')
# plt.ylabel('Count')
# plt.savefig('../count_drug.jpg',format='jpg')
# plt.figure()
# =============================================================================


# =============================================================================
# Initial practicing test cases
# =============================================================================
#print(df) #test data imported correctly 
#print(df.head(10)) # Additional test case to pull out top 10 rows (use tail for bottom)
#print(df['psold'].head(10)) #Test to pull out specific column in dataset

#print(df['disib'].describe()) # Test case to show descriptive summary statistics 
# for field 'disib' (how many siblings)



wordcloud : https://www.geeksforgeeks.org/generating-word-cloud-python/
            https://www.datacamp.com/community/tutorials/wordcloud-python
            
content analysis: https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk


# =============================================================================
# #compare age with money in savings account
# removed_rows = df1[ (df1['iasava'] == -1) | (df1['iasava'] == -8) | (df1['iasava'] == -9)].index
# df1.drop(removed_rows, inplace = True)
# age_iasava = df1[['age', 'iasava']]
# print(age_iasava.head(20))
# 
# ax_list = age_iasava.hist(bins=40, figsize=(8,3), xrot=45)
# for ax in ax_list[0]:
#     ax.locator_params(axis='x', nbins=10)
#     ax.locator_params(axis='y', nbins=3)
# =============================================================================


df1.plot(kind='scatter', x='age', y='psold')
plt.title('Age against psold')
plt.axis([50,100,50,100])

"""
