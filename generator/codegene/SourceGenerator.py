
from .CodeGenerator import CodeGenerator
import os

class SourceGenerator(CodeGenerator):
    
    '''
        @brief compute output state machine files from input machine
    '''
    def compute(self, basename):
        output = open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/output/"+basename+".c", 'w+')
                
        output.write("\n#include \"statemachine.h\"")
        output.write("\n#include \""+basename+".h\"")
        output.write("\n\n\n")
        
        
        output.write("\nstatemachine_t "+self._prefix+";\n")
        output.write("\n\n\n")
        output.write("\n/*****************************************************************")
        output.write("\n *                  States Callbacks section                     *")
        output.write("\n *****************************************************************/\n\n")
        
        output.write("/**\n")
        output.write(" * @brief set machine state\n")
        output.write(" */\n")
        output.write("static inline void " + self._prefix + "_set_state( ")
        output.write(self._prefix + "_state_t state )\n")
        output.write("{\n")
        output.write(CodeGenerator.INDENT_CHAR+"statemachine_Set_state( &" + self._prefix + ", state);\n")
        output.write("}\n\n")
        
        global_action = self._machine.getGlobal()
        
        if global_action :
            output.write(self.__buildStateCallbacks(global_action));
        
        declaration = ""
        
        for state in self._machine.getStates() :
            output.write(self.__buildStateCallbacks(state))
            declaration += self.__buildStateDeclaration(state)+",\n"
            
            
        output.write("\n/*****************************************************************")
        output.write("\n *                    States declaration                         *")
        output.write("\n *****************************************************************/\n\n")
        
        output.write("\n/**\n")
        output.write(" * @brief states declaration for "+self._machine.getName()+" machine\n")
        output.write(" */\n")
        output.write("const statemachine_state_t "+self._prefix+"_states["+self._prefix+"_state_eCOUNT]={\n")
        output.write(declaration)
        output.write("};\n")
        
        output.write("\n/*****************************************************************")
        output.write("\n *                  Public functions section                     *")
        output.write("\n *****************************************************************/\n\n")
        
        #write init function
        output.write("\n/**\n")
        output.write(" * @brief intitialize "+self._machine.getName()+" machine\n")
        output.write(" */\n")
        output.write("\nvoid "+self._prefix+"_Init( void )")
        output.write("\n{")
        output.write("\n"+CodeGenerator.INDENT_CHAR+"statemachine_Init(&"+self._prefix+", ")
        output.write(self._prefix+"_state_e"+self._machine.getEntry().upper()+", "+self._prefix+"_states);\n")
        output.write("\n"+CodeGenerator.INDENT_CHAR+"statemachine_Start(&"+self._prefix+");\n")
        
        if global_action :
            declaration = self.__buildStateDeclaration(global_action)
            output.write("\n"+CodeGenerator.INDENT_CHAR+"statemachine_Set_global(&"+self._prefix+", "+declaration+");\n")
            
        
        output.write("}\n")
        #write compute function
        output.write("\n/**\n")
        output.write(" * @brief compute "+self._machine.getName()+" machine\n")
        output.write(" * @param event the "+self._machine.getName()+" event\n")
        output.write(" * @brief data attached event's data or NULL\n")
        output.write(" */\n")
        output.write("\nvoid "+self._prefix+"_Compute( "+self._prefix+"_event_t event, void * data )")
        output.write("\n{")
        output.write("\n"+CodeGenerator.INDENT_CHAR+"statemachine_Compute(&"+self._prefix+", event, data);")
        output.write("\n}\n")
        

    
    '''
        @brief compute state do job callback
        @param state the state
        @return the string containing the callback
    ''' 
    def __buildStateDoJob(self, state):
        output = ""
        name = state.getName()
        state_name = self._prefix+"_"+name
        
        output += "/**\n"
        output += " * @brief do job for state "+name+"\n"
        output += " */\n"
        output += "statemachineDO_JOB_CLBK("+state_name+")\n"
        output += "{\n"
        output += CodeGenerator.INDENT_CHAR+"statemachineNO_DATA(); //Remove this line to use data\n\n"
        output += CodeGenerator.INDENT_CHAR+"switch(statemachineEVENT_ID())\n"
        output += CodeGenerator.INDENT_CHAR+"{\n"
        
        for action in state.getActions():
            job = action.getJob()
            to = action.getState()
            for event in action.getEvents(): 
                output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+"case "+self._prefix+"_event_e"+event['name'].upper()+":\n"
                if job :
                    output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+"/* "+job+" */\n"
                output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+"//TODO write your code here\n"
                output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR
                if to :
                    output += CodeGenerator.INDENT_CHAR+self._prefix+"_set_state( "+self._prefix+"_state_e"+to.upper()+" );\n"
                output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+"break;\n\n"
        
        output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+"default:\n"
        output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+"break;\n"
        output += CodeGenerator.INDENT_CHAR+"}\n"
        output += "}\n\n"
        
        return output
        
    '''
        @brief compute state callbacks
        @param state the state
        @return the string containing the callbacks
    ''' 
    def __buildStateCallbacks(self, state):
        output = ""
        self._prefix = self._machine.getName() + "_machine_"
        name = state.getName()            
        state_name = self._prefix+name
                        
        if state.hasEnter() :
            output += "/**\n"
            output += " * @brief on enter state "+name+"\n"
            output += " */\n"
            output += "statemachineON_ENTER_CLBK("+state_name+")\n"
            output += "{\n"
            output += CodeGenerator.INDENT_CHAR+"/* "+state.getEntry()+" */\n"
            output += CodeGenerator.INDENT_CHAR+"//TODO write your code here\n"
            output += "}\n\n"
            
        output += self.__buildStateDoJob(state)
                
        if state.hasExit() :
            output += "/**\n"
            output += " * @brief on exit state "+name+"\n"
            output += " */\n"
            output += "statemachineON_EXIT_CLBK("+state_name+")\n"
            output += "{\n"
            output += CodeGenerator.INDENT_CHAR+"/* "+state.getExit()+" */\n"
            output += CodeGenerator.INDENT_CHAR+"//TODO write your code here\n"
            output += "}\n\n"
            
        return output
        
    '''
        @brief compute state declaration
        @param state the state
        @return the string containing the declaration
    ''' 
    def __buildStateDeclaration(self, state):
        output = CodeGenerator.INDENT_CHAR+"statemachineSTATE("
        self._prefix = self._machine.getName() + "_machine_"        
        output += self._prefix+state.getName()+", "
        
                        
        if state.hasEnter() :
            output += "I"
            
        output += "D"
                
        if state.hasExit() :
            output += "O"
        
        output += " )"
            
        return output
        