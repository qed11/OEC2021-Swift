from helpers.infection import infectPeriod, infectTransition, lunchTransition, infectLunch, infectExcur
from helpers.group import updateClassrooms
from helpers.reader import getDic
import copy
import time

def main():

    infoDict = getDic('OEC2021 - School Record Book .xlsx')
    backupDic = copy.deepcopy(infoDict)
    original_infect = []
    for student_id in infoDict.keys():
        if infoDict[student_id].infected:
            original_infect.append(student_id)

    baseRate = 0.1
    baseEnvRate = 0.001
    periodCount = 5
    global_inf = 0
    global_R = 0
    eps_count = 100

    for _ in range(1, eps_count):

        infectedList = []
        infoDict = copy.deepcopy(backupDic)
        for student_id in infoDict.keys():
            infoDict[student_id].infected = False
        for student_id in original_infect:
            infoDict[student_id].infected = True
        for student in original_infect:
            infectedList.append(student)

        average_R = 0
        # Separate variables to account for incubation period
        toInfect = None
        classrooms = None
        # Main Simulation Loop
        classrooms = updateClassrooms(classrooms, infoDict, 1)
        # Infect period 1
        periodInfect, periodR = infectPeriod(infoDict, classrooms, infectedList, baseRate, baseEnvRate)
        updateClassrooms(classrooms, infoDict, 2)
        # Infect period 1-2 transition
        transitionInfect, transitionR = infectTransition(infoDict, classrooms, infectedList, baseRate/9)
        average_R += (periodR + transitionR) / 2

        #print("Period infect {}: Transition Infect: {}".format(periodInfect, transitionInfect))
        #Delayed variable update to account for incubation period
        periodInfect.extend(transitionInfect)
        toInfect = periodInfect
        #print("To infect: {}".format(toInfect))

        # Infect period 2
        periodInfect, periodR = infectPeriod(infoDict, classrooms, infectedList, baseRate, baseEnvRate)
        # Infect period 2-lunch transition
        transitionInfect, transitionR = lunchTransition(infoDict, infectedList, baseRate/9)
        average_R += (periodR + transitionR) / 2

        #print("To infect: {} Infected List: {}".format(toInfect, infectedList))
        infectedList.extend(toInfect)
        for student_id in toInfect:
            infoDict[student_id].infected = True
        periodInfect.extend(transitionInfect)
        toInfect = periodInfect

        # Infect Lunch
        lunchInfect, lunchR = infectLunch(infoDict, infectedList, baseRate)
        # Infect lunch-period 3 transition
        transitionInfect, transitionR = lunchTransition(infoDict, infectedList, baseRate / 9)
        average_R += (periodR + transitionR)/2

        infectedList.extend(toInfect)
        for student_id in toInfect:
            infoDict[student_id].infected = True
        lunchInfect.extend(transitionInfect)
        toInfect = lunchInfect

        updateClassrooms(classrooms, infoDict, 3)
        # Infect period 3
        periodInfect, periodR = infectPeriod(infoDict, classrooms, infectedList, baseRate, baseEnvRate)
        updateClassrooms(classrooms, infoDict, 4)
        # Infect period 3-4 transition
        transitionInfect, transitionR = infectTransition(infoDict, classrooms, infectedList, baseRate / 9)
        average_R += (periodR + transitionR) / 2

        infectedList.extend(toInfect)
        for student_id in toInfect:
            infoDict[student_id].infected = True
        periodInfect.extend(transitionInfect)
        toInfect = periodInfect

        #Infect period 4
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
        infected_count = len(infectedList)
        global_R += average_R
        global_inf += infected_count

    print("Multi sample R: {}".format(global_R/eps_count))
    print("Multi sample infection average: {}".format(global_inf/eps_count))

if __name__ == '__main__':
    main()