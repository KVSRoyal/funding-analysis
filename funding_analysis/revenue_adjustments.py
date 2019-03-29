# A program that will make all necessary adjustments to revenue data from the Annual Survey of School System Finances
from funding_analysis.relevant_data_f33 import RelevantData
from funding_analysis.edbuild_district_data import EdbuildDistrictData

# Load the relevant data
relevant_data = RelevantData()

# Load the district data
district_data = EdbuildDistrictData()
