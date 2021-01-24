import numpy as np
from .utils import getGradedict, generateLunchgroups, getExcurDict,getSiblingDict
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

    for class_name in classrooms.keys():

        classroom = classrooms[class_name]
        # A set is used to prevent redundant entries
        toInfect = set()
        for _ in classroom.infectedList:
            for student in classroom.currentPeriod:
                if student not in classroom.infectedList:
                    randomSample = np.random.random()
                    infectProb = augmentProb(baseRate, infoDict[student])
                    if randomSample < infectProb:
                        toInfect.add(student)

        # Second iteration of call to account for environmental factors
        if classroom.baseEnvRate != 0:
            for student in classroom.currentPeriod:
                if student not in classroom.infectedList:
                    randomSample = np.random.random()
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

    for class_name in classrooms.keys():

        classroom = classrooms[class_name]
        # A set is used to prevent redundant entries
        toInfect = set()
        for _ in classroom.infectedList:
            for student in classroom.lastPeriod:
                if student not in classroom.lastInfected:
                    randomSample = np.random.random()
                    infectProb = augmentProb(baseRate, infoDict[student])
                    if randomSample < infectProb:
                        toInfect.add(student)

        for _ in classroom.lastInfected:
            for student in classroom.currentPeriod:
                if student not in classroom.infectedList:
                    randomSample = np.random.random()
                    infectProb = augmentProb(baseRate, infoDict[student])
                    if randomSample < infectProb:
                        toInfect.add(student)

        toInfect = list(toInfect)
        newlyInfected += len(toInfect)

        # Update list of people to be infected next period
        nextPeriod.extend(toInfect)

    return nextPeriod, newlyInfected/len(infectedList)

def lunchTransition(infoDict, infectedList, baseRate):
    
    '''
    infectTransition copy that considers possible interactions from any student to any other student

    :param infoDict: Dictionary with student ids as keys, and Person class as associated values
    :param infectedList: List of student ids pertaining to known infectious students
    :param baseRate: Base rate at which an infected individual will infect others

    :return list: List of student ids that represent students newly infected this period
    :return int: Total number of newly infected individuals over total number of infected individuals at period start
    '''

    newlyInfected = 0
    toInfect = set()

    for infected in infectedList:
        for student in infoDict.keys():
            if not infoDict[student].infected:
                randomSample = np.random.random()
                infectProb = augmentProb(baseRate, infoDict[student])
                if randomSample < infectProb:
                    toInfect.add(student)

    toInfect = list(toInfect)
    newlyInfected += len(toInfect)

    return toInfect, newlyInfected / len(infectedList)

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
    newlyInfected = 0

    for lunchGroup in lunchGroups:

        # A set is used to prevent redundant entries
        toInfect = set()
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

    return toInfect, newlyInfected/len(infectedList)

def infectExcur(infoDict, infectedList, baseRate):
    '''
    Method that returns a list of infected students from extracurriculars

    :param infoDict: Dictionary with student ids as keys, and Person class as associated values
    :param infectedList: List of student ids pertaining to known infectious students
    :param baseRate: Base rate at which an infected individual will infect others

    :return list: List of student ids that represent students newly infected this period
    :return int: Total number of newly infected individuals over total number of infected individuals at period start
    '''

    excurDict = getExcurDict(infoDict)
    toInfect = set()
    newlyInfected = 0

    # iterate through all extracurricular groups
    for excurName, peopleList in excurDict.items():
        for infected_id in peopleList:
            # find infected people in each group
            if infected_id in infectedList:
                for student in peopleList:
                    # infect non infected people based on chance
                    if student not in infectedList:
                        randomSample = np.random.random()
                        infectProb = augmentProb(baseRate, infoDict[student])
                        if randomSample < infectProb:
                            toInfect.add(student)
    
    toInfect = list(toInfect)
    newlyInfected += len(toInfect)
    
    return toInfect, newlyInfected/len(infectedList)

def augmentProb(baseRate, student):

    """
    :param baseRate: base rate of infection
    :param student: Individual to be infected
    :return: int: updated infection probability based on given factors
    """

    augRate = baseRate*(.25*(student.grade-9)) #9 being the youngest grade
    augRate = augRate*(1+(not student.health)*.7)
    return augRate

def infectSiblings(infoDict,infectedList,baseRate):
    '''
    Method that returns a list of infected students from sibling infections

    :param infoDict: Dictionary with student ids as keys, and Person class as associated values
    :param infectedList: List of student ids pertaining to known infectious students
    :param baseRate: Base rate at which an infected individual will infect others

    :return list: List of student ids that represent students newly infected this period
    :return int: Total number of newly infected individuals over total number of infected individuals at period start
    '''
    
    siblingDict = getSiblingDict(infoDict)
    toInfect = set()
    newlyInfected = 0

     # iterate through all sibling groups
    for lName, peopleList in siblingDict.items():
        for infected_id in peopleList:
            # find infected people in each family
            if infected_id in infectedList:
                for student in peopleList:
                    # infect non infected people based on chance
                    if student not in infectedList:
                        randomSample = np.random.random()
                        infectProb = augmentProb(baseRate, infoDict[student])
                        if randomSample < infectProb:
                            toInfect.add(student)
    
    toInfect = list(toInfect)
    newlyInfected += len(toInfect)
    
    return toInfect, newlyInfected/len(infectedList)