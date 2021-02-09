
from machine import StateMachine


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
                
        output += self.__indentChar+prefix + "e" + content[0] + " = 0,\n"
        
        for element in content[1:]:
            output += self.__indentChar+prefix + "e" + element + ",\n"
            
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
        states = self.__machine.getStateNames()
        return self.__buildEnum("State list", prefix, states)
        
    '''
        @brief build and output header file
        @param output file base name
    '''
    def __buildHeader(self, namebase):
        output = open("output/"+namebase+".h", 'w+')
        
        protection = namebase.upper() + "_H"
        
        output.write("\n#ifndef "+protection)
        output.write("\n#define "+protection)
        output.write("\n\n")
        output.write(self.__buildStateEnum())
        output.write("\n")
        output.write(self.__buildEventEnum())
        output.write("\n")
        
        prefix = self.__machine.getName() + "_machine_"
        output.write("\nvoid "+prefix+"init( void );")
        output.write("\nvoid "+prefix+"compute( "+prefix+"event_t event, void * data );")
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
        state_name = prefix+state.getName()
        
        output += "/**\n"
        output += " * @brief do job for state "+state.getName()+"\n"
        output += " */\n"
        output += "statemachineON_ENTER_CLBK("+state_name+")\n"
        output += "{\n"
        output += self.__indentChar+"statemachineNO_DATA(); //Remove this line to use data\n\n"
        output += self.__indentChar+"switch(statemachineEVENT_ID())\n"
        output += self.__indentChar+"{\n"
        
        for trans in state.getTransitions():
            output += self.__indentChar+self.__indentChar+"case "+prefix+"event_e"+trans.getEvent()+":\n"
            output += self.__indentChar+self.__indentChar+self.__indentChar+"//TODO write your code here\n"
            output += self.__indentChar+self.__indentChar
            output += self.__indentChar+prefix+"set_state( "+prefix+"state_e"+trans.getState()+" );+\n"
            output += self.__indentChar+self.__indentChar+"break;\n\n"
        
        for action in state.getActions():
            output += self.__indentChar+self.__indentChar+"case "+prefix+"event_e"+action+":\n"
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
        state_name = prefix+state.getName()
                        
        if state.hasEnter() :
            output += "/**\n"
            output += " * @brief on enter state "+state.getName()+"\n"
            output += " */\n"
            output += "statemachineON_ENTER_CLBK("+state_name+")\n"
            output += "{\n"
            output += self.__indentChar+"//TODO write your code here\n"
            output += "}\n\n"
            
        output += self.__buildStateDoJob(state)
                
        if state.hasExit() :
            output += "/**\n"
            output += " * @brief on exit state "+state.getName()+"\n"
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
        output = open("output/"+namebase+".c", 'w+')
                
        output.write("\n#include \"statemachine.h\"")
        output.write("\n#include \""+namebase+".h\"")
        output.write("\n\n\n")
        
        
        prefix = self.__machine.getName() + "_machine"
        output.write("\nstate_machine_t "+prefix+";\n")
        output.write("\n\n\n")
        output.write("\n/*****************************************************************")
        output.write("\n *                  States Callbacks section                     *")
        output.write("\n *****************************************************************/\n\n")
        
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
        output.write("\nvoid "+prefix+"_init( void )")
        output.write("\n{")
        output.write("\n"+self.__indentChar+"statemachine_init(&"+prefix+", "+"eventStart, "+prefix+"_states);\n")
        output.write("\n"+self.__indentChar+"statemachine_start(&"+prefix+");")
        output.write("\n}\n")
        #write compute function
        output.write("\n/**\n")
        output.write(" * @brief compute "+self.__machine.getName()+" machine\n")
        output.write(" * @param event the "+self.__machine.getName()+" event\n")
        output.write(" * @brief data attached event's data or NULL\n")
        output.write(" */\n")
        output.write("\nvoid "+prefix+"_compute( "+prefix+"_event_t event, void * data );")
        output.write("\n{")
        output.write("\n"+self.__indentChar+"statemachine_compute(&"+prefix+", event, data);")
        output.write("\n}\n")
        


gene = MachineGenerator()
gene.fromFile("machine_example.yml")
gene.compute("machine_example")
