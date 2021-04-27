from dasgraph.Automaton import Automaton

#Automato
plantaTeste = Automaton('AutoTest')

#Estados
plantaTeste.addState('Origem')
plantaTeste.addState('Destino')

#Eventos
plantaTeste.addEvent('Ida')
plantaTeste.addEvent('Volta')

#Arestas
plantaTeste.addEdge('Origem','Destino','Ida')
plantaTeste.addEdge('Destino','Origem','Volta')

# implementar composições de automatos:
# paralela e produto

