import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

#reconstruction of my original code that got deleted

df = pd.read_csv('ROIs.xlsx_-_Sheet1_1.csv')
mappings = pd.read_csv('ADJUST_BG - Sheet1.csv')

#red only
dfBackground = df[df["roi_colour"] == " (red)"]
#dfBlue = df[df["roi_colour"] == " (blue)"]
#dfGreen = df[df["roi_colour"] == " (green)"]


#drop rows of turquois
df = df.drop(df[df["roi_colour"] == " (turquois)"].index)

#sample_num generation
dfBackground["sample_num"] = dfBackground.roi_name.str[6:10]
df["sample_num"] = df.roi_name.str[6:10]
#dfBlue["sample_num"] = dfBlue.roi_name.str[6:10]
#dfGreen["sample_num"] = dfGreen.roi_name.str[6:10]

#dfBlue['sample_num'] = dfBlue['sample_num'].astype(int)
dfBackground['sample_num'] = dfBackground['sample_num'].astype(int)
df['sample_num'] = df['sample_num'].astype(int)
#dfGreen['sample_num'] = dfGreen['sample_num'].astype(int)

#subtract based off of values in ADJUST_BG
#there will be both a green column and a blue column
i=0
lead_mean_list = []
potassium_mean_list = []
for label, Series in mappings.iterrows():

    #adjust lead values and average
    #print(Series['treatment'] + " lead:")
    lead_values = df.loc[(df['sample_num'] == Series['sample_num'])]['Pb_L-mean[ug/cm2]'].to_numpy() - dfBackground.loc[dfBackground['sample_num'] == Series['bg_num_red']]['Pb_L-mean[ug/cm2]'].to_numpy().item()
    lead_values = lead_values[lead_values != 0]
    lead_mean = np.mean(lead_values)
    lead_mean_list.append(lead_mean)

    i += 1

#insert into mappings
mappings.insert(4, "lead_no_background", lead_mean_list)

#replaced 72 with 71 due to lack of 71
#42 with 41 in the series sample num
#print((dfBackground.loc[dfBackground['sample_num'] == 72])['Pb_L-mean[ug/cm2]'].to_numpy())

#final calculation


#write to file
#df.to_csv("out.csv")
#dfBackground.to_csv("background_values.csv")

#print(df.head(5))
print(mappings.head(20))
