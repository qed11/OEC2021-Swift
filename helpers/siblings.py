'''Utility functions'''

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

def infectSiblings(infoDict,infectedList,baseRate):
    
    siblingDict = getSiblingDict(infoDict)

     # iterate through all extracurricular groups
    for excurName, peopleList in siblingDict:
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