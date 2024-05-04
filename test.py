from pysat.card import *

encoding = EncType.seqcounter
lits = [1,2,3,5]
bound = 1

# cnf1 = CardEnc.atleast(lits=lits, bound=bound, encoding=encoding)
# print(cnf1.clauses)

# cnf2 = CardEnc.atmost(lits=lits, bound=bound, encoding=encoding)
# print(cnf2.clauses)

cnf3 = CardEnc.equals(lits=lits, bound=bound, encoding=encoding)
print((cnf3.clauses))
print(len(cnf3.clauses))




    