# A program that will make all necessary adjustments to revenue data from the Annual Survey of School System Finances
from funding_analysis.relevant_data_f33 import RelevantData
from funding_analysis.edbuild_district_data import EdbuildDistrictData

# Load the relevant data
relevant_data = RelevantData()

# Load the district data
district_data = EdbuildDistrictData()

# Get just the state revenue
adjusted_revenues = relevant_data.select_columns(['Idcensus', 'STATE', 'TSTREV', 'TLOCREV', 'TFEDREV', 'SCHLEV', 'ENROLL'])

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

# Calculate Per-pupil state and local revenues
adjusted_revenues['PPSTATE'] = adjusted_revenues['TSTREV'] / adjusted_revenues['ENROLL']
adjusted_revenues['PPLOCAL'] = adjusted_revenues['TLOCREV'] / adjusted_revenues['ENROLL']
print(adjusted_revenues)
