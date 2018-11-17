# Imports the weighted sparse matrix in the dissect format and changes the
# row and column names to numbers for easier importing in other applications.
# Result is stored in sm_numbered in the same folder.

import re

#directories
sm = './cooccurrence/weighted_sm.sm'
rowsfile = './cooccurrence/weighted_sm.rows'
colsfile = './cooccurrence/weighted_sm.cols'
 exportpath = './cooccurrence/sm_numbered.txt'

#read columns of sparse matrix and convert to dict format
cols_in = open(colsfile, 'r')
cols = []
for line in cols_in.readlines():
    cols.append(line[:-1])
cols_in.close()
col_i = 0
cols_total = len(cols)

sm_out = open(exportpath, 'w')
sm_in = open(sm, 'r', )


#loop through matrix file
row = -1
current_row = ''

for line in sm_in.readlines():
    #identify row index
    row_entry = re.search(r'^(\S+)(?=\s)', line).group(0) #entry = non-whitespace characters followed by whitespace character
    if row_entry != current_row:
        #if it does not match, we are in a new row
        row += 1
        if row % 1000 == 0:
            print('row', str(100*float(row)/590408)[:4], '%')
        current_row = row_entry
        col_i = 0

    #identify column index
    col_entry = re.search(r'\S+(?=\s+([0-9]+\.)?[0-9]+$)', line).group(0)
    while col_i < cols_total:
        if col_entry == cols[col_i]:
            col = col_i
            break
        col_i += 1

    #identify value
    value_str = re.search(r'([0-9]+\.)?[0-9]+$', line).group(0)
    value = float(value_str)

    newline = str(row) + ' ' + str(col) + ' ' + str(value)
    sm_out.write(newline)
    sm_out.write('\n')

sm_in.close()
