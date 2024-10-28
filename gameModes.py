"""
Implement the following game modes:

simple write-the-answer mode (the definition is given, the term should be written)
multiple choice mode (terms and four definitions from the database are given, the right one should be chosen)
match-the-term mode (four terms and their definitions are given, must be matched correctly)
"""
from store import Term, TermGroup, User, Store
import random

store = Store("database.db")

def getTermList(termGroupID):
    allTerms = store.terms.list()
    termList = []
    for term in allTerms:
        if term.group_id == termGroupID:
            termList.append(term)
    random.shuffle(termList)
    return termList

def increaseTermAnswerCount(termID, bool_isCorrectAsnwer):
    term = store.terms.get(termID)
    if bool_isCorrectAsnwer:
        term.correct_ans += 1
    term.total_ans += 1
    term.mastery_coef = term.correct_ans / term.total_ans
    store.terms.update(term)

def gameMode2(termGroupID):
    termList = getTermList(termGroupID)
    termList2 = []
    for term in termList:
        termData = {
                "id": term.id,
                "term": term.term,
                "correctDefinition": None,
                "definitions": ["", "", "", ""]
            }
        termData["correctDefinition"] = random.randint(0, 3)
        termData["definitions"][termData["correctDefinition"]] = term.definition
        
        unusedDefinitions = termList.copy()
        for i in range(len(unusedDefinitions)):
            if(unusedDefinitions[i].definition == term.definition):
                remove = i
        unusedDefinitions.pop(remove)
        
        for i in range(4):
            if termData["definitions"][i] == "":
                randomDefinition = random.randint(0, len(unusedDefinitions)-1)
                termData["definitions"][i] = unusedDefinitions[randomDefinition].definition
                unusedDefinitions.pop(randomDefinition)          
        termList2.append(termData)
    return termList2

def gameMode3(termGroupID):
    termList = getTermList(termGroupID)
    termList3 = []   
    for x in range(0, len(termList)//4):
        termData = {
                "id": [None, None, None, None],
                "term": ["", "", "", ""],
                "definition": ["", "", "", ""]
            }
        
        for i in range(4):
            termData["id"][i] = termList[0].id
            termData["term"][i] = termList[0].term
            termData["definition"][i] = termList[0].definition
            termList.pop(0)
        termList3.append(termData)
    return termList3

"""
lietotajs = store.users.create(User(username="lietotajs1"))
valstis = store.term_groups.create(TermGroup(name="Valstis", user_id=lietotajs.id))
store.terms.create(Term(term="Latvija", definition="Valsts starp Igauniju un Lietuvu", group_id=valstis.id))
store.terms.create(Term(term="Igaunija", definition="Valsts virs Latvijas", group_id=valstis.id))
store.terms.create(Term(term="Lietuva", definition="Valsts zem Latvijas", group_id=valstis.id))
store.terms.create(Term(term="Anglija", definition="Valsts, kurā runā angliski", group_id=valstis.id))
store.terms.create(Term(term="Vācija", definition="Valsts, kurā dzivo vācieši", group_id=valstis.id))
pilsetas = store.term_groups.create(TermGroup(name="Pilsetas", user_id=lietotajs.id))
store.terms.create(Term(term="Riga", definition="Latvijas galvaspilseta", group_id=pilsetas.id))

print(getTermList(1))
increaseTermAnswerCount(1, True)
increaseTermAnswerCount(1, False)
list = getTermList(1)
print('\n')


gm2 = gameMode2(1)
for i in gm2:
    print(i)
print('\n')

gm3 = gameMode3(1)
for i in gm3:
    print(i)
print('\n')
"""
