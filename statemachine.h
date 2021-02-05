/**
  * @file : statemachine.h
  * @author : Adrien GIRARD
  * @brief : state machine declaration
 */
#ifndef STATE_MACHINE_H
#   define STATE_MACHINE_H

/**
  * state id
  */
typedef int statemachine_state_id_t;

/**
  * event id
  */
typedef int statemachine_event_id_t;

/**
  * @brief on state enter callback
  */
typedef void (*statemachine_enter_clbck_t)(void );

/**
  * @brief do state callback
  * @param event the event id to send to state to perform changes
  * @param data some useful data
  */
typedef void (*statemachine_do_clbck_t)(statemachine_event_id_t, void * data);

/**
  * @brief on state exit callback
  */
typedef void (*statemachine_exit_clbck_t)(void);

/**
  * state callback collection definition
  */
typedef struct
{
    /**
      * state on enter action
      */
    statemachine_enter_clbck_t on_enter;
    /**
      * state do action
      */
    statemachine_do_clbck_t do_job;
    /**
      * state on exit action
      */
    statemachine_exit_clbck_t on_exit;
}statemachine_state_t;

/**
  * state machine structure
  */
typedef struct
{
    /**
      * current machine state
      */
    statemachine_state_id_t current_state;
    /**
      * next state requested
      */
    statemachine_state_id_t new_state;
    /**
      * global on enter action
      */
    statemachine_enter_clbck_t global_on_enter;
    /**
      * global do action
      */
    statemachine_do_clbck_t global_do_job;
    /**
      * global on exit action
      */
    statemachine_exit_clbck_t global_on_exit;
    /**
      * states composing the machine
      */
    statemachine_state_t * states; 
}statemachine_t;

void statemachine_set_state(statemachine_t * machine, statemachine_state_id_t new_state);

statemachine_state_id_t statemachine_get_state(statemachine_t * machine);

void statemachine_compute(statemachine_t * machine, statemachine_event_id_t event, void * data);

#endif
