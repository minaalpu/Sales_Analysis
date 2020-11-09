# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 14:19:22 2020

@author: Mina Alpu
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 17:08:50 2020

@author: Mina Alpu
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

#Task 1: Merging 12 months data into single file

df = pd.read_csv(r'./Sales_Data/Sales_April_2019.csv')

files = [file for file in os.listdir('./Sales_Data')]

all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv(r'./Sales_Data/' + file)
    all_months_data = pd.concat([all_months_data, df])
    
all_months_data.to_csv('all_data.csv', index = False)

#Read in updated dataframe
all_data = pd.read_csv('all_data.csv')
print(all_data.head()) 


#Cleaning the data

na_df = all_data[all_data.isna().any(axis = 1)]
print(na_df.head()) 

all_data = all_data.dropna(how = 'all')
print(all_data.head())

#Find and delete 'Or' to fix the error

all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']

#Augment data with additional columns
#Task 2: Add Month and Sales column to find the month with the most sales

all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
print(all_data.head())


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])
print(all_data.head())

all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
print(all_data.head())

best = all_data.groupby('Month').sum()
print(best)

#Plot the answer
months = range(1,13)
plt.bar(months, best['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD')
plt.xlabel('Months')
plt.show()

#Task 3: Add City column to find the city with the highest number of sales

all_data['City'] = all_data['Purchase Address'].apply(lambda x: x.split(',')[1])
print(all_data.head())

best2 = all_data.groupby('City').sum()
print(best2)

#Plot the answer

cities = all_data['City'].unique()
plt.bar(cities, best2['Sales'])
plt.xticks(cities, rotation='vertical', size = 8)
plt.ylabel('Number of Sales')
plt.xlabel('City Names')
plt.show()

"""
Task 3: Find the time to display advertisements to maximize likelihood of 
customer's buying product.
"""

all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
print(all_data.head())

#Add column 'Hour' and 'Minute' to analyze better

all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
print(all_data.head())

hours = [hour for hour, df in all_data.groupby('Hour')]
plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hours')
plt.ylabel('Number of Orders')
plt.grid()
plt.show()

#Task 4: Find the products that are most often sold together

df = all_data[all_data['Order ID'].duplicated(keep = False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df = df[['Order ID', 'Grouped']].drop_duplicates()

print(df.head(100))

#Count the pairs of sold together
from itertools import combinations
from collections import Counter

count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))
    
print(count)

for key, value in count.most_common(10):
    print(key, value)
    
#Task 5: Find the product sold the most 

products_group = all_data.groupby('Product')
quantity_ordered = products_group.sum()['Quantity Ordered']
print(products_group.head())

products = [product for product, df in products_group]

plt.bar(products, quantity_ordered)
plt.xlabel('Product Name')
plt.ylabel('Quantity Ordered')
plt.xticks(products, rotation='vertical', size = 8)
plt.show()

prices = all_data.groupby('Product').mean()['Price Each']
print(prices)

#Adding second y axis
fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color = 'g')
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color = 'g')
ax2.set_ylabel('Prices', color = 'b')
ax1.set_xticklabels(products, rotation='vertical', size = 8)
plt.show()


    