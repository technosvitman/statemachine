/**
 * AUTO GENERATED FILE
 */ 
 
#include "statemachine.h"
#include "test_machine.h"



/*****************************************************************
 *              States callbacks declaration                     *
 *****************************************************************/

/********************************
 * State1
 ********************************/
statemachineON_ENTER_CLBK(test_machine_State1);
statemachineDO_JOB_CLBK(test_machine_State1);
statemachineON_EXIT_CLBK(test_machine_State1);

/********************************
 * State2
 ********************************/
statemachineON_ENTER_CLBK(test_machine_State2);
statemachineDO_JOB_CLBK(test_machine_State2);
statemachineON_EXIT_CLBK(test_machine_State2);

/********************************
 * State3
 ********************************/
statemachineON_ENTER_CLBK(test_machine_State3);
statemachineDO_JOB_CLBK(test_machine_State3);
statemachineON_EXIT_CLBK(test_machine_State3);




/*****************************************************************
 *                    States declaration                         *
 *****************************************************************/


/**
 * @brief states declaration for test machine
 */
const statemachine_state_t test_machine_states[test_machine_state_eCOUNT]={
    statemachineS_IDO(test_machine_State1),
    statemachineS_IDO(test_machine_State2),
    statemachineS_IDO(test_machine_State3),
};


/**
 * @brief the machine state
 */
statemachine_t test_machine;



/*****************************************************************
 *                  States Callbacks section                     *
 *****************************************************************/

/**
 * @brief set machine state
 */
static inline void test_machine_set_state( test_machine_state_t state )
{
    statemachine_Set_state( &test_machine, state);
}

/**
 * @brief on enter state global
 */
statemachineON_ENTER_CLBK(test_machine_global)
{
    /* catch global on enter */
    //TODO write your code here
}

/**
 * @brief do job for state global
 */
statemachineDO_JOB_CLBK(test_machine_global)
{
    statemachineNO_DATA(); //Remove this line to use data

    switch(statemachineEVENT_ID())
    {
        default:
        break;
    }
}

/**
 * @brief on exit state global
 */
statemachineON_EXIT_CLBK(test_machine_global)
{
    /* catch global on exit */
    //TODO write your code here
}

/**
 * @brief on enter state State1
 */
statemachineON_ENTER_CLBK(test_machine_State1)
{
    /* catch state1 on enter */
    //TODO write your code here
}

/**
 * @brief do job for state State1
 */
statemachineDO_JOB_CLBK(test_machine_State1)
{
    statemachineNO_DATA(); //Remove this line to use data

    switch(statemachineEVENT_ID())
    {
        case test_machine_event_eEVENT_1_2:
            //TODO write your code here
            test_machine_set_state( test_machine_state_eSTATE2 );
        break;

        case test_machine_event_eEVENT1:
            if( condition2 )
            {
                //TODO write your code here
                test_machine_set_state( test_machine_state_eSTATE2 );
            }
            if( condition3 )
            {
                //TODO write your code here
                test_machine_set_state( test_machine_state_eSTATE3 );
            }
        break;

        default:
        break;
    }
}

/**
 * @brief on exit state State1
 */
statemachineON_EXIT_CLBK(test_machine_State1)
{
    /* catch state1 on exit */
    //TODO write your code here
}

/**
 * @brief on enter state State2
 */
statemachineON_ENTER_CLBK(test_machine_State2)
{
    /* catch state2 on enter */
    //TODO write your code here
}

/**
 * @brief do job for state State2
 */
statemachineDO_JOB_CLBK(test_machine_State2)
{
    statemachineNO_DATA(); //Remove this line to use data

    switch(statemachineEVENT_ID())
    {
        case test_machine_event_eEVENT2:
            if( condition1 )
            {
                //TODO write your code here
                test_machine_set_state( test_machine_state_eSTATE1 );
            }
            if( condition3 )
            {
                //TODO write your code here
                test_machine_set_state( test_machine_state_eSTATE3 );
            }
        break;

        default:
        break;
    }
}

/**
 * @brief on exit state State2
 */
statemachineON_EXIT_CLBK(test_machine_State2)
{
    /* catch state2 on exit */
    //TODO write your code here
}

/**
 * @brief on enter state State3
 */
statemachineON_ENTER_CLBK(test_machine_State3)
{
    /* catch state3 on enter */
    //TODO write your code here
}

/**
 * @brief do job for state State3
 */
statemachineDO_JOB_CLBK(test_machine_State3)
{
    statemachineNO_DATA(); //Remove this line to use data

    switch(statemachineEVENT_ID())
    {
        default:
        break;
    }
}

/**
 * @brief on exit state State3
 */
statemachineON_EXIT_CLBK(test_machine_State3)
{
    /* catch state3 on enter */
    //TODO write your code here
}



/*****************************************************************
 *                  Public functions section                     *
 *****************************************************************/


/**
 * @brief intitialize test machine
 */

void test_machine_Init( void )
{
    statemachine_Init(&test_machine, test_machine_state_eSTATE1, test_machine_states);

    statemachine_Start(&test_machine);

    statemachine_Set_global(&test_machine, statemachineSTATE(test_machine_global, IDO ));
}

/**
 * @brief compute test machine
 * @param event the test event
 * @param data attached event's data or NULL
 */

void test_machine_Compute( test_machine_event_t event, void * data )
{
    statemachine_Compute(&test_machine, event, data);
}

