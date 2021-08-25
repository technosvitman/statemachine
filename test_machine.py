
import sys
import io
import time
import argparse
import re
from pyctest import *

def getState(test):
    return test.c_test_machine.c_state

'''
    @see PycTestCase
'''
class TestStartAndTransition(PycTestCase):
    def __init__(self):    
        super(PycTestCase, self).__init__()
        
    def runTest(self):
        self.c_test_machine_Init()
        
        self.assertEqual(getState(self), \
                self.c_test_machine_state_eSTATE1)
        
        self.c_test_machine_Compute( \
                self.c_test_machine_event_eEVENT_1_2, \
                self.NULL())
        
        self.assertEqual(getState(self), \
                self.c_test_machine_state_eSTATE2)

'''
    @see PycTestCase
'''
class TestConditionalTransition(PycTestCase):
    def __init__(self):    
        super(PycTestCase, self).__init__()
        
    def runTest(self):
        self.c_test_machine_Init()
        
        self.c_test_machine_Compute( \
                self.c_test_machine_event_eEVENT_1_2, \
                self.NULL())
                
        self.c_cond1[0] = 0
        self.c_cond2[0] = 0
        self.c_cond3[0] = 0
        
        self.c_test_machine_Compute( \
                self.c_test_machine_event_eEVENT2, \
                self.NULL())
        
        self.assertEqual(getState(self), \
                self.c_test_machine_state_eSTATE2)
                
        self.c_cond1[0] = 1
        
        self.c_test_machine_Compute( \
                self.c_test_machine_event_eEVENT2, \
                self.NULL())
        
        self.assertEqual(getState(self), \
                self.c_test_machine_state_eSTATE1)
                
        self.c_cond1[0] = 0
        self.c_cond2[0] = 1
        
        self.c_test_machine_Compute( \
                self.c_test_machine_event_eEVENT1, \
                self.NULL())
        
        self.assertEqual(getState(self), \
                self.c_test_machine_state_eSTATE2)
                
        self.c_cond2[0] = 0
        self.c_cond3[0] = 1
        
        self.c_test_machine_Compute( \
                self.c_test_machine_event_eEVENT2, \
                self.NULL())
        
        self.assertEqual(getState(self), \
                self.c_test_machine_state_eSTATE3)

'''
    @see PycTestCase
'''
class TestCurrentStateMemoryFailure(PycTestCase):
    def __init__(self):    
        super(PycTestCase, self).__init__()
        
    def runTest(self):
        self.c_test_machine_Init()
        
        self.c_test_machine.c_state = self.c_test_machine_state_eSTATE2
        
        self.c_corruption[0] = 0
        self.assertEqual(self.c_corruption[0], 0)
        
        self.c_test_machine_Compute( \
                self.c_test_machine_event_eEVENT_1_2, \
                self.NULL())
        self.assertEqual(self.c_corruption[0], 2)
        
'''
    @see PycTestCase
'''
class TestNewStateMemoryFailure(PycTestCase):
    def __init__(self):    
        super(PycTestCase, self).__init__()
        
    def runTest(self):
        self.c_test_machine_Init()
        
        self.c_test_machine.n_n_state = self.c_test_machine_state_eSTATE3
        
        self.c_corruption[0] = 0
        self.assertEqual(self.c_corruption[0], 0)
        
        self.c_test_machine_Compute( \
                self.c_test_machine_event_eEVENT2, \
                self.NULL())
                
        self.assertEqual(getState(self), \
                self.c_test_machine_state_eSTATE1)
                
        self.assertEqual(self.c_corruption[0], 1)
                
 
class TestMachine:
    MODULE_FILE="statemachine"
    MACHINE_FILE="test_machine"

    def __init__(self):
        self.__loader = PycTester()
    
    '''
        @brief build library from c file
    '''
    def build(self):    
        self.__loader.load_source("""
            
            int corrupt = 0;
            #define statemachineASSERT_CORRUPT(cond)  if(!(cond)){corrupt++;}
            int * corruption = &corrupt;
            """); 
        
    
        self.__loader.load_module(TestMachine.MODULE_FILE)
                
        self.__loader.load_source("""
            
            int condition1 = 0;
            int condition2 = 0;
            int condition3 = 0;
            
            int * cond1 = &condition1;
            int * cond2 = &condition2;
            int * cond3 = &condition3;
            """); 
            
        self.__loader.load_module(TestMachine.MACHINE_FILE)   
        
        self.__loader.load_header("""            
            extern int * cond1;
            extern int * cond2;
            extern int * cond3;
            extern int * corruption;
            extern statemachine_t test_machine;
        """); 
                
        
        self.__loader.build("_testmachine")
        
    '''
        @brief unitary test for C library
    '''
    def unitest(self):
        print("================Unitary Test==============")  

        print("Generate test cases")
        self.__loader.appendTest(TestStartAndTransition())  
        self.__loader.appendTest(TestConditionalTransition())  
        self.__loader.appendTest(TestCurrentStateMemoryFailure())  
        self.__loader.appendTest(TestNewStateMemoryFailure())     
        self.__loader.run()       
        
        
parser = argparse.ArgumentParser(description='Statemachine tester')
parser.add_argument("-u", default=False, action="store_true")
parser.add_argument("-b", default=False, action="store_true")

args = parser.parse_args()

tester = TestMachine()

if args.u or args.b:
    tester.build()

if args.u:
    tester.unitest()