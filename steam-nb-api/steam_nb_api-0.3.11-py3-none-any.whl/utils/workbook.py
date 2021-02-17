import xlrd

def find_position_of(worksheet, keyword):
    for r in range(worksheet.nrows):
        for c in range(worksheet.ncols):
            if(worksheet.cell(r,c).value==keyword):
                return (r,c)
            
def find_last_non_empty_index(row):
    for i in range(len(row)):
        if row[i].ctype == 0:
            return i
        
def get_table(worksheet, position, dimension):
    output = [[0 for x in range(dimension[0])] for y in range(dimension[1])] 
    
    for r in range(dimension[0]):
        for c in range(dimension[1]):
            output[r][c] = worksheet.cell(position[0] + r, position[1] + c + 1).value
    
    return output