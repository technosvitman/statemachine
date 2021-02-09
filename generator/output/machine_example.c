
#include "statemachine.h"
#include "machine_example.h"



state_machine_t example_machine;




/*****************************************************************
 *                  States Callbacks section                     *
 *****************************************************************/

/**
 * @brief on enter state State1
 */
statemachineON_ENTER_CLBK(example_machine_State1)
{
    //TODO write your code here
}

/**
 * @brief do job for state State1
 */
statemachineON_ENTER_CLBK(example_machine_State1)
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
            //TODO write your code here
        break;

        case example_machine_event_eEVENT5:
            //TODO write your code here
        break;

        case example_machine_event_eEVENT6:
            //TODO write your code here
        break;

        default:
        break;
    }
}

/**
 * @brief do job for state State2
 */
statemachineON_ENTER_CLBK(example_machine_State2)
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
    //TODO write your code here
}

/**
 * @brief on enter state State3
 */
statemachineON_ENTER_CLBK(example_machine_State3)
{
    //TODO write your code here
}

/**
 * @brief do job for state State3
 */
statemachineON_ENTER_CLBK(example_machine_State3)
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
    //TODO write your code here
}

/**
 * @brief do job for state State4
 */
statemachineON_ENTER_CLBK(example_machine_State4)
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

void example_machine_init( void )
{
    statemachine_init(&example_machine, example_machine_state_eSTATE2, example_machine_states);

    statemachine_start(&example_machine);
}

/**
 * @brief compute example machine
 * @param event the example event
 * @brief data attached event's data or NULL
 */

void example_machine_compute( example_machine_event_t event, void * data );
{
    statemachine_compute(&example_machine, event, data);
}
