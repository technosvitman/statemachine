
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
        self.__events = {}
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
        @brief get event name and comment list
        @return the list
    '''            
    def getEvents(self) :
        infos = []
        for event, comment in self.__events.items():
            infos.append({"name":event, "comment":comment})
        return infos
        
    '''
        @brief get state list
        @return the list
    '''            
    def getStates(self) :
        return self.__states
                
    '''
        @brief get state's name and comment list
        @return the list
    '''            
    def getStateInfo(self) :
        infos = []
        for state in self.__states:
            infos.append({"name":state.getName(), "comment":state.getComment()})
        return infos
        
    '''
        @brief append an event to the machine
        @param event the event name to append
        @param comment the event comment
    '''            
    def appendEvent(self, event, comment):
        if event in self.__events:
            if comment: 
                self.__events[event] = comment
        else :
            self.__events[event]=comment
        
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
        
        machine = yaml_content.get('machine')
        assert machine != None, "machine may have a name (field 'machine')"
        
        entry = yaml_content.get('entry')
        assert entry != None, "machine may have an entry state"
        
        machine = StateMachine(machine, entry)
        
        declared_states = []
        used_states = []
        
        states = yaml_content.get('states')
        
        assert states != None, "machine may have state list"
        
        for state_def in states :
            name = state_def.get('name')
            assert name != None, "state may have name"
            assert name not in declared_states, 'state cannot be declared twice %s'.arg(name)
            declared_states.append(name)
            
            comment = state_def.get('comment')
            assert comment != None, "state may have comment"
            
            hasenter = state_def.get('enter')
            assert hasenter != None, "state may have enter information"
            
            hasexit = state_def.get('exit')
            assert hasexit != None, "state may have exit info"
            
            
            state = State(name, comment, hasenter, hasexit)
            
            transition_event = []
            transition_state = []
            
            transitions = state_def.get('transitions')
            assert transitions != None, "state may have transitions list" 
            for trans in transitions :
                event = trans.get('event')
                assert event != None, "transition may have event"
                to = trans.get('to')
                assert to != None, "transition may have destination state ('to')"
                if to not in used_states :
                    used_states.append(to)
                transition_event.append(event)
                state.appendTransition(to, event)
                machine.appendEvent(event, trans.get("comment", ""))
            
            actions = state_def.get('actions')
            assert actions != None, "state may have action list( also if empty) " 
            for action in actions :
                event = action.get('event')
                assert event not in transition_event, 'action event cannot be set in a transition too : '+event
                state.appendAction(event, action.get("action", "") )
                machine.appendEvent(event, action.get("comment", ""))
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
