/**
  * @file : statemachine.c
  * @author : Adrien GIRARD
  * @brief :state machine implementation
 */
#include <stdio.h>
#include <stdlib.h>

#include "statemachine.h"

/**
 * @brief check state id corruption
 */
#define statemachineCHECK_STATE(state, compl)   statemachineASSERT_CORRUPT( ( state ^ compl ) == 0xFFFFFFFF )

/**
  * @brief initialize state machine
  * @param machine state machine to change
  * @param first_state the entry point state
  * @param states states definitions
  */
void statemachine_Init(statemachine_t * machine, statemachine_state_id_t first_state, const statemachine_state_t * states)
{
    statemachineASSERT(machine);
    statemachineASSERT(states);
    
    machine->current_state = first_state;
    machine->new_state = first_state;
    machine->compl_current_state = ~first_state;
    machine->compl_new_state = ~first_state;
    
    machine->global_on_enter = NULL;
    machine->global_do_job = NULL;
    machine->global_on_exit = NULL;
    machine->states = states;
}

/**
  * @brief set global states actions
  * @param machine state machine to change
  * @param global_action a state that represent global action
  */
void statemachine_Set_global(statemachine_t * machine, statemachine_state_t global_action)
{
    statemachineASSERT(machine);
    machine->global_on_enter = global_action.on_enter;
    machine->global_do_job = global_action.do_job;
    machine->global_on_exit = global_action.on_exit;
}

/**
 * @brief start state machine
 * @note execute global_on_enter and current_state on_enter
 * @warning should be called before any "compute" call
 */
void statemachine_Start(statemachine_t * machine)
{    
    statemachineASSERT(machine);
    if(machine->global_on_enter != NULL)
    {
        machine->global_on_enter();
    }
    
    statemachineCHECK_STATE( machine->current_state, machine->compl_current_state );

    const statemachine_state_t * state = &(machine->states[machine->current_state]);

    if(state->on_enter != NULL)
    {
        state->on_enter();
    }    
}

/**
  * @brief set next state
  * @param machine state machine to change
  * @param current_state the new state id
  */
void statemachine_Set_state(statemachine_t * machine, statemachine_state_id_t current_state)
{
    statemachineASSERT(machine);
    machine->new_state = current_state;
    machine->compl_new_state = ~current_state;
}

/**
  * @brief get current state
  * @param machine state machine to show
  * @return current statemachine_state_id_t
  */
statemachine_state_id_t statemachine_Get_state(statemachine_t * machine)
{    
    statemachineASSERT(machine);
    statemachineCHECK_STATE( machine->current_state, machine->compl_current_state );
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
void statemachine_Compute(statemachine_t * machine, statemachine_event_id_t event, void * data)
{   
    statemachineASSERT(machine);
    
    statemachineCHECK_STATE( machine->current_state, machine->compl_current_state );
    
    const statemachine_state_t * state = &(machine->states[machine->current_state]);

    if(machine->global_do_job!=NULL)
    {
        machine->global_do_job(event, data);
    }
    
    if( state->do_job != NULL ) 
    {
        state->do_job(event, data);
    }
    
    statemachineCHECK_STATE( machine->current_state, machine->compl_current_state );
    
    statemachineCHECK_STATE( machine->new_state, machine->compl_new_state );

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
        machine->compl_current_state = machine->compl_new_state;
    }
}


