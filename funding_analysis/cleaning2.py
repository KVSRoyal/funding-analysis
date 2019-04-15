import numpy as np
import pandas as pd
import xlrd
import pathlib
import xlwt

datademofilepath = pathlib.Path(__file__).parents[1] / 'resources' / 'datademo.xls'
outputfilepath = pathlib.Path(__file__).parents[1] / 'resources' / 'outdatademo.xls'

#reads file
#A program to clean the demographic data
demographic_df = pd.read_excel(datademofilepath)

#Capitalize all names of STATES
demographic_df['STATE'].str.upper()

#Delete rows without relevant information
demographic_df = demographic_df[demographic_df.TOTAL != 0]

#Sort by NCESID
demographic_df = demographic_df.sort_values('NCESID')

#Put sorted data onto new excel spreadsheet
demographic_df.to_excel(outputfilepath)

print("done")

#description thing for name meanings on xls - don't worry about this just yet
#sort by ncesid
#why the counting number columns?

#American indian/Alaska Native -AIAN
#Asian or Asian/ Pacific Islander - AAPI
#Hispanic - HISP
#Black - BLAC
#White - WHIT
#Hawiian Nat./Pacific Is. - HNPI
#Two or More - TOMR

#VScode folder? What are you and why are you there?