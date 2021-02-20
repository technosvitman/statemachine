
from .CodeGenerator import CodeGenerator

class Header(CodeGenerator):
    
    '''
        @brief compute output state machine files from input machine
    '''
    def compute(self, basename):
        output = CodeGenerator.getFile(basename+".h")
        
        protection = "__"+basename.upper() + "_H__"
        
        output.write("\n#ifndef "+protection)
        output.write("\n#define "+protection)
        output.write("\n\n")
        output.write(self.__buildStateEnum())
        output.write("\n")
        output.write(self.__buildEventEnum())
        output.write("\n")
        
        output.write("\nvoid "+self._prefix+"_Init( void );")
        output.write("\nvoid "+self._prefix+"_Compute( "+self._prefix+"_event_t event, void * data );")
        output.write("\n")
        output.write("\n#endif // "+protection)        
    
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
                
        output += CodeGenerator.INDENT_CHAR+"/**\n"
        output += CodeGenerator.INDENT_CHAR+" * @brief "+content[0]["comment"]+"\n"
        output += CodeGenerator.INDENT_CHAR+" */\n"
        output += CodeGenerator.INDENT_CHAR+prefix + "e" + content[0]["name"].upper() + " = 0,\n"
        
        for element in content[1:]:
            output += CodeGenerator.INDENT_CHAR+"/**\n"
            output += CodeGenerator.INDENT_CHAR+" * @brief "+element["comment"]+"\n"
            output += CodeGenerator.INDENT_CHAR+" */\n"
            output += CodeGenerator.INDENT_CHAR+prefix + "e" + element["name"].upper() + ",\n"
                            
        output += CodeGenerator.INDENT_CHAR+"/**\n"
        output += CodeGenerator.INDENT_CHAR+" * @brief amount of values\n"
        output += CodeGenerator.INDENT_CHAR+" */\n"
        output += CodeGenerator.INDENT_CHAR+prefix + "eCOUNT\n"        
        output += "}\n"
        output += prefix + "t;\n"
        return output
    
    '''
        @brief compute event enum
        @return the string containing the enum
    '''
    def __buildEventEnum(self):
        prefix = self._prefix + "_event_"
        events = self._machine.getEvents()
        return self.__buildEnum("Event list", prefix, events)
        
    '''
        @brief compute state enum
        @return the string containing the enum
    '''
    def __buildStateEnum(self):
        prefix = self._prefix + "_state_"
        states = self._machine.getStateInfo()
        return self.__buildEnum("State list", prefix, states)
        
    
        