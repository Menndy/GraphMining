import numpy as np
import xlrd

with xlrd.open_workbook('./test.xlsx') as f:
    table=f.sheets()[0]
    rows=table.nrows
    for i in range(0,rows):
        print(table.cell(i,0))