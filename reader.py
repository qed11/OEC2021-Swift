import pandas as pd
import numpy as np

l = pd.read_excel('OEC2021 - School Record Book .xlsx',sheet_name = 'Student Records', nrows = 580)
f = []
for lable, content in l.items():
    f.append(content[0])
print(f)