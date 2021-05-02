class Event(object):

    def __init__(self, eventName, eventType, eventObservability):
        
        self.eventName = eventName
        self.eventType = eventType
        self.observable = eventObservability
        
class State(object):

    def __init__(self, stateName, stateMarking, initState):
        
        self.stateName = stateName
        self.stateMarking = stateMarking
        self.initState = initState
        
class Edge(object):
    
    def __init__(self, fromState, toState, triggerEvent):
        self.fromState = fromState
        self.toState = toState
        self.triggerEvents = []
        self.triggerEvents.append(triggerEvent)
        
class RepeatedNameError(Exception):
    pass

class NotMarkingMode(Exception):
    pass

class NoState(Exception):
    pass

class NoEvent(Exception):
    pass

class Automaton(object):

    def __init__(self, automatonName, automatonKind='Plant', automatonDeterminism=True):
        
        self.states = []
        self.events = []
        self.edges = []
        self.name = automatonName
        self.kind = automatonKind
        self.deterministic = automatonDeterminism
        
    def getState(self,stateName):
        for state in self.states:
            if state.stateName == stateName:
                return state
        return False
    
    def getInitState(self):
        for state in self.states:
            if state.initState:
                return state
        raise NoState('There is no initial state defined in ' + self.name + '.')
    
    def getPossibleEventNames(self,stateName):
        if not self.getState(stateName):
            raise NoState('The state "' + stateName + '" does not exist.')
        possible = []
        for edge in self.edges:
            if stateName == edge.fromState.stateName:
                for event in edge.triggerEvents:
                    possible.append(event.eventName)
        return possible
    
    def getEvent(self,eventName):
        for event in self.events:
            if event.eventName == eventName:
                return event
        return False
    
    def getEdge(self, fromStateName, toStateName):
        for edge in self.edges:
            if edge.fromState.stateName == fromStateName and edge.toState.stateName == toStateName:
                return edge
        return False
    
    def getEdgeWithEvent(self, fromStateName, toStateName, eventName):
        for edge in self.edges:
            if edge.fromState.stateName == fromStateName and edge.toState.stateName == toStateName:
                for event in edge.triggerEvents:
                    if event.eventName == eventName:
                        return edge
        return False
            
    def addEvent(self, eventName, eventType='Controllable', eventObservability=True):
        if not self.getEvent(eventName):
            self.events.append(Event(eventName,eventType,eventObservability))
        else:
            raise RepeatedNameError('The event name "' + eventName + '" is taken. Use a different name for this event or delete the former.')
        
    def addState(self, stateName, stateMarking='', initState = False):
        if not self.getState(stateName):
            if stateMarking == '' or stateMarking == 'accepting' or stateMarking == 'forbidden': 
                self.states.append(State(stateName,stateMarking,initState))
            else:
                raise NotMarkingMode('The marking mode "' + stateMarking + '" does not exist. Try "accepting" or "forbidden" or leave it blank.')
        else:
            raise RepeatedNameError('The state name "' + stateName + '" is taken. Use a different name for this state or delete the former.')

    def addEdge(self, fromStateName, toStateName, triggerEventName):
        edge = self.getEdge(fromStateName, toStateName)
        if not edge:
            if self.getState(fromStateName):
                fromState = self.getState(fromStateName)
            elif not self.getState(fromStateName):
                raise NoState('The specified fromState "' + fromStateName + '" is not defined.')
            if self.getState(toStateName):
                toState = self.getState(toStateName)
            elif not self.getState(toStateName):
                raise NoState('The specified toState "' + toStateName + '" is not defined.')
            if self.getEvent(triggerEventName):
                triggerEvent = self.getEvent(triggerEventName)
            elif not self.getEvent(triggerEventName):
                raise NoEvent('The specified triggerEvent "' + triggerEventName + '" is not defined.')
            self.edges.append(Edge(fromState,toState,triggerEvent))
        else:
            if self.getEvent(triggerEventName):
                triggerEvent = self.getEvent(triggerEventName)
            elif not self.getEvent(triggerEventName):
                raise NoEvent('The specified triggerEvent "' + triggerEventName + '" is not defined.')    
            if triggerEvent not in edge.triggerEvents:
                edge.triggerEvents.append(triggerEvent)
                
    def nextState(self,stateName,eventName):
        for edge in self.edges:
            if stateName == edge.fromState.stateName:
                for event in edge.triggerEvents:
                    if eventName == event.eventName:
                        return edge.toState
        return self.getState(stateName)
    