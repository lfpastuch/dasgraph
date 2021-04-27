class Event(object):
    
    eventName = ''

    def __init__(self, eventName, eventType, eventObservability):
        
        self.eventName = eventName
        self.eventType = eventType
        self.observable = eventObservability
        
        