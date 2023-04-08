import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt



#########################################################################################################################
#
#   Author : Harry Yu
#   Date : 04/08/2023
#   Name : ESRP Analysis Program
#   Desc : Sorts through the mappings of treatment and background and computes the adjusted lead per potassium level
#
#########################################################################################################################


#reconstruction of my original code that got deleted

df = pd.read_csv('ROIs.xlsx_-_Sheet1_1.csv')
mappings = pd.read_csv('ADJUST_BG - Sheet1.csv')

#red only
dfBackground = df[df["roi_colour"] == " (red)"]
#dfBlue = df[df["roi_colour"] == " (blue)"]
#dfGreen = df[df["roi_colour"] == " (green)"]


#drop rows of turquois and deadtime > 30
df = df.drop(df[df["roi_colour"] == " (turquois)"].index)
df = df.drop(df[df['Dead_Time-mean[%]'] > 30].index)

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

lead_mean_list = []
potassium_mean_list = []
for label, Series in mappings.iterrows():

    #adjust lead values and average
    #print(Series['treatment'] + " lead:")
    lead_values = df.loc[(df['sample_num'] == Series['sample_num'])]['Pb_L-mean[ug/cm2]'].to_numpy() - dfBackground.loc[dfBackground['sample_num'] == Series['bg_num_red']]['Pb_L-mean[ug/cm2]'].to_numpy().item()
    lead_values = lead_values[lead_values != 0]
    lead_mean = np.mean(lead_values)
    lead_mean_list.append(lead_mean)

    #DO NOT subtract the background from the control
    if 'Control' in Series['treatment']:
        print('control: ' + Series['treatment'])
        potassium_values = df.loc[(df['sample_num'] == Series['sample_num'])]['K-mean[ug/cm2]'].to_numpy()
    else:
        print('not control: ' + Series['treatment'])
        potassium_values = df.loc[(df['sample_num'] == Series['sample_num'])]['K-mean[ug/cm2]'].to_numpy() - dfBackground.loc[dfBackground['sample_num'] == Series['bg_num_red']]['K-mean[ug/cm2]'].to_numpy().item()
    potassium_values = potassium_values[potassium_values != 0]
    potassium_mean = np.mean(potassium_values)
    potassium_mean_list.append(potassium_mean)


#insert into mappings
mappings.insert(4, "lead_no_background", lead_mean_list)
mappings.insert(5, "potassium_no_background", potassium_mean_list)
mappings['adjusted_lead'] = mappings['lead_no_background']/mappings['potassium_no_background']


#post-process (sort by treatment)
mappings_by_plant = mappings.sort_values(by=['plant'], ascending=True)
mappings_by_treatment = mappings.sort_values(by=['treatment'], ascending=True)

#replaced 72 with 71 due to lack of 71
#42 with 41 in the series sample num



#write to file
mappings_by_plant.to_csv('mappings_by_plant.csv')
mappings_by_treatment.to_csv('mappings_by_treatment.csv')


print(mappings_by_plant.head(10))
print(mappings_by_treatment.head(10))