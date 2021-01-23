import numpy as np
import random

def get_gradedict(infoDict):
    # function for getting a dictionary of list of idents from the infoDict
    # look down for the format of dictionary
    gradedict = {9: [], 10: [], 11: [], 12: [], "other": []}

    for ident, person in infoDict:
        if person.grade not in gradedict:
            gradedict["other"].append(ident)
        else:
            gradedict[person.grade].append(ident)
    
    return gradedict

def generate_lunchgroups(infoDict, infectedList, group_size=10, curr_grade_chance=0.90):
    '''
    :param infoDict: Dictionary with student ids as keys, and Person class as associated values
    :param infectedList: List of student ids pertaining to known infectious students
    :param group_size: Size of each lunch group
    :param curr_grade_chance: Chance of a student hanging out with their own grade
    '''
    # generate lunch groups with at least 1 infected person in them

    grades = [9, 10, 11, 12]

    lunch_groups = []

    gradedict = get_gradedict(infoDict)

    infList = infectedList.copy()

    # pops infected people from infected list, and generates a lunch group of a certain size with them in it
    while infList:
        curr_person = infoDict[infList.pop()]

        # initalize a lunch group
        temp_lg = [curr_person.ident]
        for i in range(group_size-1)
            if np.random.random() < curr_grade_chance: # if same grade
                new_person_id = gradedict[curr_person.grade].pop(random.randrange(len(gradedict[curr_person.grade])))
                if new_person_id == curr_person.ident: # if picked the same person as current person, choose a new one
                    new_person_id = gradedict[curr_person.grade].pop(random.randrange(len(gradedict[curr_person.grade])))
                
                try: # remove from infected list if we chose another infected person
                    infList.remove(new_person_id)

                temp_lg.append(new_person_id)
            else: # different grade
                grades.remove(curr_person.ident)

                random_grade = grades[random.randrange(len(grades))]
                new_person_id = gradedict[random_grade].pop(random.randrange(len(gradedict[random_grade])))

                try: # remove from infected list if we chose another infected person
                    infList.remove(new_person_id)

                grades.append(curr_person.ident)
        
        lunch_groups.append(temp_lg)
    
    return lunch_groups



