import numpy as np
import pandas as pd
import xlrd
import pathlib
import xlwt

datademofilepath = pathlib.Path(__file__).parents[1] / 'resources' / 'datademo.xls'
outputfilepath = pathlib.Path(__file__).parents[1] / 'resources' / 'outdatademo.xls'

#reads file
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

#description thing for name meanings on xls
#sort by ncesid
#why the counting number columns?