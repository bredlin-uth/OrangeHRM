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
    try:
        workbook = openpyxl.open(excel_path)
        sheet = workbook[sheet_name]
        row_index = None
        column_index = None
        for row in sheet.iter_rows(values_only=True):
            if row_header in row:
                row_index = row.index(row_header)
        for column in sheet.iter_cols(values_only=True):
            if column_header in column:
                column_index = column.index(column_header)

        if row_index is not None and column_index is not None:
            value = sheet.cell(row_index, column_index).value
            return value
        else:
            print(f"Headers not found: {row_header}, {column_header}")
            return None
    except Exception as e:
        print(f"Error loading workbook or fetching data: {e}")
        return None


def get_row_excel_data(sheet_name, row):
    data = []
    workbook = openpyxl.open(excel_path)
    sheet = workbook[sheet_name]
    total_rows = sheet.max_row
    total_columns = sheet.max_column
    for i in range(row, total_rows + 1):
        for column in range(1, total_columns + 1):
            data.append(sheet.cell(i, column).value)
    return data
