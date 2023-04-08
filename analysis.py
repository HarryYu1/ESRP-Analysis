import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

#reconstruction of my original code that got deleted

df = pd.read_csv('ROIs.xlsx_-_Sheet1_1.csv')

#red only
dfBackground = df[df["roi_colour"] == " (red)"]
#delete red and turquois from df
df = df.drop(df[df["roi_colour"] == " (red)"].index)
df = df.drop(df[df["roi_colour"] == " (turquois)"].index)

#sample_num generation
df["sample_num"] = df.roi_name.str[6:10]
dfBackground["sample_num"] = dfBackground.roi_name.str[6:10]

#map the potassium and lead subtraction
df['lead_no_background'] = df['Pb_L-mean[ug/cm2]'] - df['sample_num'].map(dfBackground.set_index('sample_num')['Pb_L-mean[ug/cm2]'])
df['potassium_no_background'] = df['K-mean[ug/cm2]'] - df['sample_num'].map(dfBackground.set_index('sample_num')['K-mean[ug/cm2]'])


#final calculation
df["adjusted_lead"] = df["lead_no_background"]/df["potassium_no_background"]


#write to file
df.to_csv("out.csv")
dfBackground.to_csv("background_values.csv")

print(df.head(100))
