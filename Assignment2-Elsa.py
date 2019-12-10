# -*- coding: utf-8 -*
"""
Spyder Editor

Written by: Laura Pemberton

This programme is a submission for course GEOG5955 at the univerisity of Leeds 
for assignment 2.

The programme takes the data collected by the ELSA study on ageing, cleans this data
performs some data analysis, and then finally prints out the results. 

This program provides visualisation for a number of the variables in the data set. 
This includes: a newly calculated age variable, gender, marital status, age 
considered old, and finally responses to a question regarding participants general health. 

Finally the program writes the results of the data to csv file, writes the plots to a pdf
and writes the textual output to a txt file. 


"""

# =============================================================================
# Import statements 
# =============================================================================
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time 
import seaborn as sns
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

#Create new age variable. This is the age of participant at time survey taken.
df['age'] = 2011 - df['dhdobyr']
#print(df1)

# create new data frame with columns that will be used in analysis.
df1 = df[['dhdobyr', 'psold', 'hegenh', 'dimar', 'disex', 'age']]
#print (df1)

#remove all rows in columnn dhdobyr with values -1 or -7
removed_rows = df1[ (df1['dhdobyr'] == -7) | (df1['dhdobyr'] == -1)].index
df1.drop(removed_rows, inplace = True)

#remove all rows in columnn psold with values -9,-1 or -7
removed_rows = df1[ (df1['psold'] == -7) | (df1['psold'] == -1)].index
df1.drop(removed_rows, inplace = True)
#print(df1['psold']) # test case

#remove all rows in columnn hegenh with -1
removed_rows = df1[ (df1['hegenh'] == -1)].index
df1.drop(removed_rows, inplace = True)


# Create a function that removes all rows with a value of -8 or -9. 
def remove_missing_values(df1):
    nan_values = [-8, -9]
    df1.replace(nan_values, np.nan, inplace=True)
   
# Run function to remove all values     
remove_missing_values(df1)
#print(df1)

# =============================================================================
# PIE CHART 
# First this section creates a count for all of the instances of each marital
# status in the dataset. 
# This is then tested
# Next 3 list are created that are used for the pie chart, the first is counts,
# the second is the labels and the third is the colours used for the pie chart. 
# The program then plots the pie chart using the 3 lists that have been created.
# =============================================================================

# counts num of each instance of relationship status.
num_of_widowed = np.count_nonzero(df1['dimar'] == 6)
divorced = np.count_nonzero(df1['dimar'] == 5)
legally_separated = np.count_nonzero(df1['dimar'] == 4)
remarried = np.count_nonzero(df1['dimar'] == 3)
married = np.count_nonzero(df1['dimar'] == 2)
single = np.count_nonzero(df1['dimar'] == 1)

# Test
#print(num_of_widowed, divorced, legally_separated, remarried, married, single)

# Test count of variables work as should add to 1667. 
#print(num_of_widowed + divorced + legally_separated + remarried + married + single) 


age_values = [num_of_widowed, divorced, legally_separated, remarried, married, single]
labels = ['Widowed', 'Divorced', 'Legally Separated', 'Remarried', 'Married', 'Single']
colors = ["tan", "lemonchiffon", "orange", "peachpuff", "peru", "rosybrown", "lightcoral"]

#Create the pie chart
plt.pie(age_values, labels=labels, shadow=False, colors=colors,
        startangle=90, autopct='%1.1f%%')
plt.title('Visualisation of Relationship Status')
plt.tight_layout() # ensure the plot fits in the figure 
plt.figure()

# =============================================================================
# Contingency Table to show counts of men and women vs relationship status
# this also includes totals for each of the columns and rows. 
# this output is then printed to the txt file produced by this program. 
# =============================================================================

sex_relationship = pd.crosstab(df1['disex'], df1['dimar'], margins = True, 
                               margins_name = "Total", rownames = ['Gender (1=M, 2=F)'],
                               colnames=['Relationship Status'])

#print(sex_relationship)

# =============================================================================
# Histogram of age variable with a KDE line.
# First this section just provides a summary of the age variable with .describe()
# Next this section creates a new histogram using the age vaiable. Then creates 
# a KDE line which it maps ontop of the histogram. 
# =============================================================================

