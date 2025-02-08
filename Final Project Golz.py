# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 21:37:02 2024

@author: golzm
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('FluData.csv')

df = df.rename(columns={'Age Group':'Age_Group', 'A (H1)':'A_H1', 
                        'A (H3)':'A_H3', 'A (H1N1)pdm09':'A_H1N1_pdm09',
                        'B (Victoria Lineage)':'B_Victoria_Lineage',
                        'B (Yamagata Lineage)':'B_Yamagata_Lineage',
                        'B (Lineage Unspecified)':'B_Unspecified_Lineage',
                        'H3N2v':'A_H3N2v'})

df["Age_Group"] = df["Age_Group"].str.strip(r'(yr | +)')
df["Age_Group"] = df['Age_Group'].astype("category")
df["Season"] = df["Season"].str.replace(r'-\d\d$', '', regex=True)
df["Season"] = pd.to_datetime(df["Season"])
df["Season"] = df["Season"].dt.to_period('Y')

df["A_Subtype_not_Available"] = df.loc[:,["A (Unable to Subtype)",
                                          "A (Subtyping not Performed)"]].sum(axis=1)

df = df.drop(["A (Unable to Subtype)", "A (Subtyping not Performed)"], axis=1)

cols = df.columns.tolist()
cols = cols[0:5] + cols[8:] + cols[5:8] 

df = df[cols]

def iqr(arg):
    q1 = arg.quantile(q=0.25, axis=0, numeric_only=True, method='single')
    q3 = arg.quantile(q=0.75, axis=0, numeric_only=True, method='single')
    range = q3-q1
    return range

summary_stats = pd.DataFrame({'Mean':df.mean(axis=0, numeric_only=True),
         'Median':df.median(axis=0, numeric_only=True),
         'Max':df.max(axis=0, numeric_only=True), 
         'Min':df.min(axis=0, numeric_only=True),
         'StDev':df.std(axis=0, numeric_only=True),
         'Q1':df.quantile(q=0.25, axis=0, numeric_only=True, method='single'),
         'Q2':df.quantile(q=0.75, axis=0, numeric_only=True, method='single'),
         'IQR':iqr(df)})

season_group = df.groupby('Season').sum(numeric_only=True)
grouped_ages = df.groupby('Age_Group').sum(numeric_only=True)

seasons_a = season_group.drop(["B_Victoria_Lineage", "B_Yamagata_Lineage", 
                               "B_Unspecified_Lineage"], axis=1)

seasons_b = season_group.drop(["A_H1", "A_H3", "A_H1N1_pdm09", "A_H3N2v",
                               "A_Subtype_not_Available"], axis=1)

seasons_a.plot()

seasons_b.plot()


labels = ['A_(H1)', 'A_H3', 'A_H1N1_pdm09', 'A_H3N2v',
          'A_Subtype_not_Available', 'B_Victoria_Lineage',
          'B_Yamagata_Lineage', 'B_Unspecified_Lineage']
    

