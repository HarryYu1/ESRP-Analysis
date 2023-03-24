import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

df = pd.read_csv('ROIs.xlsx_-_Sheet1_1.csv')

print(df['roi_name'])

#basic premise:

#red is always background

#first step: data cleanup