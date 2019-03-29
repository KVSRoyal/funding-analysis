#Some say District some say (District): What is the distinction/difference?

import numpy as np
import pandas as pd
import xlrd

import matplotlib
import matplotlib.pyplot as pp

demographic_df = pd.read_excel('datademo.xls')

#Capitalize all names of STATES
demographic_df['STATE'] = map(lambda x: x.upper(), demographic_df['STATE'])

#Delete rows without relevant information
demographic_df = demographic_df[demographic_df.TOTAL != 0]

ExcelFile.parse(demographic_df)