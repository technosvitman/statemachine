
from .State import State

import yaml

class StateMachine():
    
    '''
        @brief build state machine with selected name
        @param name the state machine's name
        @param entry the entry state name
    '''
    def __init__(self, name, entry):
        self.__name = name
        self.__entry = entry
        self.__events = []
        self.__states = []
        
    '''
        @brief get machine name
        @return name
    '''            
    def getName(self) :
        return self.__name
        
    '''
        @brief get entry state
        @return the entry state name
    '''            
    def getEntry(self) :
        return self.__entry
        
    '''
        @brief get event list
        @return the list
    '''            
    def getEvents(self) :
        return self.__events
        
    '''
        @brief get state list
        @return the list
    '''            
    def getStates(self) :
        return self.__states
                
    '''
        @brief get state's name list
        @return the list
    '''            
    def getStateNames(self) :
        names = []
        for state in self.__states:
            names.append(state.getName())
        return names
        
    '''
        @brief append an event to the machine
        @param event the event name to append
    '''            
    def appendEvent(self, event):
        if event not in self.__events:
            self.__events.append(event)
        
    '''
        @brief append a state to the machine
        @param state the state object
    '''            
    def appendState(self, state):
        if state not in self.__states:
            self.__states.append(state)
        
    '''
        @brief build StateMachine from file
        @param file the file name
        @return the machine
    '''
    def fromFile(file):
        yaml_content = yaml.load(file, Loader=yaml.FullLoader)
        
        machine = StateMachine(yaml_content['machine'], yaml_content['entry'])
        
        declared_states = []
        used_states = []
        
        for state_def in yaml_content['states'] :
            name = state_def['name']
            assert name not in declared_states, 'state cannot be declared twice %s'.arg(name)
            declared_states.append(name)
            state = State(name, state_def['enter'], state_def['exit'])
            
            transition_event = []
            transition_state = []
            
            for trans in state_def['transitions'] :
                event = trans['event']
                to = trans['to']
                if to not in used_states :
                    used_states.append(to)
                transition_event.append(event)
                state.appendTransition(to, event)
                machine.appendEvent(event)
                            
            for action in state_def['actions'] :
                assert action not in transition_event, 'action event cannot be set in a transition too : '+event
                state.appendAction(action)
                machine.appendEvent(action)
            machine.appendState(state)
        
        for used_state in used_states :
            assert used_state in declared_states, 'a transition uses a not declared state : '+used_state        
        
        return machine
        
    '''
        @brief string represtation for statemachine
        @return the string
    '''  
    def __str__(self):
        output = "Statemachine(" + self.__name +", Entry: "+self.__entry+"): \n  - Events:\n"
        
        for event in self.__events : 
            output += "    - " +event + "\n"
            
        output += "  - States:\n"
        
        for state in self.__states : 
            output += "    - " +str(state) + "\n"
            
        return output
