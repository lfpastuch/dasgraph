class State(object):
    
    stateName = ''

    def __init__(self, stateName, stateMarking, initState):
        
        self.stateName = stateName
        self.stateMarking = stateMarking
        self.initState = initState