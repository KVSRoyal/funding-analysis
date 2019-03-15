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


# This is a block of code that needs to be changed because the data_flags file
# is too large to push to GitHub
# Load the data flags table as a pandas data frame
#data_flags_workbook_path = workbooks_directory_path / 'data_flags.xls'
#data_flags_df = pandas.read_excel(data_flags_workbook_path)

# Do some shallow testing to verify everything went well
#col1_title = data_flags_df.columns[0]
#assert col1_title == 'STATE'
#assert len(data_flags_df.index) == 14325
#assert len(data_flags_df.columns) == 130


# Load the relevant raw data table as a pandas data frame
relevant_raw_data_workbook_path = workbooks_directory_path / 'relevant_raw_data.xls'
relevant_raw_data_df = pandas.read_excel(relevant_raw_data_workbook_path)

# Do some shallow testing to verify everything went well
col1_title = relevant_raw_data_df.columns[0]
assert col1_title == 'IDCENSUS'
assert len(relevant_raw_data_df.index) == 14325
assert len(relevant_raw_data_df.columns) == 66

print('SUCCESS: Sheets parsed as expected.')
