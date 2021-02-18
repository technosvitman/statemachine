
from machine import StateMachine

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
        
        self.__buildHeader(output)
        self.__buildSource(output)
        self.__buildUML(output)
    
    '''
        @brief compute enum
        @param title the enum title
        @param prefix the prefix to use
        @param content the enum content
        @return the string containing the enum
    '''
    def __buildEnum(self, title, prefix, content):
        output = "/**\n"
        output += " * @brief "+title+"\n"
        output += " */\n"
        output += "typedef enum\n"
        output += "{\n"
                
        output += self.__indentChar+"/**\n"
        output += self.__indentChar+" * @brief "+content[0]["comment"]+"\n"
        output += self.__indentChar+" */\n"
        output += self.__indentChar+prefix + "e" + content[0]["name"].upper() + " = 0,\n"
        
        for element in content[1:]:
            output += self.__indentChar+"/**\n"
            output += self.__indentChar+" * @brief "+element["comment"]+"\n"
            output += self.__indentChar+" */\n"
            output += self.__indentChar+prefix + "e" + element["name"].upper() + ",\n"
                            
        output += self.__indentChar+"/**\n"
        output += self.__indentChar+" * @brief amount of values\n"
        output += self.__indentChar+" */\n"
        output += self.__indentChar+prefix + "eCOUNT\n"        
        output += "}\n"
        output += prefix + "t;\n"
        return output
    
    '''
        @brief compute event enum
        @return the string containing the enum
    '''
    def __buildEventEnum(self):
        prefix = self.__machine.getName() + "_machine_event_"
        events = self.__machine.getEvents()
        return self.__buildEnum("Event list", prefix, events)
        
    '''
        @brief compute state enum
        @return the string containing the enum
    '''
    def __buildStateEnum(self):
        prefix = self.__machine.getName() + "_machine_state_"
        states = self.__machine.getStateInfo()
        return self.__buildEnum("State list", prefix, states)
        
    '''
        @brief build and output header file
        @param output file base name
    '''
    def __buildHeader(self, namebase):
        output = open(os.path.dirname(os.path.realpath(__file__))+"/output/"+namebase+".h", 'w+')
        
        protection = namebase.upper() + "_H"
        
        output.write("\n#ifndef "+protection)
        output.write("\n#define "+protection)
        output.write("\n\n")
        output.write(self.__buildStateEnum())
        output.write("\n")
        output.write(self.__buildEventEnum())
        output.write("\n")
        
        prefix = self.__machine.getName() + "_machine_"
        output.write("\nvoid "+prefix+"Init( void );")
        output.write("\nvoid "+prefix+"Compute( "+prefix+"event_t event, void * data );")
        output.write("\n")
        output.write("\n#endif")
       
    '''
        @brief compute state do job callback
        @param state the state
        @return the string containing the callback
    ''' 
    def __buildStateDoJob(self, state):
        output = ""
        prefix = self.__machine.getName() + "_machine_"
        name = state.getName()
        state_name = prefix+name
        
        output += "/**\n"
        output += " * @brief do job for state "+name+"\n"
        output += " */\n"
        output += "statemachineDO_JOB_CLBK("+state_name+")\n"
        output += "{\n"
        output += self.__indentChar+"statemachineNO_DATA(); //Remove this line to use data\n\n"
        output += self.__indentChar+"switch(statemachineEVENT_ID())\n"
        output += self.__indentChar+"{\n"
        
        for trans in state.getTransitions():
            for event in trans.getEvents(): 
                output += self.__indentChar+self.__indentChar+"case "+prefix+"event_e"+event.upper()+":\n"
                output += self.__indentChar+self.__indentChar+self.__indentChar+"//TODO write your code here\n"
                output += self.__indentChar+self.__indentChar
                output += self.__indentChar+prefix+"set_state( "+prefix+"state_e"+trans.getState().upper()+" );\n"
                output += self.__indentChar+self.__indentChar+"break;\n\n"
        
        for event, action in state.getActions().items():
            output += self.__indentChar+self.__indentChar+"case "+prefix+"event_e"+event.upper()+":\n"
            if action :
                output += self.__indentChar+self.__indentChar+self.__indentChar+"/* "+action+" */\n"
            output += self.__indentChar+self.__indentChar+self.__indentChar+"//TODO write your code here\n"
            output += self.__indentChar+self.__indentChar+"break;\n\n"
        
        
        output += self.__indentChar+self.__indentChar+"default:\n"
        output += self.__indentChar+self.__indentChar+"break;\n"
        output += self.__indentChar+"}\n"
        output += "}\n\n"
        
        return output
        
    '''
        @brief compute state callbacks
        @param state the state
        @return the string containing the callbacks
    ''' 
    def __buildStateCallbacks(self, state):
        output = ""
        prefix = self.__machine.getName() + "_machine_"
        name = state.getName()            
        state_name = prefix+name
                        
        if state.hasEnter() :
            output += "/**\n"
            output += " * @brief on enter state "+name+"\n"
            output += " */\n"
            output += "statemachineON_ENTER_CLBK("+state_name+")\n"
            output += "{\n"
            output += self.__indentChar+"//TODO write your code here\n"
            output += "}\n\n"
            
        output += self.__buildStateDoJob(state)
                
        if state.hasExit() :
            output += "/**\n"
            output += " * @brief on exit state "+name+"\n"
            output += " */\n"
            output += "statemachineON_EXIT_CLBK("+state_name+")\n"
            output += "{\n"
            output += self.__indentChar+"//TODO write your code here\n"
            output += "}\n\n"
            
        return output
        
    '''
        @brief compute state declaration
        @param state the state
        @return the string containing the declaration
    ''' 
    def __buildStateDeclaration(self, state):
        output = self.__indentChar+"statemachineSTATE("
        prefix = self.__machine.getName() + "_machine_"        
        output += prefix+state.getName()+", "
        
                        
        if state.hasEnter() :
            output += "I"
            
        output += "D"
                
        if state.hasExit() :
            output += "O"
        
        output += " )"
            
        return output
       
    '''
        @brief build source file
    ''' 
    def __buildSource(self, namebase):
        output = open(os.path.dirname(os.path.realpath(__file__))+"/output/"+namebase+".c", 'w+')
                
        output.write("\n#include \"statemachine.h\"")
        output.write("\n#include \""+namebase+".h\"")
        output.write("\n\n\n")
        
        
        prefix = self.__machine.getName() + "_machine"
        output.write("\nstatemachine_t "+prefix+";\n")
        output.write("\n\n\n")
        output.write("\n/*****************************************************************")
        output.write("\n *                  States Callbacks section                     *")
        output.write("\n *****************************************************************/\n\n")
        
        output.write("/**\n")
        output.write(" * @brief set machine state\n")
        output.write(" */\n")
        output.write("static inline void " + prefix + "_set_state( ")
        output.write(prefix + "_state_t state )\n")
        output.write("{\n")
        output.write(self.__indentChar+"statemachine_Set_state( &" + prefix + ", state);\n")
        output.write("}\n\n")
        
        global_action = self.__machine.getGlobal()
        
        if global_action :
            output.write(self.__buildStateCallbacks(global_action));
        
        declaration = ""
        
        for state in self.__machine.getStates() :
            output.write(self.__buildStateCallbacks(state))
            declaration += self.__buildStateDeclaration(state)+",\n"
            
            
        output.write("\n/*****************************************************************")
        output.write("\n *                    States declaration                         *")
        output.write("\n *****************************************************************/\n\n")
        
        output.write("\n/**\n")
        output.write(" * @brief states declaration for "+self.__machine.getName()+" machine\n")
        output.write(" */\n")
        output.write("const statemachine_state_t "+prefix+"_states["+prefix+"_state_eCOUNT]={\n")
        output.write(declaration)
        output.write("};\n")
        
        output.write("\n/*****************************************************************")
        output.write("\n *                  Public functions section                     *")
        output.write("\n *****************************************************************/\n\n")
        
        #write init function
        output.write("\n/**\n")
        output.write(" * @brief intitialize "+self.__machine.getName()+" machine\n")
        output.write(" */\n")
        output.write("\nvoid "+prefix+"_Init( void )")
        output.write("\n{")
        output.write("\n"+self.__indentChar+"statemachine_Init(&"+prefix+", ")
        output.write(prefix+"_state_e"+self.__machine.getEntry().upper()+", "+prefix+"_states);\n")
        output.write("\n"+self.__indentChar+"statemachine_Start(&"+prefix+");\n")
        
        if global_action :
            declaration = self.__buildStateDeclaration(global_action)
            output.write("\n"+self.__indentChar+"statemachine_Set_global(&"+prefix+", "+declaration+");\n")
            
        
        output.write("}\n")
        #write compute function
        output.write("\n/**\n")
        output.write(" * @brief compute "+self.__machine.getName()+" machine\n")
        output.write(" * @param event the "+self.__machine.getName()+" event\n")
        output.write(" * @brief data attached event's data or NULL\n")
        output.write(" */\n")
        output.write("\nvoid "+prefix+"_Compute( "+prefix+"_event_t event, void * data )")
        output.write("\n{")
        output.write("\n"+self.__indentChar+"statemachine_Compute(&"+prefix+", event, data);")
        output.write("\n}\n")
        
    '''
        @brief build uml file
    ''' 
    def __buildUML(self, namebase):
        
        #build plantuml
        plantuml = "\n@startuml\n"
        
        name = self.__machine.getName()
        
        global_action = self.__machine.getGlobal()
        if global_action : 
            plantuml += "\n[*] -> "+name+"\n"
            plantuml += "state "+name+"{\n"
            if global_action.hasEnter():
                plantuml += name+" : __global on enter__ : **global_on_enter()**\n"
                plantuml += name+" : > " + global_action.getEnter() + "\\n\n"
            if global_action.hasExit():
                plantuml += name+" : __global on exit__ : **global_on_exit()**\n"
                plantuml += name+" : > " + global_action.getExit() + "\\n\n"
            for trans in global_action.getTransitions():
                events = trans.getEvents()[0]
                for event in trans.getEvents()[1:] :
                    events += " || "+event
                plantuml += name+" --> "+trans.getState()+" : "+ events +"\n"            
            if len(global_action.getActions()):
                for event, action in global_action.getActions().items():
                    plantuml += name+" --> "+name+" : " + event
                    if action : 
                        plantuml += " : //"+action+"//"
                    plantuml += "\n"
                plantuml += "\n"
            plantuml += "\n"
        
        
        plantuml += "\n[*] -> "+ self.__machine.getEntry()+"\n"
        
        for state in self.__machine.getStates() :
            plantuml += "\n"
            plantuml += state.getName()+" : //"+state.getComment()+"//\\n\n"
            if state.hasEnter():
                plantuml += state.getName()+" : __on enter__ : **"+state.getName()+"_on_enter()**\n"
                plantuml += state.getName()+" : > " + state.getEnter() + "\\n\n"
            if state.hasExit():
                plantuml += state.getName()+" : __on exit__ : **"+state.getName()+"_on_exit()**\n"
                plantuml += state.getName()+" : > " + state.getExit() + "\\n\n"
            for trans in state.getTransitions():
                events = trans.getEvents()[0]
                for event in trans.getEvents()[1:] :
                    events += " || "+event
                plantuml += state.getName()+" --> "+trans.getState()+" : "+ events +"\n"
            
            if len(state.getActions()):
                for event, action in state.getActions().items():
                    plantuml += state.getName()+" --> "+state.getName()+" : " + event
                    if action : 
                        plantuml += " : //"+action+"//"
                    plantuml += "\n"
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
