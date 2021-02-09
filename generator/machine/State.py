

class StateTransition():
    '''
        @brief build state transition
        @param to the target state
        @param event the event triggering the transition
    '''
    def __init__(self, to, event):
        self.__to = to
        self.__event = event
    
    '''
        @brief string represtation for statemachine
        @return the string
    '''  
    def __str__(self):
        return "on "+ self.__event + "-> " + self.__to
    

class State():

    '''
        @brief build state with selected name
        @param name the state's name
    '''
    def __init__(self, name):
        self.__name = name
        self.__actions = []
        self.__transitions = []
        
    '''
        @brief append action triggered by event
        @param event the event name to append
    '''            
    def appendAction(self, event):
        self.__actions.append(event)
        
    '''
        @brief append a transition
        @param state the state object
    '''            
    def appendTransition(self, state, event):
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
        

