# An example of how to load the data from all of the simple excel files into pandas dataframes
import pathlib
import pandas

# Open the relevant sheet in the elementary-secondary financial data for 2016 workbook as a dataframe
workbooks_directory_path = pathlib.Path(__file__).parents[1] / 'resources' / 'raw_data'

# Load the non-exhibit items table as a pandas data frame
nonexhibit_items_workbook_path = workbooks_directory_path / 'nonexhibit_items.xls'
nonexhibit_items_df = pandas.read_excel(nonexhibit_items_workbook_path)

# Do some shallow testing to verify everything went well
col1_title = nonexhibit_items_df.columns[0]
assert col1_title == 'STATE'
assert len(nonexhibit_items_df.index) == 14325
assert len(nonexhibit_items_df.columns) == 141

# Load the data flags table as a pandas data frame
data_flags1_workbook_path = workbooks_directory_path / 'data_flags1.xls'
data_flags1_df = pandas.read_excel(data_flags1_workbook_path)

# Do some shallow testing to verify everything went well
col1_title = data_flags1_df.columns[0]
assert col1_title == 'STATE'
assert len(data_flags1_df.index) == 7160
assert len(data_flags1_df.columns) == 130


data_flags2_workbook_path = workbooks_directory_path / 'data_flags2.xls'
data_flags2_df = pandas.read_excel(data_flags2_workbook_path)

# Do some shallow testing to verify everything went well
col1_title = data_flags2_df.columns[0]
assert col1_title == 'STATE'
assert len(data_flags2_df.index) == 7165
assert len(data_flags2_df.columns) == 130

# Append the data_flags dataframes into one large dataframe
data_flags_df = data_flags1_df.append(data_flags2_df, ignore_index=True)

# Do some shallow testing to verify everything went well
col1_title = data_flags2_df.columns[0]
assert col1_title == 'STATE'
for state_id in data_flags_df[col1_title]:
    assert state_id != 'STATE'
assert len(data_flags_df.index) == 14325
assert len(data_flags_df.columns) == 130


# Load the relevant raw data table as a pandas data frame
relevant_raw_data_workbook_path = workbooks_directory_path / 'relevant_raw_data.xls'
relevant_raw_data_df = pandas.read_excel(relevant_raw_data_workbook_path)

# Do some shallow testing to verify everything went well
col1_title = relevant_raw_data_df.columns[0]
assert col1_title == 'IDCENSUS'
assert len(relevant_raw_data_df.index) == 14325
assert len(relevant_raw_data_df.columns) == 66


# Load the district data values given in the original analysis
edbuild_district_data_workbook_path = workbooks_directory_path.parents[0] / 'edbuild_district_data.xlsx'
edbuild_district_data = pandas.read_excel(edbuild_district_data_workbook_path)

# Do some shallow testing to verify everything went well
assert len(edbuild_district_data.index) == 12944
assert len(edbuild_district_data.columns) == 21

print('SUCCESS: Sheets parsed as expected.')
