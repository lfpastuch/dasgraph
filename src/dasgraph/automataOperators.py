from dasgraph.automataStructure import Automaton
from _operator import index

index = 0
S = []

def eventUnion(A1,A2):
    result = []
    for event in A1.events:
        result.append(event)
    for event in A2.events:
        if not A1.getEvent(event.eventName):
            result.append(event)
    return result

def getUniqueEventNames(A1,A2):
    A1EventNames = [event.eventName for event in A1.events]
    A2EventNames = [event.eventName for event in A2.events]
    return [eventName for eventName in A1EventNames if not eventName in A2EventNames]
    

def listsIntersection(L1,L2):
    return [item for item in L1 if item in L2]

def expandProductCompStates(A,A1,A2,startingA1state,startingA2state,eventName):
    
    fromState = startingA1state.stateName + ',' + startingA2state.stateName
    
    currentA1state = A1.nextState(startingA1state.stateName,eventName)
    currentA2state = A2.nextState(startingA2state.stateName,eventName)
    
    toState = currentA1state.stateName + ',' + currentA2state.stateName
    
    if A.getState(toState) and A.getEdgeWithEvent(fromState,toState,eventName):
        return A
    elif A.getState(toState) and not A.getEdgeWithEvent(fromState,toState,eventName):
        A.addEdge(fromState,toState,eventName)
    else:
        A.addState(toState)
        A.addEdge(fromState,toState,eventName)

    A1events = A1.getPossibleEventNames(currentA1state.stateName)
    A2events = A2.getPossibleEventNames(currentA2state.stateName)
    A1A2SyncEvents = listsIntersection(A1events,A2events)
    
    for eventName in A1A2SyncEvents:
        
        A = expandProductCompStates(A,A1,A2,currentA1state,currentA2state,eventName)
        
    return A
        

def productComposition(A1,A2):
    
    A = Automaton(A1.name + 'x' + A2.name)
    
    A.events = eventUnion(A1,A2)
    
    startingA1state = A1.getInitState()
    startingA2state = A2.getInitState()
    A.addState(startingA1state.stateName + ',' + startingA2state.stateName, initState=True)
    
    startingA1events = A1.getPossibleEventNames(startingA1state.stateName)
    startingA2events = A2.getPossibleEventNames(startingA2state.stateName)
    startingA1A2SyncEvents = listsIntersection(startingA1events,startingA2events)

    for eventName in startingA1A2SyncEvents:
        
        A = expandProductCompStates(A,A1,A2,startingA1state,startingA2state,eventName)

    return A

def expandParallelCompStates(A,A1,A2,A1UniqueEvents,A2UniqueEvents,startingA1state,startingA2state,eventName):
    
    fromState = startingA1state.stateName + ',' + startingA2state.stateName
    
    currentA1state = A1.nextState(startingA1state.stateName,eventName)
    currentA2state = A2.nextState(startingA2state.stateName,eventName)
    
    toState = currentA1state.stateName + ',' + currentA2state.stateName
    
    if A.getState(toState) and A.getEdgeWithEvent(fromState,toState,eventName):
        return A
    elif A.getState(toState) and not A.getEdgeWithEvent(fromState,toState,eventName):
        A.addEdge(fromState,toState,eventName)
    else:
        A.addState(toState)
        A.addEdge(fromState,toState,eventName)

    A1events = A1.getPossibleEventNames(currentA1state.stateName)
    A2events = A2.getPossibleEventNames(currentA2state.stateName)
    A1A2SyncEvents = listsIntersection(A1events,A2events)
    possibleA1UniqueEvents = listsIntersection(A1events,A1UniqueEvents)
    possibleA2UniqueEvents = listsIntersection(A2events,A2UniqueEvents)
    possibleParallelEvents = A1A2SyncEvents + possibleA1UniqueEvents + possibleA2UniqueEvents
    
    for eventName in possibleParallelEvents:
        
        A = expandParallelCompStates(A,A1,A2,A1UniqueEvents,A2UniqueEvents,currentA1state,currentA2state,eventName)
        
    return A

