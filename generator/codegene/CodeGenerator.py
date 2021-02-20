
from machine import StateMachine
import os


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
        
    '''
        @biref get write access to output file
    '''
    def getFile(filename):
        return open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/output/"+filename, 'w+')
        
    '''
        @biref get write access to output file
    '''
    def getBinaryFile(filename):
        return open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/output/"+filename, 'wb+')