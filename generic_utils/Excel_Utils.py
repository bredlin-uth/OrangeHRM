import os

import openpyxl

excel_path = os.path.join(os.path.dirname(os.path.abspath('.')), "test_data\\Data.xlsx")

def get_row_count(sheet_name):
    workbook = openpyxl.open(excel_path)
    sheet = workbook[sheet_name]
    return sheet.max_row

def get_column_count(sheet_name):
    workbook = openpyxl.open(excel_path)
    sheet = workbook[sheet_name]
    return sheet.max_column

def read_data_from_excel(sheet_name, row, column):
    workbook = openpyxl.open(excel_path)
    sheet = workbook[sheet_name]
    return sheet.cell(row, column).value

def write_data_into_excel(sheet_name, row, column, data):
    workbook = openpyxl.open(excel_path)
    sheet = workbook[sheet_name]
    sheet.cell(row, column).value = data
    workbook.save(excel_path)

def fetch_data_from_excel(sheet_name, row_header, column_header):
    workbook = openpyxl.open(excel_path)
    sheet = workbook[sheet_name]
    # Find the row and column indices
    for row_index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
        if row_header in row:
            break
    for col_index, col in enumerate(sheet.iter_cols(values_only=True), start=1):
        if column_header in col:
            break
    # Check if the headers were found
    if row_index and col_index:
        cell_value = sheet.cell(row_index, col_index).value
        return cell_value
    else:
        return None


def get_row_excel_data(sheet_name, row, path=excel_path):
    data = []
    workbook = openpyxl.open(path)
    sheet = workbook[sheet_name]
    total_rows = sheet.max_row
    total_columns = sheet.max_column
    for i in range(row, total_rows + 1):
        for column in range(1, total_columns + 1):
            data.append(sheet.cell(i, column).value)
    return data


print(fetch_data_from_excel("Credentials", "Testing", "URL"))