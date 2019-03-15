# A program for cleaning up the summary tables
import xlrd
import pathlib

# Get the correct path for the workbook with the summary tables
summary_tables_workbook_path = pathlib.Path(__file__).parents[1] / 'resources' / 'elsec16_sumtables.xls'

# Open the workbook with the summary tables
workbook = xlrd.open_workbook(summary_tables_workbook_path, on_demand=True)

# Open the sheet with the titles of the summary tables (Table of Contents)
table_names_sheet = workbook.sheet_by_index(0)

# Read in ONLY the sheet titles
list_of_sheet_names = []
for row in range(table_names_sheet.nrows):
    label_found = table_names_sheet.cell(row, 1).value

    # Ignore empty cells
    if label_found == xlrd.empty_cell.value:
        continue

    # Ignore everything that is all block letters
    if label_found.isupper():
        continue

    # If there is a colon in the title, ignore everything after and including the colon
    index_of_colon = label_found.find(':')
    if index_of_colon != -1:
        label_found = label_found[:index_of_colon]

    list_of_sheet_names.append(label_found)

# Print the names we found
for name in list_of_sheet_names:
    print(name)

# TODO: Remove the sumtables xls file somehow, for the sake of my sanity
