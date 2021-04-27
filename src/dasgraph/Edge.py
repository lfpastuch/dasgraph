class Edge(object):
    
    fromState = ''
    toState = ''
    triggerEvent = ''
    
    def __init__(self, fromState, toState, triggerEvent):
        self.fromState = fromState
        self.toState = toState
        
        