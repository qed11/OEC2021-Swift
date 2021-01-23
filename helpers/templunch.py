import numpy as np
import random

def getGradedict(infoDict):
    # function for getting a dictionary of list of idents from the infoDict
    # look down for the format of dictionary
    gradedict = {9: [], 10: [], 11: [], 12: [], "other": []}

    for ident, person in infoDict:
        if person.grade not in gradedict:
            gradedict["other"].append(ident)
        else:
            gradedict[person.grade].append(ident)
    
    return gradedict

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

        # initalize a lunch group
        tempLg = [currPerson.ident]
        for i in range(groupSize-1)
            if np.random.random() < currGradeChance: # if same grade
                newPersonId = gradeDict[currPerson.grade].pop(random.randrange(len(gradeDict[currPerson.grade])))
                if newPersonId == currPerson.ident: # if picked the same person as current person, choose a new one
                    newPersonId = gradeDict[currPerson.grade].pop(random.randrange(len(gradeDict[currPerson.grade])))
                
                try: # remove from infected list if we chose another infected person
                    infList.remove(newPersonId)

                tempLg.append(newPersonId)
            else: # different grade
                grades.remove(currPerson.ident)

                randomGrade = grades[random.randrange(len(grades))]
                newPersonId = gradeDict[randomGrade].pop(random.randrange(len(gradeDict[randomGrade])))

                try: # remove from infected list if we chose another infected person
                    infList.remove(newPersonId)

                grades.append(currPerson.ident)
        
        lunchGroups.append(tempLg)
    
    return lunchGroups

def infectLunch(infoDict, infectedList, baseRate):

    '''
    Method that updates infoDict with newly infected students - intended to be used every period

    :param infoDict: Dictionary with student ids as keys, and Person class as associated values
    :param infectedList: List of student ids pertaining to known infectious students
    :param baseRate: Base rate at which an infected individual will infect others

    :return list: List of student ids that represent students newly infected this period
    :return int: Total number of newly infected individuals over total number of infected individuals at period start
    '''

    lunchGroups = generateLunchgroups(infoDict, infectedList, groupSize=10)

    for lunchGroup in lunchGroups:

        # A set is used to prevent redundant entries
        toInfect = {}
        for infectedId in lunchGroup:
            if infoDict[infectedId].infected:
                for studentId in lunchGroup:
                    if infoDict[studentId].infected == False:
                        randomSample = np.random.random()
                        infectProb = augmentProb(baseRate, infoDict[studentId])
                        if randomSample < infectProb:
                            toInfect.add(studentId)

        toInfect = list(toInfect)
        newlyInfected += len(toInfect)

        # Update list of people to be infected next period
        nextPeriod.extend(toInfect)

    return nextPeriod, newlyInfected/len(infectedList)

def augmentProb(baseRate, student):

    '''

    :param baseRate: base rate of infection
    :param student: Individual to be infected
    :return: int: updated infection probability based on given factors
    '''

    augRate = baseRate*(.25*(student.grade-9)) #9 being the youngest grade
    augRate = augRate*(1+(not student.health)*.7)
    return augRate