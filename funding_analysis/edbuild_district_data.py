# A class that will store all data given in the original edbuild analysis in a pandas dataframe
import pathlib
import pandas


class EdbuildDistrictData:
    """
    An object containing all district data from the original EdBuild Analysis and ways to
    load their descriptions
    """
    def __init__(self):
        """
        Creates an object containing all district data from the original EdBuild Analysis and ways to
        load their descriptions
        """
        filepath = pathlib.Path(__file__).parents[1] / 'resources' / 'edbuild_district_data.xlsx'
        self.district_data_df = pandas.read_excel(filepath)
        self.__abbreviate_column_titles()

    def get_all_district_data(self):
        """
        Returns a pandas dataframe containing all edbuild district data
        :return: A pandas dataframe containing all edbuild district data
        """
        return self.district_data_df

    def select_column(self, variable):
        """
        Returns a pandas dataframe of all data for this variable / column title
        :param variable: The variable / column title for which all available data is being selected
        :return: All data for this variable / column item in a pandas dataframe
        """
        return self.district_data_df[variable].to_frame()

    def select_columns(self, variables):
        """
        Returns a pandas dataframe of all data for the given list of variables / column titles
        :param variables: A list of variables / column titles for which all available data is being selected
        :return: All data for these variables / column titles in a pandas dataframe
        """
        return self.district_data_df[variables]

    def __abbreviate_column_titles(self):
        """
        Abbreviates the column titles and stores their full length name in a dictionary. This
        will not abbreviate the State, the NCESID, or the District.
        """
        self.descriptions = {}

        # Add column titles that should be unchanged to dictionary. Ensure they are upper case
        for unchanged_column_title in self.district_data_df.columns[0:3]:
            self.descriptions[unchanged_column_title.upper()] = unchanged_column_title

        # Add abbreviated columns titles and their descriptions to the dictionary
        for column_title in self.district_data_df.columns[3:]:
            abbreviated_column_title = self.__abbreviate_column_title(column_title)
            self.descriptions[abbreviated_column_title] = column_title

        reversed_descriptions = dict(zip(self.descriptions.values(), self.descriptions.keys()))
        self.district_data_df.rename(columns=reversed_descriptions, inplace=True)

    @staticmethod
    def __abbreviate_column_title(column_title):
        """
        Returns the abbreviated version of a column title, all in upper case
        :return: The abbreviated version of a column title, all in upper case
        """
        acronym = ''

        for word in column_title.split():
            acronym += word[0]

        return acronym.upper()

    def find_description(self, variable):
        """
        Returns a meaningful description of this column title.
        :param variable: The title of a column in the edbuild district data file
        :return: A meaningful description of the column title.
        """
        try:
            return variable + ':\t' + self.descriptions[variable.upper()]
        except KeyError:
            return variable + ' does not exist'

    def find_descriptions(self, variables):
        """
        Returns meaningful descriptions of these column titles.
        :param variable: The titles of columns in the edbuild district data file
        :return: A meaningful description of these column titles.
        """
        descriptions = ''

        for variable in variables:
            descriptions += self.find_description(variable) + '\n'

        return descriptions
