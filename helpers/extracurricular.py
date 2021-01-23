
def getExcurDict(infoDict):
    '''
    Method that gets an extracurricular dictionary
    only the first extracurricular is used

    :param infoDict: Dictionary with student ids as keys, and Person class as associated values
    
    :return dict: dictionary of {"excur_tag": [idents, ]}
    '''
    excurDict = {}
    for ident, person in infoDict:
        if person.excur:
            try:
                excurDict[person.excur[0]].append(ident)
            
            except KeyError:
                excurDict[person.excur[0]] = [ident]
    
    return excurDict

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

    # iterate through all extracurricular groups
    for excurName, peopleList in excurDict:
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