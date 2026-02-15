#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Project: In Silico Evaluation of Myxobacterial Secondary Metabolites for Toxicity and Anticancer Properties
Authors: Wesal Hammo, Nathaniel Santiago, Elizabeth Jarvis 
Mentor: Professor Joseph Hibdon 
Institution: Northeastern Illinois University 
Summer Research 2025

Description:
This script processes predicted toxicity probabilities for Stigmatella aurantica 
across 31 endpoints. It identifies and isolates the 25 human-specific 
endpoints of interest, computes average toxicity probabilities, and 
produces histogram visualizations to assess distribution trends and 
comparative variability.

"""


# In[10]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# In[11]:


# Load toxicity prediction results
df = pd.read_csv("Stigtoxresults.csv")
# Define the subset of columns relevant to this analysis.
#   - "SMILES" (chemical structure representation)
#   - 25 human-specific toxicity endpoints, including:
#       • Nuclear receptor response endpoints (NR-*)
#       • Stress response pathways (SR-*)
#       • Genomic toxicity indicators (e.g., mutagenesis, carcinogenesis)
#       • Dose-response and organ-specific toxicity measures
columns_to_keep = [
    "SMILES",
    "Probability_Nuclear Response_NR-AR",
    "Probability_Nuclear Response_NR-AR-LBD",
    "Probability_Nuclear Response_NR-AhR",
    "Probability_Nuclear Response_NR-Aromatase",
    "Probability_Nuclear Response_NR-ER",
    "Probability_Nuclear Response_NR-ER-LBD",
    "Probability_Nuclear Response_NR-PPAR-gamma",
    "Probability_Nuclear Response_NR-GR",
    "Probability_Nuclear Response_NR-TR",
    "Probability_Stress Response_SR-ARE",
    "Probability_Stress Response_SR-ATAD5",
    "Probability_Stress Response_SR-HSE",
    "Probability_Stress Response_SR-MMP",
    "Probability_Stress Response_SR-p53",
    "Probability_Genomic_AMES_Mutagenesis",
    "Probability_Genomic_Carcinogenesis",
    "Probability_Genomic_Micronucleus",
    "PredictionsDose Response_Maximum_Tolerated_Dose",
    "Probability_Organic_Skin_Sensitisation",
    "Probability_Organic_hERG_I_Inhibitor",
    "Probability_Organic_hERG_II_Inhibitor",
    "Probability_Organic_Liver_Injury_I",
    "Probability_Organic_Liver_Injury_II",
    "Probability_Organic_Eye_Irritation",
    "Probability_Organic_Eye_Corrosion",
    "Probability_Organic_Respiratory_Disease"
]


# In[4]:


new_df = df[columns_to_keep]


# In[5]:


new_df.to_csv("Stigtoxresults_filtered.csv", index=False)


# In[6]:


filtered_df = pd.read_csv("Stig_Auran_tox_filtered.csv")


# In[12]:


# Check if the dataframe has at least 12 columns
if filtered_df.shape[1] < 12:
    # If there are fewer than 12 columns, raise an error with a message
    raise ValueError("The input file must have at least 12 columns.")

# Create a new column 'Average_4_to_12' which is the average of columns 4 to 12 (0-indexed: 3 to 11)
filtered_df['Average_4_to_12'] = filtered_df.iloc[:, 3:12].mean(axis=1)

# Plot a histogram of the 'Average_4_to_12' values
plt.hist(filtered_df['Average_4_to_12'], bins=30)  # 30 bins for the histogram
plt.xlabel('Average Probability of Compound Nuclear Toxicity')  # X-axis label
plt.ylabel('Frequency')  # Y-axis label
plt.title('Histogram of Average Values of Nuclear Toxicity Probability(Stigmatella Aurantiaca)')  # Plot title
plt.show()  # Display the plot


# In[33]:


if filtered_df.shape[1] < 17:
    raise ValueError("The input file must have at least 17 columns.")

filtered_df['Average_13_to_17'] = filtered_df.iloc[:, 12:17].mean(axis=1)

plt.hist(filtered_df['Average_13_to_17'], bins=30)
plt.xlabel('Average Probability of Compound Stress Response')
plt.ylabel('Frequency')
plt.title('Histogram of Average Values of Compound Stress Response(Stigmatella Aurantiaca)')
plt.show()


# In[34]:


if filtered_df.shape[1] < 20:
    raise ValueError("The input file must have at least 20 columns.")

filtered_df['Average_18_to_20'] = filtered_df.iloc[:, 17:20].mean(axis=1)

plt.hist(filtered_df['Average_18_to_20'], bins=30)
plt.xlabel('Average Probability of Compound Genomic Toxicity')
plt.ylabel('Frequency')
plt.title('Histogram of Average Values of Compound Genomic Toxicity Probability(Stigmatella Aurantiaca)')
plt.show()


# In[35]:


if filtered_df.shape[1] < 29:
    raise ValueError("The input file must have at least 29 columns.")

filtered_df['Average_22_to_29'] = filtered_df.iloc[:, 21:29].mean(axis=1)

plt.hist(filtered_df['Average_22_to_29'], bins=30)
plt.xlabel('Average Probability of Compound Organic Toxicity')
plt.ylabel('Frequency')
plt.title('Histogram of Average Values of Compound Organic Toxicity Probability(Stigmatella Aurantiaca)')
plt.show()


# In[ ]:




