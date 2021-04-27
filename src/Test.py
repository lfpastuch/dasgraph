from dasgraph.Automaton import Automaton

plantaTeste = Automaton('AutoTest')

plantaTeste.addState('Origem')
plantaTeste.addState('Destino')
plantaTeste.addEvent('Ida')
plantaTeste.addEvent('Volta')

plantaTeste.addEdge('Origem','Destino','Ida')
plantaTeste.addEdge('Destino','Origem','Volta')

