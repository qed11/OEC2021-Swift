import numpy as np
import random

def infectPeriod(infoDict, classrooms, infectedList, baseRate, baseEnvRate):

    '''
    Method that returns a list of students to be infected - called every period

    :param infoDict: Dictionary with student ids as keys, and Person class as associated values
    :param classrooms: List of classroom classes for students in the current period
    :param infectedList: List of student ids pertaining to known infectious students
    :param baseEnvRate: Infection rate of environment per infectious individual
    :param baseRate: Base rate at which an infected individual will infect others

    :return list: List of student ids that represent students newly infected this period
    :return int: Total number of newly infected individuals over total number of infected individuals at period start
    '''

    newlyInfected = 0
    nextPeriod = []

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

        classroom.baseEnvRate = baseEnvRate * len(classroom.infectedList)

        toInfect = list(toInfect)
        newlyInfected += len(toInfect)

        # Update list of people to be infected next period
        nextPeriod.extend(toInfect)

    return nextPeriod, newlyInfected / len(infectedList)


def infectTransition(infoDict, classrooms, infectedList, baseRate):

    '''
    infectPeriod sample that should use lower baseRate, and uses lastPeriod in consideration of infecting others

    :param infoDict: Dictionary with student ids as keys, and Person class as associated values
    :param classrooms: List of classroom classes for students in the current period
    :param infectedList: List of student ids pertaining to known infectious students
    :param baseRate: Base rate at which an infected individual will infect others

    :return list: List of student ids that represent students newly infected this period
    :return int: Total number of newly infected individuals over total number of infected individuals at period start
    '''

    newlyInfected = 0
    nextPeriod = []

    for classroom in classrooms:

        # A set is used to prevent redundant entries
        toInfect = {}
        for _ in classroom.infectedList:
            for student in classroom.lastPeriod:
                if student not in classroom.lastInfected:
                    randomSample = random.uniform(0, 1)
                    infectProb = augmentProb(baseRate, infoDict[student])
                    if randomSample < infectProb:
                        toInfect.add(student)

        for _ in classroom.lastInfected:
            for student in classroom.currentPeriod:
                if student not in classroom.infectedList:
                    randomSample = random.uniform(0, 1)
                    infectProb = augmentProb(baseRate, infoDict[student])
                    if randomSample < infectProb:
                        toInfect.add(student)

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