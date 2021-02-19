
from .State import State
from .State import StateAction

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
        self.__global = None
        
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
        @brief set global state action
        @param state the state object that represent global action
    '''            
    def setGlobal(self, state):
        self.__global = state
        
    '''
        @brief return global state action
    '''            
    def getGlobal(self):
        return self.__global
        
    '''
        @brief append a state to the machine
        @param state the state object
    '''            
    def appendState(self, state):
        if state not in self.__states:
            self.__states.append(state)
            
    '''
        @brief extract state from yaml
        @param state_def yaml definition
        @param name state name
    '''
    def extractState(self, state_def, name):
    
        if name == "" :
            name = "global"
            comment = "Global action"
        else:
            comment = state_def.get('comment', '')
            assert comment != None, "state may have comment"
        
        hasenter = state_def.get('enter')
        assert hasenter != None, "state may have enter information"
        
        hasexit = state_def.get('exit')
        assert hasexit != None, "state may have exit info"
        
        
        state = State(name, comment, hasenter, hasexit)
        
        action_event = []
        action_state = []
        used_states = []
        
        actions = state_def.get('actions')
        assert actions != None, "state may have action list( also if empty) " 
        
        for action in actions :
            event = action.get('event')
            assert event != None, "action may have event"
                        
            to = action.get('to', None)
            job = action.get('job', None)
            
            assert not (to == None and job == None), "an action may at least have an action or a target state"
            
            state.appendAction(StateAction(event, to, job))
            
            if isinstance(event, str):
                self.appendEvent(event, action.get("comment", ""))
            else :
                for e in event :
                    self.appendEvent(e, action.get("comment", ""))
                    
        if name == "global" :            
            self.setGlobal(state)
        else :            
            self.appendState(state)
        
        return used_states
        
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
                
        global_action = yaml_content.get('global', None)
        if global_action :
            used_states += machine.extractState(global_action, "")
        
        states = yaml_content.get('states')
        
        assert states != None, "machine may have state list"
        
        for state_def in states :
            name = state_def.get('name')
            assert name != None, "state may have name"
            assert name not in declared_states, 'state cannot be declared twice %s'.arg(name)
            declared_states.append(name)
            used_states += machine.extractState(state_def, name)
        
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
