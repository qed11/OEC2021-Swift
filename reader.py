import pandas as pd
import numpy as np
from helpers.people import Person

def getDic(filename:str):
    #big dictionary holding all information
    person_class = dict()
    

    inf = pd.read_excel(filename,sheet_name = 'ZBY1 Status', nrows = 4).to_numpy()
    
    #read student information first 
    stu = pd.read_excel(filename,sheet_name = 'Student Records', nrows = 580).to_numpy()
    for i in stu:
        person_dict = dict()
        if i[0] == np.nan:
            break
        #generate identifier
        key = 'S-' + str(i[0])
        #extracurricular
        ext = extra(str(i[9]))
        #health
        health = 0
        if i[8] != np.nan:
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
        person_class[key] = person

    
    #teachers
    t = pd.read_excel(filename,sheet_name = 'Teacher Records',nrows = 20).to_numpy()
    for i in t:
        person_dict = dict()
        if i[0] == np.nan:
            break
        key = 'T-'+str(i[0])
        for j in inf:
            if j[0] == i[0] and j[1] == i[1] and j[2] == i[2]:
                person_dict['infected'] = True
        person_dict['l_name'] = i[1]
        person_dict['f_name'] = i[2]
        person_dict['p1'] = i[3]
        person_dict['ident'] = key
        person = Person.from_dict(person_dict)
        person_class[key] = person
    
    #TAs
    ta = pd.read_excel(filename, sheet_name = 'Teaching Assistant Records',nrows = 6).to_numpy()
    #print(ta)
    for i in ta:
        person_dict = dict()
        i[0] = int(i[0])
        if i[0] == np.nan:
            break
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

if __name__=='__main__':
    p_class = getDic('OEC2021 - School Record Book .xlsx')
    '''
    print(p_class['S-86'].l_name)
    print(p_class['S-86'].f_name)
    print(p_class['S-86'].ident)
    print(p_class['S-86'].infected)
    print(p_class['S-86'].excur)
    print(p_class['S-86'].p1)
    print(p_class['S-86'].p2)
    print(p_class['S-86'].p3)
    print(p_class['S-86'].p4)
    print(p_class['S-86'].health)    
    print(p_class['S-86'].grade)
    '''