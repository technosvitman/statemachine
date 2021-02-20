
from machine import StateMachine
from codegene import *

import argparse
import os


class MachineGenerator():

    '''
        @brief initialize generator
    '''
    def __init__(self):
        self.__machine = None
        self.__indentChar = "    "
    
    '''
        build input machine from file
    '''
    def fromFile(self, file):
        yaml_file = open(file, 'r')
        self.__machine = StateMachine.fromFile(yaml_file)
    
    '''
        @brief compute output state machine files from input machine
    '''
    def compute(self, output):
        assert len(self.__machine.getEvents()) != 0, 'Event list cannot be empty'
        print( self.__machine )
        
        gene = Source(self.__machine)
        gene.compute(output)
        gene = Header(self.__machine)
        gene.compute(output)
        gene = Plantuml(self.__machine)
        gene.compute(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script so useful.')
    parser.add_argument("-i", type=str, default=os.path.dirname(os.path.realpath(__file__))+"/machine_example.yml")
    parser.add_argument("-o", type=str, default="")
    
    args = parser.parse_args()
    
    gene = MachineGenerator()
    gene.fromFile(args.i)
    
    output = args.o
    if output == "":
        head, tail = os.path.split(args.i)
        output = os.path.splitext(tail)[0]
    
    gene.compute(output)
