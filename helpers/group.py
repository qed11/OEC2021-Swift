class LunchGroup:

    def __init__(self, members):
        '''

        :param members: list of student ids with lunch group
        '''
        self.members = members

class Classroom:

    def __init__(self, lastPeriod, currentPeriod, baseEnvRate=0):
        '''
        Location class used to represent classrooms and extracurricular locations

        :param lastPeriod: list of student ids within this classroom in the last period
        :param currentPeriod: list of student ids within this classroom for the current period
        :param baseEnvRate: infection rate of classroom due to inhabitation of infectious individuals
        '''

        self.lastPeriod = lastPeriod
        self.currentPeriod = currentPeriod
        self.baseEnvRate = baseEnvRate
        self.infectedList = []
        self.lastInfected = []

def resetEnvRate(classrooms):
    '''
    Reset environment infection rate of all classrooms

    :param classrooms: dictionary of classroom objects with keys corresponding to names
    '''

    for class_name in classrooms.keys():
        classrooms[class_name].baseEnvRate = 0

def updateClassrooms(classrooms, info_dict, period):
    '''
    Method for updating classroom information based on data

    :param classrooms: dictionary of classroom objects with keys corresponding to names
    :param info_dict: dictionary of Person objects from data with keys corresponding to student ids
    :param period: current period in simulation
    '''

    class_names = ['Physics', 'Biology', 'Functions', 'Calculus', 'Philosophy', 'Art', 'Drama', 'Computer Science',
                   'Computer Engineering', 'Humanities']

    if classrooms == None:
        classrooms = {}
        for name in class_names:
            for letter in ['A', 'B']:
                in_class = []
                classroom_name = name+' '+letter
                classrooms[classroom_name] = Classroom(None, [], 0)
                # No last period for the first period

        for student_id in info_dict.keys():
            classrooms[info_dict[student_id].p1].currentPeriod.append(student_id)
            if info_dict[student_id].infected:
                classrooms[info_dict[student_id].p1].infectedList.append(student_id)

    else:
        for name in classrooms.keys():
            classrooms[name].currentPeriod = []
            classrooms[name].lastPeriod = []
            classrooms[name].infectedList = []
        for student_id in info_dict.keys():
            student_periods = [info_dict[student_id].p1, info_dict[student_id].p2, info_dict[student_id].p3,
                               info_dict[student_id].p4]

            classrooms[student_periods[period-1]].currentPeriod.append(student_id)
            classrooms[student_periods[period-2]].lastPeriod.append(student_id)
            if info_dict[student_id].infected:
                classrooms[student_periods[period-1]].infectedList.append(student_id)
                classrooms[student_periods[period-2]].infectedList.append(student_id)

    return classrooms
