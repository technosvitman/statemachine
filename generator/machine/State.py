

class StateTransition():
    '''
        @brief build state transition
        @param to the target state
        @param event the event triggering the transition
    '''
    def __init__(self, to, event):
        self.__to = to
        self.__event = [event]
        
    '''
        @brief get transition state target
        @return state name
    '''            
    def getState(self) :
        return self.__to
        
    '''
        @brief get transition event
        @return event
    '''            
    def getEvents(self) :
        return self.__event
        
    '''
        @brief append transition event
        @param event event
    '''            
    def append(self, event) :
        self.__event.append(event)
    
    '''
        @brief string represtation for statemachine
        @return the string
    '''  
    def __str__(self):
        output = self.__event[0]
        for event in self.__event[1:]:
            output += " | " + event
        return "on ("+ output + ")-> " + self.__to
    

class State():

    '''
        @brief build state with selected name
        @param name the state's name
        @param comment some information on state
        @param enterBrief if not empty the state has action on enter
        @param exitBrief if not empty the state has action on exit
    '''
    def __init__(self, name, comment, enterBrief, exitBrief):
        self.__name = name
        self.__comment = comment
        self.__enter = enterBrief
        self.__exit = exitBrief
        self.__actions = {}
        self.__transitions = []
        
    '''
        @brief get state name
        @return name
    '''            
    def getName(self) :
        return self.__name
        
    '''
        @brief get state comment
        @return comment
    '''            
    def getComment(self) :
        return self.__comment
        
    '''
        @brief get state actions
        @return action list
    '''            
    def getActions(self) :
        return self.__actions
        
    '''
        @brief get state transitions
        @return transition list
    '''            
    def getTransitions(self) :
        return self.__transitions
        
    '''
        @brief get if has enter callback
        @return true if has callback
    '''
    def hasEnter(self) :
        return self.__enter!=""
        
    '''
        @brief get if has exit callback
        @return true if has callbac
    '''            
    def hasExit(self) :
        return self.__exit!=""
        
    '''
        @brief get enter action brief
        @return enter brief
    '''
    def getEnter(self) :
        return self.__enter
        
    '''
        @brief get exit action brief
        @return exit brief
    '''            
    def getExit(self) :
        return self.__exit
        
    '''
        @brief append action triggered by event
        @param event the event name to append
        @param action the action brief
    '''            
    def appendAction(self, event, action):
        self.__actions[event]=action
        
    '''
        @brief append a transition
        @param state the state object
    '''            
    def appendTransition(self, state, event):
        for trans in self.__transitions :
            if trans.getState() == state :
                trans.append(event)
                return
        self.__transitions.append( StateTransition(state, event) )

    '''
        @brief string represtation for statemachine
        @return the string
    '''  
    def __str__(self):
        output = "State(" + self.__name +"): Transitions( "
        
        for trans in self.__transitions :
            output += str(trans) + ', '
        
        output += "), Actions( "
        
        for action in self.__actions :
            output += action + ', '
            
        return output + ")"
        

