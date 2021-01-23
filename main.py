from helpers.infection import infectPeriod, infectTransition, lunchTransition, infectLunch, infectExcur
from helpers.group import updateClassrooms
from helpers.reader import getDic

def main():

    infoDict = getDic('OEC2021 - School Record Book .xlsx')
    infectedList = []

    for student_id in infoDict.keys():
        if infoDict[student_id].infected:
            infectedList.append(student_id)
    classrooms = None
    baseRate = 0.01
    baseEnvRate = 0.001
    average_R = 0
    periodCount = 5

    # Separate variables to account for incubation period
    toInfect = None

    # Main Simulation Loop
    updateClassrooms(classrooms, infoDict, 1)
    periodInfect, periodR = infectPeriod(infoDict, classrooms, infectedList, baseRate, baseEnvRate)
    transitionInfect, transitionR = infectTransition(infoDict, classrooms, infectedList, baseRate/9)
    average_R += (periodR + transitionR) / 2

    #Delayed variable update to account for incubation period
    toInfect = periodInfect.extend(transitionInfect)

    updateClassrooms(classrooms, infoDict, 2)
    periodInfect, periodR = infectPeriod(infoDict, classrooms, infectedList, baseRate, baseEnvRate)
    transitionInfect, transitionR = lunchTransition(infoDict, classrooms, infectedList, baseRate/9)
    average_R += (periodR + transitionR) / 2
    # No transition after period 2

    infectedList.extend(toInfect)
    for student_id in toInfect:
        infoDict[student_id].infected = True
    toInfect = periodInfect.extend(transitionInfect)

    lunchInfect, lunchR = infectLunch(infoDict, infectedList, baseRate)
    transitionInfect, transitionR = lunchTransition(infoDict, classrooms, infectedList, baseRate / 9)
    average_R += (periodR + transitionR)/2

    infectedList.extend(toInfect)
    for student_id in toInfect:
        infoDict[student_id].infected = True
    toInfect = lunchInfect.extend(transitionInfect)

    updateClassrooms(classrooms, infoDict, 3)
    periodInfect, periodR = infectPeriod(infoDict, classrooms, infectedList, baseRate, baseEnvRate)
    transitionInfect, transitionR = infectTransition(infoDict, classrooms, infectedList, baseRate / 9)
    average_R += (periodR + transitionR) / 2

    infectedList.extend(toInfect)
    for student_id in toInfect:
        infoDict[student_id].infected = True
    toInfect = periodInfect.extend(transitionInfect)

    updateClassrooms(classrooms, infoDict, 4)
    periodInfect, periodR = infectPeriod(infoDict, classrooms, infectedList, baseRate, baseEnvRate)
    average_R += periodR

    infectedList.extend(toInfect)
    for student_id in toInfect:
        infoDict[student_id].infected = True
    toInfect = periodInfect

    excurInfect, excurR = infectExcur(infoDict, infectedList, baseRate)
    average_R += excurR

    infectedList.extend(toInfect)
    for student_id in toInfect:
        infoDict[student_id].infected = True
    toInfect = excurInfect

    # After getting home
    infectedList.extend(toInfect)
    for student_id in toInfect:
        infoDict[student_id].infected = True

    #SIBLINGS
    average_R /= periodCount

if __name__ == '__main__':
    main()