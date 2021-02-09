
#include "statemachine.h"
#include "machine_example.h"



state_machine_t example_machine;




/*****************************************************************
 *                States Callbacks section                       *
 *****************************************************************/

/**
 * @brief on enter state State1
 */
statemachineON_ENTER_CLBK(example_machine_State1)
{
    //TODO write your code here
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
 * @brief on exit state State3
 */
statemachineON_EXIT_CLBK(example_machine_State3)
{
    //TODO write your code here
}


/*****************************************************************
 *                Public functions section                       *
 *****************************************************************/


/**
 * @brief intitialize example machine
 */

void example_machine_init( void )
{
    statemachine_init(&example_machine, eventStart, example_machine_states);

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
