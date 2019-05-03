# A program that will make all necessary adjustments to revenue data from the Annual Survey of School System Finances
from funding_analysis.f33_data.relevant_data_f33 import RelevantData
from funding_analysis.edbuild_data.edbuild_district_data import EdbuildDistrictData
import pathlib
import pandas
import re

# Load the relevant data
relevant_data = RelevantData()

# Get just the state revenue
adjusted_revenues = relevant_data.select_columns(['Idcensus', 'STATE', 'TSTREV', 'TLOCREV', 'TFEDREV', 'SCHLEV',
                                                  'ENROLL', 'NCESID'])

# Put the NCESID in front and sort by it
cols = list(adjusted_revenues.columns)
cols.insert(0, cols.pop(cols.index('NCESID')))
adjusted_revenues = adjusted_revenues.loc[:, cols]
adjusted_revenues.sort_values(['NCESID'])

# Load all of the Common Core Data
outputfilepath = pathlib.Path(__file__).parents[1] / 'resources' / 'outdatademo.xls'

# Read file and sort by NCESID
demographic_df = pandas.read_excel(outputfilepath)
demographic_df.sort_values('NCESID')

# Add all non-duplicate columns from the demographic table to the cost adjusted revenues table
for col in demographic_df.columns:
    if col not in adjusted_revenues:
        adjusted_revenues[col] = demographic_df[col]

# Print the unchanged table
print(adjusted_revenues)


# ~~~ DONE LOADING ALL NECESSARY DATA. READY TO BEGIN ADJUSTMENTS ~~~ #


# Remove the capital outlay
capital_outlay_series = relevant_data.select_column('C11')
adjusted_revenues['TSTREV'] = adjusted_revenues['TSTREV'] - capital_outlay_series

# Remove the revenue generated from sale of property
revenue_from_sale_of_property = relevant_data.select_column('u11')
adjusted_revenues['TLOCREV'] = adjusted_revenues['TLOCREV'] - revenue_from_sale_of_property

# Removes a proportional share (based on the percent of each districts’ revenues that come from local, state and federal
# sources) of the total amount of money sent to outside charter LEAs—an expenditure category included in the
# F33 survey.

# Calculate what percentage of the revenue comes from each source
local_revenue_proportion = relevant_data.select_column('PCTLTOT') / 100
state_revenue_proportion = relevant_data.select_column('PCTSTOT') / 100
federal_revenue_proportion = relevant_data.select_column('PCTFTOT') / 100

# Calculate the total amount sent to outside charter LEAs (both private and charter schools)
total_money_sent_outside = relevant_data.select_column('v91') + relevant_data.select_column('v92')

# Calculate how much to remove from each revenue total
amount_to_remove_from_local_revenue = local_revenue_proportion * total_money_sent_outside
amount_to_remove_from_state_revenue = state_revenue_proportion * total_money_sent_outside
amount_to_remove_from_federal_revenue = federal_revenue_proportion * total_money_sent_outside

# Remove a proportional share of the money sent to charter schools from
adjusted_revenues['TLOCREV'] = adjusted_revenues['TLOCREV'] - amount_to_remove_from_local_revenue
adjusted_revenues['TSTREV'] = adjusted_revenues['TSTREV'] - amount_to_remove_from_state_revenue
adjusted_revenues['TFEDREV'] = adjusted_revenues['TFEDREV'] - amount_to_remove_from_federal_revenue

# Exclude the Districts that are of types 5 (vocational or special education), 6 (nonoperating) or 7 (educational
# service agency) in the F33 data
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['SCHLEV'] != '05']
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['SCHLEV'] != '06']
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['SCHLEV'] != '07']

# Exclude districts with zero total enrollments (missing is also represented as 0)
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['ENROLL'] != 0]

# Exclude districts with zero revenue (missing is also represented as 0)
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['TFEDREV'] != 0]
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['TLOCREV'] != 0]
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['TSTREV'] != 0]

# Exclude districts with low revenues (< $500,000)
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['TLOCREV'] >= 500]
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['TSTREV'] >= 500]
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['TFEDREV'] >= 500]

# Exclude districts with high revenues (> $100,000,000)
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['TLOCREV'] <= 100000]
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['TSTREV'] <= 100000]
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['TFEDREV'] <= 100000]

# Exclude districts from US Territories
states = [str(num) for num in range(52)]
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['STATE'].isin(states)]

# School districts that intersect with Native American Reservations because federal dollars are a much larger
# proportion of revenue for Bureau of Indian Affairs (BIA) schools and the federal dollars are not always intended
# to supplement funds from BIA. TODO
our_ncesids = adjusted_revenues['NCESID'].tolist()


# Load the district data
district_data = EdbuildDistrictData()
edbuild_ncesids = district_data.select_column('ncesid').tolist()
print(edbuild_ncesids)

# Check if the NCESID is in the edbuild data. Remove it if it isn't. (Our data has an extra leading zero)
to_remove = [ncesid for ncesid in our_ncesids if int(ncesid[1:]) not in edbuild_ncesids]
print(str(to_remove) + '\n' + str(len(our_ncesids)) + '\t' + str(len(edbuild_ncesids)) + '\t' + str(len(to_remove)) +
      '\n')
adjusted_revenues = adjusted_revenues.loc[~adjusted_revenues['NCESID'].isin(to_remove)]

# Calculate Per-pupil state and local revenues
adjusted_revenues['PPSTATE'] = adjusted_revenues['TSTREV'] / adjusted_revenues['ENROLL']
adjusted_revenues['PPLOCAL'] = adjusted_revenues['TLOCREV'] / adjusted_revenues['ENROLL']
print(adjusted_revenues)
