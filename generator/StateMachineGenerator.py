
from machine import StateMachine


class MachineGenerator():

    '''
        @brief initialize generator
    '''
    def __init__(self):
        self.__machine = None
    
    '''
        build input machine from file
    '''
    def fromFile(self, file):
        self.__machine = StateMachine.fromFile(file)
    
    '''
        @brief compute output state machine files from input machine
    '''
    def compute(self):
        print( self.__machine )



gene = MachineGenerator()
gene.fromFile("TBD")
gene.compute()
