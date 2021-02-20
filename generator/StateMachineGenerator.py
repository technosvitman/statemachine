
from machine import StateMachine
from codegene import *

import argparse
import os
from plantweb.render import render as render_uml


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
        
        gene = SourceGenerator(self.__machine)
        gene.compute(output)
        gene = HeaderGenerator(self.__machine)
        gene.compute(output)
        self.__buildUML(output)
        
    '''
        @brief build uml file
    ''' 
    def __buildUML(self, namebase):
        
        #build plantuml
        plantuml = "\n@startuml\n"
        
        name = self.__machine.getName().upper()
        
        global_action = self.__machine.getGlobal()
        if global_action : 
            plantuml += "\n[*] -> "+name+"\n"
            plantuml += "state "+name+"{\n"
            if global_action.hasEnter():
                plantuml += name+" : **global entry** : __global_on_enter()__\n"
                plantuml += name+" : > " + global_action.getEnter() + "\\n\n"
            if global_action.hasExit():
                plantuml += name+" : **global exit** : __global_on_exit()__\n"
                plantuml += name+" : > " + global_action.getExit() + "\\n\n"
            
            for action in global_action.getActions():
                
                events = action.getEvents()[0]["name"]
                for event in action.getEvents()[1:] :
                    events += " || "+event["name"]
                job = action.getJob()
                if job :
                    plantuml += name+" : **On** __" + events
                    plantuml += "__ / //"+job+"//"
                    plantuml += "\n"
                to = action.getState()
                if to :
                    plantuml += name+" --> "+to+" : "+ events +"\n"
                plantuml += "\n"
            plantuml += "\n"
        
        
        plantuml += "\n[*] -> "+ self.__machine.getEntry()+"\n"
        
        for state in self.__machine.getStates() :
            plantuml += "\n"
            plantuml += state.getName()+" : //"+state.getComment()+"//\\n\n"
            if state.hasEnter():
                plantuml += state.getName()+" : **Entry** / __"+state.getName()+"_on_enter()__\n"
                plantuml += state.getName()+" : > " + state.getEnter() + "\\n\n"
            if state.hasExit():
                plantuml += state.getName()+" : **Exit** / __"+state.getName()+"_on_exit()__\n"
                plantuml += state.getName()+" : > " + state.getExit() + "\\n\n"
                
            for action in state.getActions():
                
                events = action.getEvents()[0]["name"]
                for event in action.getEvents()[1:] :
                    events += " || "+event["name"]
                job = action.getJob()
                if job :
                    plantuml += state.getName()+" : **On** __" + events
                    plantuml += "__ / //"+job+"//"
                    plantuml += "\n"
                to = action.getState()
                if to :
                    plantuml += state.getName()+" --> "+to+" : "+ events +"\n"
                plantuml += "\n"
            plantuml += "\n"
        
        
        if global_action : 
            plantuml += "}\n"
        
        plantuml += "\n@enduml\n"
        
        output = open(os.path.dirname(os.path.realpath(__file__))+"/output/"+namebase+".plantuml", 'w+')
        output.write(plantuml)
        
        #render uml
        uml = render_uml( plantuml, engine='plantuml', format='png', cacheopts={ 'use_cache': False} )
        
        output = open(os.path.dirname(os.path.realpath(__file__))+"/output/"+namebase+".png", 'wb+')
        for b in uml:
            if isinstance(b, bytes):
                output.write(b)
            elif isinstance(b, str):
                output.write(bytes(b, 'UTF8'))
            
        

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
