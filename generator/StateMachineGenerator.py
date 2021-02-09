
from machine import StateMachine


class MachineGenerator():

    '''
        @brief initialize generator
    '''
    def __init__(self):
        self.__machine = None
        self.__indentChar = "  "
    
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
        
    def __buildHeader(self, namebase):
        output = open(namebase+".h", 'w+')
        
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
        


gene = MachineGenerator()
gene.fromFile("machine_example.yml")
gene.compute("machine_example")
