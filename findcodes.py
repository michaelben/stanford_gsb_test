import re, math
from collections import Counter
import operator
import sys

WORD = re.compile(r'\w+')

# get cosine match value for 2 strings
def get_cosine_match_value(str1, str2):
    def get_cosine(vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def text_to_vector(text):
        words = WORD.findall(text)
        return Counter(words)

    vector1 = text_to_vector(str1)
    vector2 = text_to_vector(str2)

    return get_cosine(vector1, vector2)


import xlrd
sample_file = 'sample_Descriptions.xlsx'
hscodes_file = 'HScodes_1988.xls'
n = 2

if len(sys.argv) > 1:
    n = int(sys.argv[1])

# read sample file
samples = xlrd.open_workbook(sample_file)
samples = samples.sheet_by_name('Sheet1')
samples_list = []
for rownum in range(1, samples.nrows):
    values = samples.row_values(rownum)
    samples_list.append([str(int(values[0])), values[1]])

# read hscode file
hscodes = xlrd.open_workbook(hscodes_file)
hscodes = hscodes.sheet_by_name('HS_v1988')
hscodes_map = {}
for rownum in range(hscodes.nrows):
    values = hscodes.row_values(rownum)
    hscodes_map[values[0]] = values[1]
del hscodes_map['HScode']

# search the best matches
for i in samples_list:
    full_desc = i[1]
    cosines = []
    for code in hscodes_map.keys():
        if len(code) == 4:
            code2 = code[0:2]
            code4 = code
            if code2 in code4:
                desc = hscodes_map[code]
            elif code4 in code2:
                desc = hscodes_map[code2]
            else:
                desc = hscodes_map[code] + ' ' + hscodes_map[code2]
        elif len(code) == 6:
            code2 = code[0:2]
            code4 = code[0:4]
            if code2 in code4:
                desc = hscodes_map[code] + ' ' + hscodes_map[code4] 
            elif code4 in code2:
                desc = hscodes_map[code] + ' ' + hscodes_map[code2]
            else:
                desc = hscodes_map[code] + ' ' + hscodes_map[code4] + ' ' + hscodes_map[code2]
        else:
            desc = hscodes_map[code]

        cosine = get_cosine_match_value(full_desc, desc)
        cosines.append([i[0], i[1], code, hscodes_map[code2], hscodes_map[code4], hscodes_map[code], cosine])
    cosines = sorted(cosines, key=operator.itemgetter(6))[::-1][0:n]
    print(cosines)

