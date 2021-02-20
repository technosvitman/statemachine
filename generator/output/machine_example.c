
#include "statemachine.h"
#include "machine_example.h"



statemachine_t example_machine;




/*****************************************************************
 *                  States Callbacks section                     *
 *****************************************************************/

/**
 * @brief set machine state
 */
static inline void example_machine_set_state( example_machine_state_t state )
{
    statemachine_Set_state( &example_machine, state);
}

/**
 * @brief on enter state global
 */
statemachineON_ENTER_CLBK(example_machine_global)
{
    /* Do the global on enter job */
    //TODO write your code here
}

/**
 * @brief do job for state global
 */
statemachineDO_JOB_CLBK(example_machine_global)
{
    statemachineNO_DATA(); //Remove this line to use data

    switch(statemachineEVENT_ID())
    {
        case example_machine_event_eEVENT7:
            //TODO write your code here
            example_machine_set_state( example_machine_state_eSTATE4 );
        break;

        case example_machine_event_eEVENT4:
            /* do global event 4 job */
            //TODO write your code here
                break;

        case example_machine_event_eEVENT6:
            /* do global event 6 job */
            //TODO write your code here
                break;

        default:
        break;
    }
}

/**
 * @brief on exit state global
 */
statemachineON_EXIT_CLBK(example_machine_global)
{
    /* Do the global on exit job */
    //TODO write your code here
}

/**
 * @brief on enter state State1
 */
statemachineON_ENTER_CLBK(example_machine_State1)
{
    /* Do the enter job for state 1 */
    //TODO write your code here
}

/**
 * @brief do job for state State1
 */
statemachineDO_JOB_CLBK(example_machine_State1)
{
    statemachineNO_DATA(); //Remove this line to use data

    switch(statemachineEVENT_ID())
    {
        case example_machine_event_eEVENT1:
            //TODO write your code here
            example_machine_set_state( example_machine_state_eSTATE2 );
        break;

        case example_machine_event_eEVENT2:
            //TODO write your code here
            example_machine_set_state( example_machine_state_eSTATE3 );
        break;

        case example_machine_event_eEVENT3:
            //TODO write your code here
            example_machine_set_state( example_machine_state_eSTATE4 );
        break;

        case example_machine_event_eEVENT4:
            /* do event 4 job */
            //TODO write your code here
                break;

        case example_machine_event_eEVENT6:
            /* do event 6 job */
            //TODO write your code here
                break;

        default:
        break;
    }
}

/**
 * @brief do job for state State2
 */
statemachineDO_JOB_CLBK(example_machine_State2)
{
    statemachineNO_DATA(); //Remove this line to use data

    switch(statemachineEVENT_ID())
    {
        case example_machine_event_eEVENT3:
            //TODO write your code here
            example_machine_set_state( example_machine_state_eSTATE3 );
        break;

        case example_machine_event_eEVENT4:
            //TODO write your code here
            example_machine_set_state( example_machine_state_eSTATE4 );
        break;

        case example_machine_event_eEVENT5:
            //TODO write your code here
            example_machine_set_state( example_machine_state_eSTATE1 );
        break;

        case example_machine_event_eEVENT1:
            /* do event 1 job */
            //TODO write your code here
                break;

        default:
        break;
    }
}

/**
 * @brief on exit state State2
 */
statemachineON_EXIT_CLBK(example_machine_State2)
{
    /* Do the exit job for the state 2 */
    //TODO write your code here
}

/**
 * @brief on enter state State3
 */
statemachineON_ENTER_CLBK(example_machine_State3)
{
    /* Do the enter job for state 3 */
    //TODO write your code here
}

/**
 * @brief do job for state State3
 */
statemachineDO_JOB_CLBK(example_machine_State3)
{
    statemachineNO_DATA(); //Remove this line to use data

    switch(statemachineEVENT_ID())
    {
        case example_machine_event_eEVENT6:
            //TODO write your code here
            example_machine_set_state( example_machine_state_eSTATE4 );
        break;

        case example_machine_event_eEVENT2:
            //TODO write your code here
            example_machine_set_state( example_machine_state_eSTATE2 );
        break;

        case example_machine_event_eEVENT1:
            //TODO write your code here
            example_machine_set_state( example_machine_state_eSTATE1 );
        break;

        case example_machine_event_eEVENT4:
            /* do event 4 job */
            //TODO write your code here
                break;

        default:
        break;
    }
}

/**
 * @brief on exit state State3
 */
statemachineON_EXIT_CLBK(example_machine_State3)
{
    /* Do the exit job for state 2 */
    //TODO write your code here
}

/**
 * @brief do job for state State4
 */
statemachineDO_JOB_CLBK(example_machine_State4)
{
    statemachineNO_DATA(); //Remove this line to use data

    switch(statemachineEVENT_ID())
    {
        case example_machine_event_eEVENT6:
            //TODO write your code here
            example_machine_set_state( example_machine_state_eSTATE1 );
        break;

        case example_machine_event_eEVENT5:
            //TODO write your code here
            example_machine_set_state( example_machine_state_eSTATE2 );
        break;

        case example_machine_event_eEVENT2:
            /* do event 2 job */
            //TODO write your code here
                break;

        default:
        break;
    }
}


/*****************************************************************
 *                    States declaration                         *
 *****************************************************************/


/**
 * @brief states declaration for example machine
 */
const statemachine_state_t example_machine_states[example_machine_state_eCOUNT]={
    statemachineSTATE(example_machine_State1, ID ),
    statemachineSTATE(example_machine_State2, DO ),
    statemachineSTATE(example_machine_State3, IDO ),
    statemachineSTATE(example_machine_State4, D ),
};

/*****************************************************************
 *                  Public functions section                     *
 *****************************************************************/


/**
 * @brief intitialize example machine
 */

void example_machine_Init( void )
{
    statemachine_Init(&example_machine, example_machine_state_eSTATE2, example_machine_states);

    statemachine_Start(&example_machine);

    statemachine_Set_global(&example_machine,     statemachineSTATE(example_machine_global, IDO ));
}

/**
 * @brief compute example machine
 * @param event the example event
 * @brief data attached event's data or NULL
 */

void example_machine_Compute( example_machine_event_t event, void * data )
{
    statemachine_Compute(&example_machine, event, data);
}
