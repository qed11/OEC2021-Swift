import numpy as np
import random

def getGradedict(infoDict):
    # function for getting a dictionary of list of idents from the infoDict
    # look down for the format of dictionary
    gradedict = {9: [], 10: [], 11: [], 12: [], "other": []}

    for ident, person in infoDict.items():
        if person.grade not in gradedict:
            gradedict["other"].append(ident)
        else:
            gradedict[person.grade].append(ident)
    
    return gradedict

def getExcurDict(infoDict):
    '''
    Method that gets an extracurricular dictionary
    only the first extracurricular is used

    :param infoDict: Dictionary with student ids as keys, and Person class as associated values
    
    :return dict: dictionary of {"excur_tag": [idents, ]}
    '''
    excurDict = {}
    for ident, person in infoDict.items():
        if person.excur:
            try:
                excurDict[person.excur[0]].append(ident)
            
            except KeyError:
                excurDict[person.excur[0]] = [ident]
    
    return excurDict

def generateLunchgroups(infoDict, infectedList, groupSize=10, currGradeChance=0.90):
    '''
    :param infoDict: Dictionary with student ids as keys, and Person class as associated values
    :param infectedList: List of student ids pertaining to known infectious students
    :param groupSize: Size of each lunch group
    :param currGradeChance: Chance of a student hanging out with their own grade
    '''
    # generate lunch groups with at least 1 infected person in them

    grades = [9, 10, 11, 12]

    lunchGroups = []

    gradeDict = getGradedict(infoDict)

    infList = infectedList.copy()

    # pops infected people from infected list, and generates a lunch group of a certain size with them in it
    while infList:
        currPerson = infoDict[infList.pop()]
        if currPerson.grade > 12:
            continue
        # initalize a lunch group
        tempLg = [currPerson.ident]
        for i in range(groupSize-1):
            if np.random.random() < currGradeChance: # if same grade
                newPersonId = gradeDict[currPerson.grade].pop(random.randrange(len(gradeDict[currPerson.grade])))
                if newPersonId == currPerson.ident: # if picked the same person as current person, choose a new one
                    newPersonId = gradeDict[currPerson.grade].pop(random.randrange(len(gradeDict[currPerson.grade])))
                
                try: # remove from infected list if we chose another infected person
                    infList.remove(newPersonId)
                except:
                    pass

                tempLg.append(newPersonId)
            else: # different grade
                grades.remove(currPerson.grade)

                randomGrade = grades[random.randrange(len(grades))]
                newPersonId = gradeDict[randomGrade].pop(random.randrange(len(gradeDict[randomGrade])))

                try: # remove from infected list if we chose another infected person
                    infList.remove(newPersonId)
                except:
                    pass

                grades.append(currPerson.grade)
        
        lunchGroups.append(tempLg)
    
    return lunchGroups

def getSiblingDict(person_class:dict):
    sib = dict()
    for el in person_class:
        if person_class[el].l_name not in sib:
            sib[person_class[el].l_name] = [el]
        else:
            sib[person_class[el].l_name].append(el)
    
    for family in list(sib):
        if len(sib[family]) == 1:
            del sib[family]
    
    return sib
