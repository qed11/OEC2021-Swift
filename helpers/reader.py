import pandas as pd
import numpy as np
from people import Person

def getDic(filename:str):
    #big dictionary holding all information
    person_class = dict()
    

    inf = pd.read_excel(filename,sheet_name = 'ZBY1 Status', nrows = 4).to_numpy()
    
    #read student information first 
    stu = pd.read_excel(filename,sheet_name = 'Student Records').to_numpy()
    for i in stu:
        person_dict = dict()
        if np.isnan(i[0]) == True:
            break
        #generate identifier
        i[0] = int(i[0])
        key = 'S-' + str(i[0])
        #extracurricular
        ext = extra(str(i[9]))
        #health
        health = 0
        if np.isnan(i[8]) == False:
            health = 1
        #creating individual element
        for j in inf:
            if j[0] == i[0] and j[1] == i[1] and j[2] == i[2]:
                person_dict['infected'] = True
        person_dict['l_name'] = i[1]
        person_dict['f_name'] = i[2]
        person_dict['grade'] = int(i[3])
        person_dict['p1'] = i[4]
        person_dict['p2'] = i[5]
        person_dict['p3'] = i[6]
        person_dict['p4'] = i[7]
        person_dict['ident'] = key
        person_dict['heatlh'] = health
        person_dict['excur'] = ext
        person = Person.from_dict(person_dict)
        #print(key)
        person_class[key] = person

    
    #teachers
    t = pd.read_excel(filename,sheet_name = 'Teacher Records').to_numpy()
    for i in t:
        person_dict = dict()
        if np.isnan(i[0]) == True:
            break
        i[0] = int(i[0])
        key = 'T-'+str(i[0])
        for j in inf:
            if j[0] == i[0] and j[1] == i[1] and j[2] == i[2]:
                person_dict['infected'] = True
        person_dict['l_name'] = i[1]
        person_dict['f_name'] = i[2]
        person_dict['p1'] = i[3]
        person_dict['ident'] = key
        person = Person.from_dict(person_dict)
        #print(key)
        person_class[key] = person
    
    #TAs
    ta = pd.read_excel(filename, sheet_name = 'Teaching Assistant Records').to_numpy()
    #print(ta)
    for i in ta:
        if np.isnan(i[0]) == True:
            break
        person_dict = dict()
        i[0] = int(i[0])
        key = 'TA-'+str(i[0])
        for j in inf:
            if j[0] == i[0] and j[1] == i[1] and j[2] == i[2]:
                person_dict['infected'] = True
        person_dict['l_name'] = i[1]
        person_dict['f_name'] = i[2]
        person_dict['p1'] = i[3]
        person_dict['p2'] = i[4]
        person_dict['p3'] = i[5]
        person_dict['p4'] = i[6]
        person_dict['ident'] = key
        person = Person.from_dict(person_dict)
        #print(key)
        person_class[key] = person

    return person_class

def extra(el):
    #no extracurricular
    if el == np.nan:
        return []
    
    if ',' in el:
        #multiple extracurricular
        return el.split(',')
    else:
        #one extracurricular
        return [el]

"""
if __name__=='__main__':
    p_class = getDic('OEC2021 - School Record Book .xlsx')
    '''
    print(p_class['S-580'].l_name)
    print(p_class['S-580'].f_name)
    print(p_class['S-580'].ident)
    print(p_class['S-580'].infected)
    print(p_class['S-580'].excur)
    print(p_class['S-580'].p1)
    print(p_class['S-580'].p2)
    print(p_class['S-580'].p3)
    print(p_class['S-580'].p4)
    print(p_class['S-580'].health)    
    print(p_class['S-580'].grade)
    '''
"""