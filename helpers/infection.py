import numpy as np
import random

def infectPeriod(infoDict, classrooms, infectedList, baseRate, baseEnvRate):

    '''
    Method that updates infoDict with newly infected students - intended to be used every period

    :param infoDict: Dictionary with student ids as keys, and Person class as associated values
    :param classrooms: List of classroom classes for students in the current period
    :param infectedList: List of student ids pertaining to known infectious students
    :param baseEnvRate: Infection rate of environment per infectious individual
    :param baseRate: Base rate at which an infected individual will infect others
    '''

    for classroom in classrooms:

        # A set is used to prevent redundant entries
        toInfect = {}
        for infected in classroom.infectedList:
            for student in classroom.currentPeriod:
                if student not in classroom.infectedList:
                    randomSample = random.uniform(0, 1)
                    infectProb = augmentProb(baseRate, infoDict[student])
                    if randomSample < infectProb:
                        toInfect.add(student)

        # Second iteration of call to account for environmental factors
        if classroom.baseEnvRate != 0:
            for student in classroom.currentPeriod:
                if student not in classroom.infectedList:
                    randomSample = random.uniform(0, 1)
                    infectProb = augmentProb(classroom.baseEnvRate, infoDict[student])
                    if randomSample < infectProb:
                        toInfect.add(student)

        classroom.baseEnvRate = baseEnvRate*len(classroom.infectedList)

        toInfect = list(toInfect)
        for person in toInfect:
            # Update information dictionary
            infoDict[person].infected = True

        # Update list of infected in classroom
        classroom.infectedList = classroom.infectedList.extend(toInfect)

def augmentProb(baseRate, student):

    '''

    :param baseRate: base rate of infection
    :param student: Individual to be infected
    :return: int: updated infection probability based on given factors
    '''

    augRate = baseRate*(.25*(student.grade-9)) #9 being the youngest grade
    augRate = augRate*(1+(not student.health)*.7)
    return augRate