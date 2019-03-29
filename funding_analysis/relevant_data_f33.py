# A class that will store all relevant data and descriptions into pandas dataframes
import pathlib
import pandas


class RelevantData:
    """
    An object containing all relevant data from the Annual Survey of School System Finances and ways to
    load their descriptions
    """

    def __init__(self):
        """
        Creates a RelevantData object containing all relevant data from the Annual Survey of School System
        Finances and ways to load their descriptions
        """
        # Get the directory holding the necessary files: relevant raw data and descriptions
        workbook_path = pathlib.Path(__file__).parents[1] / 'resources'

        # Load the relevant raw data table as a pandas data frame
        relevant_raw_data_workbook_path = workbook_path / 'raw_data' / 'relevant_raw_data.xls'
        self.relevant_raw_data_df = pandas.read_excel(relevant_raw_data_workbook_path)

        # Load the nonexhibit items as a pandas data frame
        nonexhibit_items_workbook_path = workbook_path / 'raw_data' / 'nonexhibit_items.xls'
        self.nonexhibit_items_df = pandas.read_excel(nonexhibit_items_workbook_path)

        # Load the description table as a pandas data frame\
        descriptions_workbook_path = workbook_path / 'descriptions.xls'
        self.descriptions_df = pandas.read_excel(descriptions_workbook_path)

        # Clean the Data Item names
        for index in range(len(self.descriptions_df['Data Item'])):
            curr_data_item = self.descriptions_df.loc[index, 'Data Item']
            self.descriptions_df.loc[index, 'Data Item'] = curr_data_item.strip()

        # Set the Data Item column as the row index
        self.descriptions_df = self.descriptions_df.set_index('Data Item')

    def get_all_relevant_raw_data(self):
        """
        Returns a pandas dataframe containing all relevant raw data
        :return: A pandas dataframe containing all relevant raw data
        """
        return self.relevant_raw_data_df

    def select_column(self, variable):
        """
        Returns a pandas dataframe of all data for this variable / data item tag
        :param variable: The type of data item for which all available data is being selected
        :return: All data for this data item in a pandas dataframe
        """
        # Ensure the variable is upper case
        variable = variable.upper()

        try:
            return self.relevant_raw_data_df[variable].to_frame()
        except KeyError:
            return self.nonexhibit_items_df[variable].to_frame()
        except KeyError:
            return None

    def select_columns(self, variables):
        """
        Returns a pandas dataframe of all data for the given list of variables / data item tags
        :param variables: A list of data items for which all available data is being selected
        :return: All data for these data items in a pandas dataframe
        """
        selected_columns = pandas.DataFrame()

        for variable in variables:
            # Ensure the variable is upper case
            variable = variable.upper()

            selected_columns[variable] = self.select_column(variable)[variable]

        return selected_columns

    def find_description(self, variable, depth=1):
        """
        Returns a meaningful description of this column title.
        :param variable: The title of a column in either the relevant_raw_data or nonexhibit items file.
        :param depth: The number of tabs the dependees of this variable should be offset by
        :return: A meaningful description of the column title.
        """
        # Add General Info that applies to all variables, but only if depth = 1
        if depth == 1:
            general_info = 'GENERAL INFO:\n' \
                           'All amounts, except for fall membership and personal income, are expressed in\n' \
                           'thousands of dollars. Fall membership data are presented in whole amounts.\n' \
                           'Personal income totals are expressed in millions of dollars.\n\n' \
                           'VARIABLE INFO:\n'
        else:
            general_info = ''

        # Make sure the input variable is upper case
        variable = variable.upper()

        # Find the appropriate description. If the variable cannot be found, return DNE
        try:
            description = self.descriptions_df.loc[variable, 'Description']
        except KeyError:
            return variable + ' does not exist'

        # Determine whether or not this value is dependent on any others
        dependees = self.descriptions_df.loc[variable, 'Dependees']

        # If this value is dependent, determine which other variables it is dependent on
        if dependees is not pandas.np.nan:
            dependees = dependees.replace(')', '')
            dependees = dependees.replace('+', '')
            parsed_dependees = dependees.split(' ')
            parsed_dependees.pop(0)
            parsed_dependees.pop(0)
            parsed_dependees = [parsed_dependee for parsed_dependee in parsed_dependees if parsed_dependee != '']

            # Append the descriptions of the values it depends on to its description
            for dependee in parsed_dependees:
                dependee_description = self.find_description(dependee, depth + 1)
                description += '\n'
                for tab in range(depth - 1):
                    description += '\t'
                description += dependee_description

        return general_info + variable + ':\t' + description

    def find_descriptions(self, variables):
        """
        Returns a meaningful description of these column title.
        :param variable: The titles of a columns in either the relevant_raw_data or nonexhibit items file.
        :param depth: The number of tabs the dependees of this variable should be offset by
        :return: A meaningful description of these column titles.
        """
        # Add general info
        descriptions = 'GENERAL INFO:\n' \
                       'All amounts, except for fall membership and personal income, are expressed in\n' \
                       'thousands of dollars. Fall membership data are presented in whole amounts.\n' \
                       'Personal income totals are expressed in millions of dollars.\n\n' \
                       'VARIABLE INFO:\n'

        # Add info for each variable
        for variable in variables:
            descriptions += self.find_description(variable, 2) + '\n'

        return descriptions
