
from machine import StateMachine


class CodeGenerator():

    INDENT_CHAR = "    " 

    '''
        @brief initialize generator
        @param machine the state machine to compute
    '''
    def __init__(self, machine):
        self._machine = machine   
        self._prefix = self._machine.getName() + "_machine"
    
    '''
        @brief compute output state machine files from input machine
    '''
    def compute(self, basename):
        pass