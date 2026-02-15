#!/usr/bin/env python
# coding: utf-8

# In[7]:


"""
Project: In Silico Evaluation of Myxobacterial Secondary Metabolites for Toxicity and Anticancer Properties
Authors: Wesal Hammo, Nathaniel Santiago, Elizabeth Jarvis 
Mentor: Professor Joseph Hibdon 
Institution: Northeastern Illinois University 
Summer Research 2025

Description: 
This script processes predicted IC50 (inhibitory concentration) results for Myxococcus macrosporus.
It analyzes all cell lines and natural products to identify the most effective compounds and the cancers 
they target. The script then generates histograms of IC50 distributions for the top compounds 
to visualize their effectiveness across different cell lines. It then identifies the most negative IC50 values 
and matches their SMILES strings with the Myxobacterial natural products data to determine the names of the products 
through their SMILES. The final output is a clean table showing the most potent compounds, 
their molecular formulas, IC50 values, cell lines, and tissue sites.


"""


# In[8]:


import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('macrosporuscancerresults.csv')

# Save cell line names and site names for labeling plots
cell_line_names = df.iloc[:, 1]   # Column 1 = cell line names
site_names = df.iloc[:, -3]       # Third-to-last column = site names

# Drop columns that are not numeric: first column, cell line, last three columns
df_cleaned = df.drop(columns=[df.columns[0], df.columns[1], df.columns[-1], df.columns[-2], df.columns[-3]])

# Convert remaining columns to numeric
numeric_df = df_cleaned.apply(pd.to_numeric, errors='coerce')

# Find top 5 rows with lowest minimum values
row_min_values = numeric_df.min(axis=1)          
top5_rows = row_min_values.nsmallest(5).index    

# Plot histograms for each top row
for i, idx in enumerate(top5_rows, start=1):
    row_data = numeric_df.loc[idx].dropna()      # Drop NaN values from the row
    cell_line = cell_line_names[idx]
    site = site_names[idx]

    # Create a new figure for each histogram
    plt.figure(figsize=(8, 4))
    plt.hist(row_data, bins=15, edgecolor='black', color='darkred')
    plt.title(f'IC50 Distribution — {cell_line} ({site})')
    plt.xlabel('IC50 or log(IC50) Value')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    
    # Show the histogram
    plt.show()
    
    # Close the figure so the next one is independent
    plt.close()

# Combine all top row values for later use
combined_values = []  # All numeric values from top 5 rows
value_info = []

for idx in top5_rows:
    row_data = numeric_df.loc[idx].dropna()
    cell_line = cell_line_names[idx]
    site = site_names[idx]

    for val in row_data:
        combined_values.append(val)
        value_info.append((val, cell_line, site))


# In[9]:


#  Read the raw CSV file without headers to capture the very first row (SMILES strings)
raw_df = pd.read_csv('macrosporuscancerresults.csv', header=None)

# Save the first row which contains SMILES strings for the compounds
smiles_row = raw_df.iloc[0, :]

# Read the CSV again, skipping the first row
df = pd.read_csv('macrosporuscancerresults.csv', skiprows=1)

# Extract cell line names and site names for labeling later
cell_line_names = df.iloc[:, 1]      
site_names = df.iloc[:, -3]          

# Clean the dataframe. drop non-numeric columns:
df_cleaned = df.drop(columns=[df.columns[0], df.columns[1], df.columns[-1], df.columns[-2], df.columns[-3]])

# Convert all remaining columns to numeric; non-numeric values become NaN
numeric_df = df_cleaned.apply(pd.to_numeric, errors='coerce')

#  Find top 5 rows with the lowest minimum values and compute the minimum value in each row
row_min_values = numeric_df.min(axis=1)

# Get the indices of the 5 smallest minimum values
top5_rows = row_min_values.nsmallest(5).index

# Initialize a list to store tuples of (IC50 value, cell line, site, SMILES)
value_info = []

for idx in top5_rows:
    # Get the numeric values in the row
    row_data = numeric_df.loc[idx].dropna()
    cell_line = cell_line_names[idx]
    site = site_names[idx]

    # Iterate over each column/value pair in the row
    for col, val in row_data.items():
        # Get the SMILES string corresponding to this column
        smiles = smiles_row[df.columns.get_loc(col)] if col in df.columns else "N/A"
        
        # Append all info as a tuple
        value_info.append((val, cell_line, site, smiles))

#  Convert collected info into a DataFrame
value_df = pd.DataFrame(value_info, columns=['Value', 'Cell Line', 'Site', 'SMILES'])

#  Sort and select top 10 most negative IC50 values
top_10_negative = value_df.sort_values(by='Value', ascending=True).head(10)

# Print the top 10 results
print("Top 10 Most Negative IC50 Values:")
print(top_10_negative.to_string(index=False))


# In[11]:


# Load the myxobacterial natural products data
myxo_df = pd.read_csv('myxobacterial_natural_products.csv')

# Clean the SMILES strings in the top 10 negative IC50s
top_10_negative['SMILES_clean'] = (
    top_10_negative['SMILES']
    .astype(str)         
    .str.strip()          
    .str.replace(r'^IC50_', '', regex=True)  
)

#Clean the SMILES strings in the myxobacterial database
myxo_df['compound_smiles_clean'] = (
    myxo_df['compound_smiles']
    .astype(str)          
    .str.strip()          
)

# Merge the top IC50 results with the myxobacterial database
merged_df = pd.merge(
    top_10_negative,
    myxo_df[['compound_smiles_clean', 'compound_name', 'compound_molecular_formula']],
    left_on='SMILES_clean',          # Match cleaned SMILES from top IC50 results
    right_on='compound_smiles_clean',# Match cleaned SMILES from database
    how='left'                      
)

# Select relevant columns for final output
final_df = merged_df[[
    'compound_name',
    'compound_molecular_formula',
    'Value',        # IC50 value
    'Cell Line',    # Cell line tested
    'Site'          # Site/tissue type
]]

# Display the top 10 most potent compounds
print("Top 10 Most Potent Compounds:")
print(final_df.to_string(index=False))


# In[ ]:




