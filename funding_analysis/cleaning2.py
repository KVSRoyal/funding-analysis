#Problems to fix : in Agency ID column some of the things are indented in excel
#Some rows do not seem to have data: they have either †'s (data not applicable) or 0's or - (data missing) or ‡ (data does not meet quality standards)
# #### where there should be numbers: is it relevant information or is it okay that it does that?
#change agency ID to an integer: do I need to or will it work as a string?

#How do I start?  Remove the schools that have missing or 0 enrollment

#Some say District some say (District): What is the distinction/difference?
import numpy as np
import pandas as pd
import xlrd

import matplotlib
import matplotlib.pyplot as pp

demographics = pd.read_excel('SchoolDataProj/datademo.xls')

print (demographics.STATE)