# A program that will make all necessary adjustments to revenue data from the Annual Survey of School System Finances
from funding_analysis.relevant_data_f33 import RelevantData
from funding_analysis.edbuild_district_data import EdbuildDistrictData

# Load the relevant data
relevant_data = RelevantData()

# Load the district data
district_data = EdbuildDistrictData()

# Print out all information about the relevant raw data items
# print(relevant_data.find_descriptions(relevant_data.get_all_relevant_raw_data().columns))

adjusted_state_revenues = relevant_data.select_columns(['NAME', 'TSTREV'])
print(adjusted_state_revenues)
adjusted_state_revenues = adjusted_state_revenues['TSTREV'].sub(relevant_data.select_column('C11'), axis=0)
print(adjusted_state_revenues)
