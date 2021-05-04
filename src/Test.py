from dasgraph.automataStructure import Automaton
from dasgraph.automataOperators import productComposition,parallelComposition

G1 = Automaton('G1')
G1.addState('x', stateMarking = 'accepting', initState = True)
G1.addState('y')
G1.addState('z')
G1.addEvent('a')
G1.addEvent('b')
G1.addEvent('g')
G1.addEdge('x','x','a')
G1.addEdge('x','z','g')
G1.addEdge('z','z','b')
G1.addEdge('z','y','a')
G1.addEdge('z','y','b')
G1.addEdge('z','y','g')
G1.addEdge('y','y','b')
G1.addEdge('y','x','a')

G2 = Automaton('G2')
G2.addState('0', initState = True)
G2.addState('1', stateMarking = 'accepting')
G2.addEvent('a')
G2.addEvent('b')
G2.addEdge('0','0','b')
G2.addEdge('0','1','a')
G2.addEdge('1','1','a')
G2.addEdge('1','0','b')

#Produto

G1xG2 = productComposition(G1,G2)
print('******* Composição Produto ********')
G1xG2.printAutomata()   
print('***********************************')

#Paralelo

G1IIG2 = parallelComposition(G1,G2)
print('******* Composição Paralela ******* ')
G1IIG2.printAutomata()
print('***********************************')
