from helpers.infection import infectPeriod, infectTransition, lunchTransition, infectLunch, infectExcur, infectSiblings
from helpers.group import updateClassrooms, resetEnvRate
from helpers.reader import getDic
import copy
import numpy as np
import csv
import time

def main():

    infoDict = getDic('OEC2021 - School Record Book .xlsx')
    backupDic = copy.deepcopy(infoDict)
    original_infect = []
    for student_id in infoDict.keys():
        if infoDict[student_id].infected:
            original_infect.append(student_id)

    infectionDict = {}
    for student_id in infoDict.keys():
        infectionDict[student_id] = 0

    baseRate = 0.095
    baseEnvRate = 0.01
    periodCount = 5
    global_inf = 0
    global_R = 0
    eps_count = 5000

    for eps in range(1, eps_count+1):

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
        average_R += periodR

        #print("Period infect {}: Transition Infect: {}".format(periodInfect, transitionInfect))
        #Delayed variable update to account for incubation period
        periodInfect.extend(transitionInfect)
        toInfect = periodInfect
        #print("To infect: {}".format(toInfect))

        # Infect period 2
        periodInfect, periodR = infectPeriod(infoDict, classrooms, infectedList, baseRate, baseEnvRate)
        # Infect period 2-lunch transition
        transitionInfect, transitionR = lunchTransition(infoDict, infectedList, baseRate/9)
        average_R += periodR

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
        average_R += periodR

        infectedList.extend(toInfect)
        for student_id in toInfect:
            infoDict[student_id].infected = True
        lunchInfect.extend(transitionInfect)
        toInfect = lunchInfect

        updateClassrooms(classrooms, infoDict, 3)
        # Reset env
        resetEnvRate(classrooms)

        # Infect period 3
        periodInfect, periodR = infectPeriod(infoDict, classrooms, infectedList, baseRate, baseEnvRate)
        updateClassrooms(classrooms, infoDict, 4)
        # Infect period 3-4 transition
        transitionInfect, transitionR = infectTransition(infoDict, classrooms, infectedList, baseRate / 9)
        average_R += periodR

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
        #average_R += excurR

        infectedList.extend(toInfect)
        for student_id in toInfect:
            infoDict[student_id].infected = True
        toInfect = excurInfect

        siblingInfect, siblingR = infectSiblings(infoDict, infectedList, baseRate)
        #average_R += siblingR

        toInfect += siblingInfect

        # After getting home
        infectedList.extend(toInfect)
        for student_id in toInfect:
            infoDict[student_id].infected = True

        #SIBLINGS
        average_R /= periodCount
        infected_count = len(infectedList)
        global_R += average_R
        global_inf += infected_count
        for student_id in infectionDict.keys():
            if infoDict[student_id].infected:
                infectionDict[student_id] += 1

        if (eps+1) % 10 == 0:
            idList = []
            infectionList = []
            for student_id in infectionDict.keys():
                idList.append(student_id)
                infectionList.append(infectionDict[student_id])
            idx_list = np.argsort(infectionList)[::-1]
            print("Highest probability of infection, Iteration: {}".format(eps+1))
            for i, idx in enumerate(idx_list):
                print("{}. Student {}, Infection Chance {:.2f}".format(i + 1, idList[idx], 100 * infectionList[idx] / eps))
                if i == 50:
                    break

            time.sleep(0.5)

    #print("Infection dict: {}".format(infectionDict))
    print("Multi sample R: {}".format(global_R/eps_count))
    print("Multi sample infection average: {}".format(global_inf/eps_count))
    idList = []
    infectionList = []
    for student_id in infectionDict.keys():
        idList.append(student_id)
        infectionList.append(infectionDict[student_id])
    idx_list = np.argsort(infectionList)[::-1]

    '''
    with open('infection_probability.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Rankings", "Student ID", "Likelihood of Infection"])
        for i, idx in enumerate(idx_list):
            writer.writerow([i+1, idList[idx], infectionList[idx]/eps_count])
    '''




if __name__ == '__main__':
    main()