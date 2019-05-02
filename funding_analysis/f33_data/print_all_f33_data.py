# A program that will print all relevant data from the Annual Survey of School System Finances
from funding_analysis.f33_data.relevant_data_f33 import RelevantData
from funding_analysis.edbuild_data.edbuild_district_data import EdbuildDistrictData

# Load the relevant data
relevant_data = RelevantData()

# Load the district data
district_data = EdbuildDistrictData()

# Print out all information about the relevant raw data items
print(relevant_data.find_descriptions(relevant_data.get_all_relevant_raw_data().columns))

# Print out all information about the nonexhibit data items
print(relevant_data.find_descriptions(relevant_data.get_all_nonexhibit_data().columns))