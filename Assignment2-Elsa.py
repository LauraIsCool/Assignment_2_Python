# -*- coding: utf-8 -*
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.formula.api import ols
import seaborn as sns
import time 

start = time.process_time()

# =============================================================================
# Read in dataset
# =============================================================================
df = pd.read_csv("elsawave1.csv")  # df stands for dataframe. This is a type of 
# df pandas object  returns output in an object with rows and columns


# =============================================================================
# Initial practicing test cases
# =============================================================================
#print(df) #test data imported correctly 
#print(df.head(10)) # Additional test case to pull out top 10 rows (use tail for bottom)
#print(df['psold'].head(10)) #Test to pull out specific column in dataset

#print(df['disib'].describe()) # Test case to show descriptive summary statistics 
# for field 'disib' (how many siblings)


# =============================================================================
# Data Cleaning
# =============================================================================

#remove all columns after position 100
df1 = df.drop(df.iloc[:, 200:].columns, axis = 1)

#Create new age column. This is the age of participant at time survey taken.
df1['age'] = 2011 - df['dhdobyr']

#remove all rows in columnn dhdobyr with values -9,-1 or -7
removed_rows = df1[ (df1['dhdobyr'] == -7) | (df1['dhdobyr'] == -1)].index
df1.drop(removed_rows, inplace = True)

#remove all rows where any column contains the value -9 AKA missing data. 
#df1 = df1.replace(to_replace= -9, value=np.nan).dropna()

print(df1)

# =============================================================================
# Histogram of age variable
# =============================================================================

print(df1['age'].describe())

#hisogram of age with KDE (kernel density estimation)
ax = df1['age'].hist(bins=30, color = 'LightSteelBlue', normed=True)
df1['age'].plot(kind= 'kde', lw=2, color = 'Green', ax=ax)
plt.grid()
plt.title('Histogrm of age with kde')
plt.locator_params(nbins=5)
plt.xlabel('age (years)')

#compare age with how many cigs smoked on weekdays
df1['heskb'] = df1['heskb'].replace([-1], 0) # -1 = N/A so replaced with 0. 
age_heskb = df1[['age', 'heskb']]
print(age_heskb.head(20))

ax_list = age_heskb.hist(bins=40, figsize=(8,3), xrot=45, color = 'Green')
ax1, ax2 = ax_list[0]
ax1.set_title('Age (years)')
ax2.set_title('Cigarettes smoked on weekdays')
for ax in ax_list[0]:
    ax.grid()
    ax.locator_params(axis='x', nbins=10)
    ax.locator_params(axis='y', nbins=3)

#compare age with money in savings account
removed_rows = df1[ (df1['iasava'] == -1) | (df1['iasava'] == -8) | (df1['iasava'] == -9)].index
df1.drop(removed_rows, inplace = True)
age_iasava = df1[['age', 'iasava']]
print(age_iasava.head(20))

ax_list = age_iasava.hist(bins=40, figsize=(8,3), xrot=45)
for i in ax_list[0]:
    i.locator_params(axis='x', nbins=10)
    i.locator_params(axis='y', nbins=3)
    

# =============================================================================
# Write to excel file with pandas
# =============================================================================
df1.to_excel('cleaned_data_python.xlsx', sheet_name='sheet1', index=False)


end = time.process_time()
print ("time completed in: "+ str(round(end-start, 3)))

"""NOTES""""""
# =============================================================================
# Linear Regression Analysis
# =============================================================================

#linear_regression_model = ols("disex ~ dhdobyr + psold", df, weight=df.digran).fit()
#print(linear_regression_model.summary())


# =============================================================================
# Table
# =============================================================================

# Count plot of drug use split by gender
ax = sns.countplot(x='dimar', hue='disex', data=df1)
# Change handle labels
handles = ax.get_legend_handles_labels()[0]
ax.legend(handles, ['Female', 'Male'], title='Gender')
#Set labels, save and show plot
plt.title('Number of pupils with reported drug use where 0=no and 1=yes')
plt.xlabel('Ever used any drugs')
plt.ylabel('Count')
plt.savefig('../count_drug.jpg',format='jpg')
plt.figure()


wordcloud : https://www.geeksforgeeks.org/generating-word-cloud-python/

content analysis: https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk
"""
