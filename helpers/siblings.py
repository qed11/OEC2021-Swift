'''Utility functions'''
from reader import getDic
def getSiblingDict(person_class:dict):
    sib = dict()
    for el in person_class:
        if person_class[el].l_name not in sib:
            sib[person_class[el].l_name] = [el]
        else:
            sib[person_class[el].l_name].append(el)
    '''
    for family in sib:
        if len(sib[family]) == 1:
            sib.pop(family)
    '''
    return sib

def infectSiblings(infoDict,infectedList,baseRate):
    
    siblingDict = getSiblingDict(infoDict)

if __name__=='__main__':
    l = getDic('OEC2021 - School Record Book .xlsx')
    siblingDict = getSiblingDict(l)
    print(siblingDict)