from dasgraph.Event import Event
from dasgraph.State import State
from dasgraph.Edge import Edge

class Automaton(object):
    
    states = []
    events = []
    edges = []
    name = ''

    def __init__(self, automatonName, automatonKind='Plant', automatonDeterminism=True):
        
        self.name = automatonName
        self.kind = automatonKind
        self.deterministic = automatonDeterminism
        
    def addEvent(self, eventName, eventType='Controllable', eventObservability=True):
        self.events.append(Event(eventName,eventType,eventObservability))
        
    def addState(self, stateName, stateMarking=''):
        self.states.append(State(stateName,stateMarking))
        
    def getState(self,stateName):
        for state in self.states:
            if state.stateName == stateName:
                return state
    
    def getEvent(self,eventName):
        for event in self.events:
            if event.eventName == eventName:
                return event

    def addEdge(self, fromStateName, toStateName, triggerEventName):
        fromState = self.getState(fromStateName)
        toState = self.getState(toStateName)
        triggerEvent = self.getEvent(triggerEventName)
        self.edges.append(Edge(fromState,toState,triggerEvent))
    
    