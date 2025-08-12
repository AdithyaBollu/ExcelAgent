
import os
import openpyxl
import natsort
from openpyxl.utils import get_column_letter

def read_excel_file(file_path):
    # Select the active sheet or specify the sheet by name
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active  # or wb['Sheet1']

    # Loop through all rows and cells
    valuable_cells = []
    print("valuable cells in the excel file: ", valuable_cells)
    for row in sheet.iter_rows():
        for cell in row:
            if  cell.value:
                valuable_cells.append(f"{cell.coordinate}: {cell.value}")

    valuable_cells = natsort.natsorted(valuable_cells)
    print("valuable cells in the excel file: ", "\n".join(valuable_cells))
    return "\n".join(valuable_cells)

def add_formula_to_excel(file_path, column_letter, formula_template, start_row, end_row):
    print(f"Adding formula in column {column_letter} from row {start_row} to {end_row}")
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active  # or wb['Sheet1']
    
    if end_row is None:
        end_row = sheet.max_row
    
    for row in range(start_row, end_row + 1):

        formula = formula_template.format(row=row)
        cell = f"{column_letter}{row}"
        sheet[cell] = formula
    
    wb.save("./createdFiles/" + os.path.basename(file_path))
    return f"Formula applied to {column_letter}{start_row}:{column_letter}{end_row} in {file_path}", f"./createdFiles/{os.path.basename(file_path)}"

def write_to_cell(file_path, column, row, value):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active  # or wb['Sheet1']
    
    cell = f"{column}{row}"
    sheet[cell] = value
    
    wb.save("./createdFiles/" + os.path.basename(file_path))
    return f"Value '{value}' written to {cell} in {file_path}", f"./createdFiles/{os.path.basename(file_path)}"