# descriptive statistics of age variable
age_described = df1['age'].describe()
#print('descriptive statistics of age variable:', '\n', age_described)

# creates histogram of age variable
ax = df1['age'].hist(bins=15, color = 'peru', normed=True)
# plots a KDE line
df1['age'].plot(kind= 'kde', lw=1, color = 'black', ax=ax)
#Plot histogram onto a grid 
plt.title('Histogram of age with kde')

# define number of bins to plot data
plt.locator_params(nbins=10)
plt.xlabel('age (years)')
plt.figure()
plt.show(block=False)

#print(df1['disex'].describe())


# =============================================================================
# Count plot 'how is your health in general' (hegenh) split by gender.
# x variable is participant responses to a likert scale.
# countplot is used as a means to measure categorical data and disagregates 
# the response by another category, in this case gender. 
# =============================================================================
ax3 = sns.countplot(x='hegenh', hue='disex', data=df1, palette='pastel')
# Change handle labels
handles = ax3.get_legend_handles_labels()[0]
ax3.legend(handles, ['Male', 'Female'], title='Gender')
#Set labels, save and show plot
plt.title('How is your health in general')
plt.xlabel('Responses (1=Very good, 2=Good, 3=Fair, 4=Bad, 5=Very bad')
plt.ylabel('Count')
plt.show(block=False)

# =============================================================================
# compare actual age with age that people consider old. Program creates two
# histograms which are displayed side by side. A new dataframe variable is 
# created that just incldues the age and age considered old (psold) variables.
# =============================================================================

age_psold = df1[['age', 'psold']]
#print(age_psold.head(20)) # test case


#Create histograms
ax_list = age_psold.hist(bins=40, figsize=(8,3), xrot=45, color = 'peru')
ax1, ax2 = ax_list[0]
ax1.set_title('Age (years)')
ax2.set_title('age considered old')
ax1.set_ylabel('Count')
ax2.set_ylabel('Count')
for ax in ax_list[0]:
    ax.grid()
    ax.locator_params(axis='x', nbins=10)
    ax.locator_params(axis='y', nbins=5)


# =============================================================================
# Write to excel file with pandas
# =============================================================================
df1.to_excel('cleaned_data_python.xlsx', sheet_name='sheet1', index=False)

# =============================================================================
# Program creates a new pdf document and writes to this each time its run.
# =============================================================================
pdf = PdfPages('plots.pdf')
pdf.savefig(1)
pdf.savefig(2)
pdf.savefig(3)
pdf.savefig(4)
pdf.close()

# =============================================================================
# Save textual command line outputs to a txt file. Program uses open function
# to create a new file object that the program can write to. The program will
# write each of the 3 pieces of analysis to a txt file.  
# =============================================================================
with open('output.txt', 'w') as f:
    print('ELSA Wave 1 data python output', file=f) 
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
# Initial practicing test cases
# =============================================================================
#print(df) #test data imported correctly 
#print(df.head(10)) # Additional test case to pull out top 10 rows (use tail for bottom)
#print(df['psold'].head(10)) #Test to pull out specific column in dataset

#print(df['disib'].describe()) # Test case to show descriptive summary statistics 
# for field 'disib' (how many siblings)



# =============================================================================
# Linear Regression Analysis
# =============================================================================
linear_regression_model = ols("disex ~ dhdobyr + psold", df1, weight=df1.digran).fit()
model_summary = linear_regression_model.summary()
#print(model_summary)

print('\n', 'Logistic Regression Analysis:','\n', model_summary, file=f)

# =============================================================================
# Data cleaning start point
# =============================================================================

#remove all columns after position 500 
#df1 = df.drop(df.iloc[:, 500:].columns, axis = 1)
# Cleaning data - this method allowed the program to run faster but not very sustainable. 
df1=   df1.replace(to_replace= -9, value=np.nan).dropna()
df1 =  df1.replace(to_replace= -8, value=np.nan).dropna()


# =============================================================================
# Scatter
# =============================================================================

df1.plot(kind='scatter', x='age', y='psold')
plt.title('Age against psold')
plt.axis([50,100,50,100])

"""
