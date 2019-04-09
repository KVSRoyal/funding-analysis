# A program that will make all necessary adjustments to revenue data from the Annual Survey of School System Finances
from funding_analysis.relevant_data_f33 import RelevantData
from funding_analysis.edbuild_district_data import EdbuildDistrictData

# Load the relevant data
relevant_data = RelevantData()

# Load the district data
district_data = EdbuildDistrictData()

# Get just the state revenue
adjusted_revenues = relevant_data.select_columns(['Idcensus', 'TSTREV', 'TLOCREV', 'TFEDREV','SCHLEV'])
print('Unchanged revenues')
print(adjusted_revenues)

# Remove the capital outlay
capital_outlay_series = relevant_data.select_column('C11')
adjusted_revenues['TSTREV'] = adjusted_revenues['TSTREV'] - capital_outlay_series
print('Revenue after removing capital outlay from State Revenue')
print(adjusted_revenues)

# Remove the revenue generated from sale of property
revenue_from_sale_of_property = relevant_data.select_column('u11')
adjusted_revenues['TLOCREV'] = adjusted_revenues['TLOCREV'] - revenue_from_sale_of_property
print('Revenue after removing revenue generated from the sale of property from local revenue')
print(adjusted_revenues)

# Removes a proportional share (based on the percent of each districts’ revenues that come from local, state and federal
# sources) of the total amount of money sent to outside charter LEAs—an expenditure category included in the
# F33 survey.

# Calculate what percentage of the revenue comes from each source
total_revenues = relevant_data.select_column('TOTALREV')
local_revenue_proportion = relevant_data.select_column('Tlocrev') / total_revenues
state_revenue_proportion = relevant_data.select_column('TSTREV') / total_revenues
federal_revenue_proportion = relevant_data.select_column('TFEDREV') / total_revenues

# Calculate the total amount sent to outside charter LEAs (both private and charter schools)
total_money_sent_outside = relevant_data.select_column('v91') + relevant_data.select_column('v92')
print('Total money sent to outside charter LEAs')

# Calculate how much to remove from each revenue total
amount_to_remove_from_local_revenue = local_revenue_proportion * total_money_sent_outside
amount_to_remove_from_state_revenue = state_revenue_proportion * total_money_sent_outside
amount_to_remove_from_federal_revenue = federal_revenue_proportion * total_money_sent_outside

# Remove a proportional share of the money sent to charter schools from
adjusted_revenues['TLOCREV'] = adjusted_revenues['TLOCREV'] - amount_to_remove_from_local_revenue
adjusted_revenues['TSTREV'] = adjusted_revenues['TSTREV'] - amount_to_remove_from_state_revenue
adjusted_revenues['TFEDREV'] = adjusted_revenues['TFEDREV'] - amount_to_remove_from_federal_revenue

print('Revenue after removing money spent on outside charter LEAs from all revenues')
print(adjusted_revenues)


# Exclude the Districts that are of types 5 (vocational or special education), 6 (nonoperating) or 7 (educational
# service agency) in the F33 data
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['SCHLEV'] != '05']
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['SCHLEV'] != '06']
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['SCHLEV'] != '07']

print('Revenue after removing schools of type 5, 6 and 7')
print(adjusted_revenues)

# If F33 school type is missing, exclude districts that are of types 4 (regional education service agency),
# 5 (state agency), 6 (federal agency), 7 (charter agency) or 8 (other education agency) based on Common Core of Data
# TODO
#


# Exclude districts with missing or zero total enrollments
adjusted_revenues = adjusted_revenues.loc[adjusted_revenues['SCHLEV'] != '05']

print(adjusted_revenues)
