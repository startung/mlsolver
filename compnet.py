from mlsolver.kripke import World, KripkeStructure
from mlsolver.model import add_symmetric_edges, add_reflexive_edges
import mlsolver.model as Model
from mlsolver.formula import Atom, Box, Or, Box_a, And, Not, Box_star

class WiseMenWithHat:
    """
    Class models the Kripke structure of the "Three wise men example.
    """

    knowledge_base = []

    def __init__(self):
        worlds = [
            World('RWW', {'1:R': True, '2:W': True, '3:W': True}),
            World('RRW', {'1:R': True, '2:R': True, '3:W': True}),
            World('RRR', {'1:R': True, '2:R': True, '3:R': True}),
            World('WRR', {'1:W': True, '2:R': True, '3:R': True}),

            World('WWR', {'1:W': True, '2:W': True, '3:R': True}),
            World('RWR', {'1:R': True, '2:W': True, '3:R': True}),
            World('WRW', {'1:W': True, '2:R': True, '3:W': True}),
            World('WWW', {'1:W': True, '2:W': True, '3:W': True}),
        ]

        relations = {
            '1': {('RWW', 'WWW'), ('RRW', 'WRW'), ('RWR', 'WWR'), ('WRR', 'RRR')},
            '2': {('RWR', 'RRR'), ('RWW', 'RRW'), ('WRR', 'WWR'), ('WWW', 'WRW')},
            '3': {('WWR', 'WWW'), ('RRR', 'RRW'), ('RWW', 'RWR'), ('WRW', 'WRR')}
        }

        relations.update(add_reflexive_edges(worlds, relations))
        relations.update(add_symmetric_edges(relations))

        self.ks = KripkeStructure(worlds, relations)

        # Wise man ONE does not know whether he wears a red hat or not
        self.knowledge_base.append(And(Not(Box_a('1', Atom('1:R'))), Not(Box_a('1', Not(Atom('1:R'))))))

        # This announcement implies that either second or third wise man wears a red hat.
        self.knowledge_base.append(Box_star(Or(Atom('2:R'), Atom('3:R'))))

        # Wise man TWO does not know whether he wears a red hat or not
        self.knowledge_base.append(And(Not(Box_a('2', Atom('2:R'))), Not(Box_a('2', Not(Atom('2:R'))))))

        # This announcement implies that third men has be the one, who wears a red hat
        self.knowledge_base.append(Box_a('3', Atom('3:R')))

def test_add_symmetric_edges():
    relations = {'1': {('a', 'b')}}
    expected_relations = {'1': {('a', 'b'), ('b', 'a')}}
    relations.update(Model.add_symmetric_edges(relations))
    assert expected_relations == relations


def test_add_symmetric_is_already():
    relations = {'1': {('a', 'b'), ('b', 'a')}}
    expected_relations = {'1': {('a', 'b'), ('b', 'a')}}
    relations.update(Model.add_symmetric_edges(relations))
    assert expected_relations == relations


def test_add_reflexive_edges_one_agent():
    worlds = [World('WR', {}), World('RW', {})]
    relations = {'1': {('WR', 'RW')}}
    expected_relations = {'1': {('WR', 'RW'), ('RW', 'RW'), ('WR', 'WR')}}
    relations = Model.add_reflexive_edges(worlds, relations)
    assert expected_relations == relations


def test_add_reflexive_edges_two_agents():
    worlds = [World('WR', {}), World('RW', {})]
    relations = {'1': {('WR', 'RW')}, '2': {('RW', 'WR')}}
    expected_relations = {'1': {('WR', 'RW'), ('WR', 'WR'), ('RW', 'RW')},
                          '2': {('RW', 'WR'), ('RW', 'RW'), ('WR', 'WR')}}
    relations = Model.add_reflexive_edges(worlds, relations)
    assert expected_relations == relations


def test_solve_with_model_first_ann():
    wise_men_model = WiseMenWithHat()
    ks = wise_men_model.ks
    model = ks.solve(wise_men_model.knowledge_base[1])
    print(model)

    worlds_expected = [
        World('RRW', {'1:R': True, '2:R': True, '3:W': True}),
        World('RRR', {'1:R': True, '2:R': True, '3:R': True}),
        World('WRR', {'1:W': True, '2:R': True, '3:R': True}),

        World('WWR', {'1:W': True, '2:W': True, '3:R': True}),
        World('RWR', {'1:R': True, '2:W': True, '3:R': True}),
        World('WRW', {'1:W': True, '2:R': True, '3:W': True}),
    ]

    relations_expected = {
        '1': {('RRW', 'WRW'), ('RWR', 'WWR'), ('WRR', 'RRR')},
        '2': {('RWR', 'RRR'), ('WRR', 'WWR')},
        '3': {('RRR', 'RRW'), ('WRW', 'WRR')}
    }

    relations_expected.update(Model.add_reflexive_edges(worlds_expected, relations_expected))
    relations_expected.update(Model.add_symmetric_edges(relations_expected))
    ks_expected = KripkeStructure(worlds_expected, relations_expected)
    print(ks_expected)
    assert ks_expected.__eq__(model)


def test_solve_with_model_second_ann():
    wise_men_model = WiseMenWithHat()
    ks = wise_men_model.ks
    model = ks.solve(wise_men_model.knowledge_base[1])
    model = model.solve(wise_men_model.knowledge_base[3])

    worlds_expected = [
        World('RRR', {'1:R': True, '2:R': True, '3:R': True}),
        World('WRR', {'1:W': True, '2:R': True, '3:R': True}),

        World('WWR', {'1:W': True, '2:W': True, '3:R': True}),
        World('RWR', {'1:R': True, '2:W': True, '3:R': True}),
    ]

    relations_expected = {
        '1': {('RWR', 'WWR'), ('WRR', 'RRR')},
        '2': {('RWR', 'RRR'), ('WRR', 'WWR')},
        '3': set()
    }

    relations_expected.update(Model.add_reflexive_edges(worlds_expected, relations_expected))
    relations_expected.update(Model.add_symmetric_edges(relations_expected))
    ks_expected = KripkeStructure(worlds_expected, relations_expected)
    # assert ks_expected.__eq__(model)
    return model, ks_expected


model, ks_expected = test_solve_with_model_second_ann()

print("model=", model)
print("ks_expected=", ks_expected)
print(f"Equal: {ks_expected.__eq__(model)}")