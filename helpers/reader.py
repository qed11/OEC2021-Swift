import pandas as pd
import numpy as np
from people import Person

def getDic(filename:str):
    '''
    Method that generate a dictionary of student, teacher and ta information to be accessed from the school record book

    :param filename: pathway to the school record book 
    :return dictionary: contained with information of student and using genreated identification number as keys
    '''
    #big dictionary holding all information
    person_class = dict()
    
    #information of infected personnel
    inf = pd.read_excel(filename,sheet_name = 'ZBY1 Status', nrows = 4).to_numpy()
    
    #read student information first 
    stu = pd.read_excel(filename,sheet_name = 'Student Records').to_numpy()
    for i in stu:
        person_dict = dict()
        #check if the entry is valid
        if np.isnan(i[0]) == True:
            break
        #generate identifier
        i[0] = int(i[0])
        key = 'S-' + str(i[0])
        
        #extracurricular
        ext = extra(str(i[9]))
        
        #health condition
        health = False
        if isinstance(i[8],str) == True:
            health = True
        
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
        person_dict['health'] = health
        person_dict['excur'] = ext
        person = Person.from_dict(person_dict)
        person_class[key] = person

    #===========================================================================
    #teachers
    t = pd.read_excel(filename,sheet_name = 'Teacher Records').to_numpy()
    for i in t:
        person_dict = dict()
        #check if the entry is valid
        if np.isnan(i[0]) == True:
            break

        #generate identifier
        i[0] = int(i[0])
        key = 'T-'+str(i[0])

        #check infected or not
        for j in inf:
            if j[0] == i[0] and j[1] == i[1] and j[2] == i[2]:
                person_dict['infected'] = True

        #create individual element and insert into big dictionary
        person_dict['l_name'] = i[1]
        person_dict['f_name'] = i[2]
        person_dict['p1'] = i[3]
        person_dict['ident'] = key
        person = Person.from_dict(person_dict)
        person_class[key] = person
    
    #========================================================================================
    #TAs
    ta = pd.read_excel(filename, sheet_name = 'Teaching Assistant Records').to_numpy()
    for i in ta:
        person_dict = dict()
        #check validity of data entry
        if np.isnan(i[0]) == True:
            break
        #generate identifyer
        i[0] = int(i[0])
        key = 'TA-'+str(i[0])
        #check infection status
        for j in inf:
            if j[0] == i[0] and j[1] == i[1] and j[2] == i[2]:
                person_dict['infected'] = True
        
        #create individual element and insert into the big dictionary
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
    '''
    :param el: a string with all extracurricular activities
    :return list: extract extracurricular activites from input list and send into a list.
    '''
    if el == 'nan':
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
    print(p_class['S-566'].l_name)
    print(p_class['S-566'].f_name)
    print(p_class['S-566'].ident)
    print(p_class['S-566'].infected)
    print(p_class['S-566'].excur)
    print(p_class['S-566'].p1)
    print(p_class['S-566'].p2)
    print(p_class['S-566'].p3)
    print(p_class['S-566'].p4)
    print(p_class['S-566'].health)    
    print(p_class['S-566'].grade)
    '''
