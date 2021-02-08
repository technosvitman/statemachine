/**
  * @file : statemachine.c
  * @author : Adrien GIRARD
  * @brief :state machine implementation
 */
#include <stdio.h>
#include <stdlib.h>

#include "statemachine.h"

/**
  * @brief initialize state machine
  * @param machine state machine to change
  * @param first_state the entry point state
  * @param states states definitions
  */
void statemachine_init(statemachine_t * machine, statemachine_state_id_t first_state, const statemachine_state_t * states)
{
	machine->new_state = first_state;
	machine->current_state = first_state;
	machine->current_state = first_state;
	machine->global_on_enter = NULL;
	machine->global_do_job = NULL;
	machine->global_on_exit = NULL;
	machine->states = states;
}

/**
  * @brief set global states actions
  * @param machine state machine to change
  * @param on_enter global on enter action
  * @param do_job global do job action
  * @param on_exit global on exit action
  */
void statemachine_set_golbal(statemachine_t * machine, statemachine_enter_clbck_t on_enter, statemachine_do_clbck_t do_job,
							statemachine_exit_clbck_t on_exit)
{
	machine->global_on_enter = on_enter;
	machine->global_do_job = do_job;
	machine->global_on_exit = on_exit;
}

/**
 * @brief start state machine
 * @note execute global_on_enter and current_state on_enter
 * @warning should be called before any "compute" call
 */
void statemachine_start(statemachine_t * machine)
{    
	if(machine->global_on_enter != NULL)
	{
		machine->global_on_enter();
	}

	const statemachine_state_t * state = &(machine->states[machine->current_state]);

	if(state->on_enter != NULL)
	{
		state->on_enter();
	}	
}

/**
  * @brief set next state
  * @param machine state machine to change
  * @param new_state the new state id
  */
void statemachine_set_state(statemachine_t * machine, statemachine_state_id_t new_state)
{
    machine->new_state = new_state;
}

/**
  * @brief get current state
  * @param machine state machine to show
  * @return current statemachine_state_id_t
  */
statemachine_state_id_t statemachine_get_state(statemachine_t * machine)
{
    return machine->current_state;
}

/**
  * @brief compute state machine
  * perform state change if needed and compute expected callbacks
  * global do
  * specific do
  * global on exit
  * specific on exit
  * global on enter
  * specific on enter
  * @param machine state machine to compute
  * @param event the event id to send to state to perform changes
  * @param data some useful data
  */
void statemachine_compute(statemachine_t * machine, statemachine_event_id_t event, void * data)
{
    const statemachine_state_t * state = &(machine->states[machine->current_state]);

    if(machine->global_do_job!=NULL)
    {
        machine->global_do_job(event, data);
    }
    
    if( state->do_job != NULL ) 
    {
        state->do_job(event, data);
    }

    /* state change so compute */
    if( machine->new_state != machine->current_state ) 
    {
        if(machine->global_on_exit != NULL)
        {
            machine->global_on_exit();
        }
        
        if( state->on_exit != NULL )
        {
            state->on_exit();
        }
    
        if(machine->global_on_enter != NULL)
        {
            machine->global_on_enter();
        }

        state = &(machine->states[machine->new_state]);

        if(state->on_enter != NULL)
        {
            state->on_enter();
        }

        machine->current_state = machine->new_state;
    }
}