def parallelComposition(A1,A2):
    
    A = Automaton(A1.name + 'II' + A2.name)
    
    A.events = eventUnion(A1,A2)
    
    A1UniqueEvents = getUniqueEventNames(A1,A2)
    A2UniqueEvents = getUniqueEventNames(A2,A1)
    
    startingA1state = A1.getInitState()
    startingA2state = A2.getInitState()
    A.addState(startingA1state.stateName + ',' + startingA2state.stateName, initState=True)
    
    startingA1events = A1.getPossibleEventNames(startingA1state.stateName)
    startingA2events = A2.getPossibleEventNames(startingA2state.stateName)
    startingA1A2SyncEvents = listsIntersection(startingA1events,startingA2events)
    possibleA1UniqueEvents = listsIntersection(startingA1events,A1UniqueEvents)
    possibleA2UniqueEvents = listsIntersection(startingA2events,A2UniqueEvents)
    possibleParallelEvents = startingA1A2SyncEvents + possibleA1UniqueEvents + possibleA2UniqueEvents

    for eventName in possibleParallelEvents:
        
        A = expandParallelCompStates(A,A1,A2,A1UniqueEvents,A2UniqueEvents,startingA1state,startingA2state,eventName)

    return A
        
def getCycles(G):
    
    global index
    global S
    
    cycles = []
    
    for state in G.states:
        if not hasattr(state,'index'):
            SCC = getCyclesCall(G,state)
            cycles.append(SCC)
            
    index = 0
    S = []
    return cycles
    
def getCyclesCall(G,state):
    
    global index
    global S
    
    state.index = index
    state.lowlink = index
    index += 1
    S.append(state)
    state.onStack = True
    
    for edge in G.edges:
        if edge.fromState.stateName == state.stateName:
            if not hasattr(edge.toState,'index'):
                SCC = getCyclesCall(G,edge.toState)
                if SCC:
                    return SCC
                state.lowlink = min(state.lowlink,edge.toState.lowlink)
            elif edge.toState.onStack:
                state.lowlink = min(state.lowlink,edge.toState.index)
    
    if state.lowlink == state.index:
        SCC = []
        while S[-1].stateName != state.stateName:
            w = S.pop()
            w.onStack = False
            SCC.append(w)
        return SCC
    return False


def isDiagnosable(G):
    
    #calcular GN, sendo produto de G (automato com evento de falha) e AN (eventos: todos menos falha)
    An = Automaton('An')
    An.addState('n', initState=True)
    for event in G.events:
        if not event.fail:
            An.addEvent(event.eventName, event.eventType, event.observable)
    Gn = productComposition(G, An)
    #retirar os eventos de falha de GN
    for event in Gn.events:
        if event.fail:
            Gn.removeEvent(event)
    #calcular GL, sendo parlelo de G e AL
    Al = Automaton('Al')
    Al.addState('n', initState=True)
    Al.addState('y')
    for event in G.events:
        if event.fail:
            Al.addEvent(event.eventName, event.eventType, event.observable, event.fail)
            Al.addEdge('n','y',event.eventName)
            Al.addEdge('y','y',event.eventName)
    Gl = parallelComposition(G,Al)
    #calcular GL', marcando todos os estados com y de GL 
    for state in Gl.states:
        if state.stateName[-1] == 'y':
            state.stateMarking = 'accepting'
    #calcular GF, sendo CoAc(GL')
    Gf = Gl
    #calcular GNR, renomeando os eventos nao observaveis de GN, adicionando R ao final do nome
    Gnr = Gn
    for event in Gnr.events:
        if not event.observable:
            event.eventName = event.eventName + 'r'
    #calcular GV, sendo paralelo de GNR com GF
    Gv = parallelComposition(Gnr,Gf)
    #procurar por ciclos de estados com y na segunda coordenada.
    loops = getCycles(G)
    #verificar se, em pelo menos um dos eventos desse ciclo, existe algum evento que não foi renomeado. Se sim, não é diagnosticavel.
    for loop in loops:
        hasY = False
        for state in loop:
            if state.stateName[-1] == 'y':
                hasY = True
        if hasY:
            for i in range(len(loop)):
                if i < (len(loop)-1):
                    edge = G.getEdge(loop[i],loop[i+1])
                else:
                    edge = G.getEdge(loop[i],loop[0])
                for event in edge.triggerEvents:
                    if event.eventName[-1] != 'r':
                        return False
    return True
