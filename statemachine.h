/**
  * @file : statemachine.h
  * @author : Adrien GIRARD
  * @brief : state machine declaration
 */
#ifndef STATE_MACHINE_H
#   define STATE_MACHINE_H


/**
 * @brief build state on enter callback name
 * @param state_name the state name
 */
#define statemachineON_ENTER(state)         sm_##state##_on_enter

/**
 * build state do job callback name
 * @param state_name the state name
 */
#define statemachineDO_JOB(state)           sm_##state##_do_job

/**
 * @brief build state on enter callback name
 * @param state_name the state name
 */
#define statemachineON_EXIT(state)          sm_##state##_on_exit
 
 
/**
 * @brief build state on enter callback function
 * @param state_name the state name
 */
#define statemachineON_ENTER_CLBK(state)     static void sm_##state##_on_enter(void)

/**
 * build state do job callback function
 * @param state_name the state name
 */
#define statemachineDO_JOB_CLBK(state)       static void sm_##state##_do_job(statemachine_event_id_t event, void * data)

/**
 * @brief build state on enter callback function
 * @param state_name the state name
 */
#define statemachineON_EXIT_CLBK(state)      static void sm_##state##_on_exit(void)

/**
 * @brief get the event id
 * @note to be used in do_job callback 
 */
#define statemachineEVENT_ID()                    (event)  

/**
 * @brief get the event data pointer
 * @note to be used in do_job callback 
 */
#define statemachineEVENT_DATA()                  (data)

/**
 * @brief indicate that event data are not used
 * @note to be used in do_job callback
 */
#define statemachineNO_DATA()                  ((void)data)

/**
 * @brief state declaration helper with Enter/Do/Exit callbacks
 */
#define statemachineS_IDO(state)  {  \
											statemachineON_ENTER(state), \
											statemachineDO_JOB(state), \
											statemachineON_EXIT(state) \
									}

/**
 * @brief state declaration helper with Enter/Do callbacks
 */
#define statemachineS_ID(state)  {  \
											statemachineON_ENTER(state), \
											statemachineDO_JOB(state), \
											NULL \
									}

/**
 * @brief state declaration helper with Do callback only
 */
#define statemachineS_D(state)  {  \
											NULL, \
											statemachineDO_JOB(state), \
											NULL \
									}

/**
 * @brief state declaration helper with Do/Exit callbacks
 */
#define statemachineS_DO(state)  {  \
											NULL, \
											statemachineDO_JOB(state), \
											statemachineON_EXIT(state) \
									}

/**
 * @brief state declaration helper with Enter/Exit callbacks
 */
#define statemachineS_IO(state)  {  \
											statemachineON_ENTER(state), \
											NULL, \
											statemachineON_EXIT(state) \
									}
/**
 * @brief state declaration helper with Enter callback only
 */
#define statemachineS_I(state)  {  \
											statemachineON_ENTER(state), \
											NULL, \
											NULL \
									}
/**
 * @brief state declaration helper with Exit callback only
 */
#define statemachineS_O(state)  {  \
											NULL, \
											NULL, \
											statemachineON_EXIT(state) \
									}
/**
 * @brief state declaration helper with no callbacks
 */
#define statemachineS_(state)  {  \
											NULL, \
											NULL, \
											NULL \
									}

/**
 * @brief state declaration helper
 * @param state the state name
 * @param callbacks needed callbacks
 * - I : use on_enter callback
 * - D : use do_job callback
 * - O : use on_exit callback
 * I, D, O should be set in this order
 */
#define statemachineSTATE(state, callbacks)  ((statemachine_state_t)statemachineS_##callbacks(state))
 
 
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
typedef void (*statemachine_do_clbck_t)(statemachine_event_id_t id, void * data);

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
    const statemachine_state_t * states; 
}statemachine_t;

void statemachine_Init(statemachine_t * machine, statemachine_state_id_t first_state, const statemachine_state_t * states);

void statemachine_Set_global(statemachine_t * machine, statemachine_state_t global_action);

void statemachine_Start(statemachine_t * machine);


void statemachine_Set_state(statemachine_t * machine, statemachine_state_id_t new_state);

statemachine_state_id_t statemachine_Get_state(statemachine_t * machine);

void statemachine_Compute(statemachine_t * machine, statemachine_event_id_t event, void * data);

#endif
