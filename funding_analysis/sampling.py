# A program that will allow users to sample data in pandas dataframes from the relevant_raw_data file
import pathlib
import pandas

# Open the relevant sheet in the elementary-secondary financial data for 2016 workbook as a dataframe
workbooks_directory_path = pathlib.Path(__file__).parents[1] / 'resources' / 'raw_data'

# Load the relevant raw data table as a pandas data frame
relevant_raw_data_workbook_path = workbooks_directory_path / 'relevant_raw_data.xls'
relevant_raw_data_df = pandas.read_excel(relevant_raw_data_workbook_path)

def sample_column(variable):
    """
    Returns a pandas dataframe of all data for this variable / data item tag
    :param variable: The type of data item for which all available data is being sampled
    :return: All data for this data item in a pandas dataframe
    """
    return relevant_raw_data_df[variable].to_frame()


def sample_columns(variables):
    """
    Returns a pandas dataframe of all data for the given list of variables / data item tags
    :param variables: A list of data items for which all available data is being sampled
    :return: All data for these data items in a pandas dataframe
    """
    return relevant_raw_data_df[variables]


print(str(sample_column('CONUM')) + '\n')
print(str(sample_columns(['NAME', 'TOTALREV'])) + '\n')
