'''
File for people definition
'''

class Person():
    def __init__(self, l_name, f_name, grade, p1, p2, p3, p4, health, excur, ident, infected):
        self.l_name = l_name
        self.f_name = f_name
        self.grade = grade
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.health = health
        self.excur = excur
        self.ident = ident
        self.infected = infected

    @classmethod
    def from_dict(cls, person_dict):
        # function for creating a person from a dictionary containing their attributes
        if "grade" not in person_dict:
            person_dict["grade"] = 20
            # default grade for teachers and TAs
        if "health" not in person_dict:
            person_dict["health"] = False
            # default health
        if "excur" not in person_dict:
            person_dict["excur"] = []
            # default extracurriculars
        if "infected" not in person_dict:
            person_dict["infected"] = False
            # default infected value
        if "p2" not in person_dict:
            person_dict["p2"] = person_dict["p1"]
            # for teachers, distributes p1 to all periods
        if "p3" not in person_dict:
            person_dict["p3"] = person_dict["p1"]
            # for teachers, distributes p1 to all periods
        if "p4" not in person_dict:
            person_dict["p4"] = person_dict["p1"]
            # for teachers, distributes p1 to all periods

        return cls.__init__(person_dict["l_name"], person_dict["f_name"], person_dict["grade"], 
                            person_dict["p1"], person_dict["p2"], person_dict["p3"], person_dict["p4"],
                            person_dict["excur"], person_dict["ident"], person_dict["infected"])