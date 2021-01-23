class LunchGroup:

    def __init__(self, members):
        '''

        :param members: list of student ids with lunch group
        '''
        self.members = members

class Classroom:

    def __init__(self, name, lastPeriod, currentPeriod, baseEnvRate=0):
        '''
        Location class used to represent classrooms and extracurricular locations

        :param name: Name of classroom/location
        :param lastPeriod: list of student ids within this classroom in the last period
        :param currentPeriod: list of student ids within this classroom for the current period
        :param baseEnvRate: infection rate of classroom due to inhabitation of infectious individuals
        '''

        self.name = name
        self.lastPeriod = lastPeriod
        self.currentPeriod = currentPeriod
        self.baseEnvRate = baseEnvRate
        self.infectedList = None
