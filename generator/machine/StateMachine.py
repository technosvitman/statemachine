
from .State import State

class StateMachine():
    
    '''
        @brief build state machine with selected name
        @param name the state machine's name
    '''
    def __init__(self, name):
        self.__name = name
        self.__events = []
        self.__states = []
        
    '''
        @brief append an event to the machine
        @param event the event name to append
    '''            
    def appendEvent(self, event):
        self.__events.append(event)
        
    '''
        @brief append a state to the machine
        @param state the state object
    '''            
    def appendState(self, state):
        self.__states.append(state)
    
        
    '''
        @brief build StateMachine from file
        @param file the file name
        @return the machine
    '''
    def fromFile(file):
        machine = StateMachine("TBD")
        machine.appendEvent("Event1")
        machine.appendEvent("Event2")
        machine.appendEvent("Event3")
        
        state = State("State1")
        state.appendTransition("State2", "Event1")
        state.appendTransition("State3", "Event2")
        state.appendAction("Event3")
        machine.appendState(state)
        
        
        state = State("State2")
        state.appendTransition("State1", "Event1")
        state.appendAction("Event2")
        state.appendAction("Event3")
        machine.appendState(state)
        
        return machine
        
    '''
        @brief string represtation for statemachine
        @return the string
    '''  
    def __str__(self):
        output = "Statemachine(" + self.__name +"): \n  - Events:\n"
        
        for event in self.__events : 
            output += "    - " +event + "\n"
            
        output += "  - States:\n"
        
        for state in self.__states : 
            output += "    - " +str(state) + "\n"
            
        return output
