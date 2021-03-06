# An example of code that will find the description of any variable name (column title) given to it from the
# relevant_raw_data table
import pathlib
import pandas

# Load the description table as a pandas data frame\
workbook_path = pathlib.Path(__file__).parents[2] / 'resources' / 'raw_f33_data' / 'descriptions.xls'
descriptions_df = pandas.read_excel(workbook_path)

# Clean the Data Item names
for index in range(len(descriptions_df['Data Item'])):
    curr_data_item = descriptions_df.loc[index, 'Data Item']
    descriptions_df.loc[index, 'Data Item'] = curr_data_item.strip()

# Set the Data Item column as the row index
descriptions_df = descriptions_df.set_index('Data Item')


def find_description(variable, depth=1):
    """
    Returns a meaningful description of this column title.
    :param variable: The title of a column in either the data_flags1, data_flags2,
    relevant_raw_data or nonexhibit items file.
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
        description = descriptions_df.loc[variable, 'Description']
    except KeyError:
        return variable + ' does not exist'

    # Determine whether or not this value is dependent on any others
    dependees = descriptions_df.loc[variable, 'Dependees']

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
            dependee_description = find_description(dependee, depth + 1)
            description += '\n'
            for tab in range(depth):
                description += '\t'
            description += dependee + ': ' + dependee_description

    return general_info + description


print(find_description('state') + '\n')

print(find_description('CONUM') + '\n')

print(find_description('TOTALREV') + '\n')

print(find_description('ppsgenad') + '\n')
