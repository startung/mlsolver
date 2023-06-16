from mlsolver.tableau import *
# from mlsolver.formula import ProofTree

formula = Or(
    And(Box(Atom('p')), Atom('r'))
    , And(Atom('r'), Diamond(Atom('q')))
)
pt = ProofTree(formula)
pt.derive()

print(pt)
assert formula.semantic(pt.kripke_structure, 's') is True