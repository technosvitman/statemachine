# statemachine

## Introduction

In many microcontroler program, without the help of tiny OS (like FreeRTOS), we need to implement a non blocking state machine.
In many program we can see the easy way, but not maintenable, that use a switch/case called each time in main loop.
This library use a better way...

## What is a state ?

A state is described by 3 actions: 

* *on_enter* : what to do on enter
* *do_job* : what to do on *event*
* *on_exit* : what to do on exit

Switching from a state to another is managed in *do_job* regarding which *event* is received. 

## What is an event ?

An event is identified by an integer value and has sometimes attaches data.
By example, an event can be "button pushed" and the attached data can be "the button identifier"

## Build your state machine

### Initialization 

//declare an enumeration with wanted states

typedef enum
{
  my_state_eSTATE_1 = 0,
  my_state_eSTATE_2,
  my_state_eSTATE_3,
  my_state_eSTATE_4,
  my_state_eSTATE_5,
  my_state_eCOUNT // only to know how much states you have
}my_states_t;

// declare your machine

statemachine_t  my_machine;


// in your initialization function

void my_machine_init(void)
{
  // declare states

  const statemachine_state_t states[my_state_eCOUNT]={
			statemachineSTATE(my_state_eSTATE_1, ID), // this state as Enter action (I) and Do action (D) 
			statemachineSTATE(my_state_eSTATE_2, IDO), // this state as Enter, Do and Exit action (O)
			statemachineSTATE(my_state_eSTATE_3, DO), // this state as Do an exit action
			statemachineSTATE(my_state_eSTATE_4, D), // this state as only Do action
			statemachineSTATE(my_state_eSTATE_5, ID)
	  };
    
   // initialize machine
  statemachine_init(&my_machine,
					my_state_eSTATE_3,     // entry state
					states);

  // when ready, you can start the machine
	statemachine_start(&my_machine);
}

### Implement callbacks

// Do job callback
statemachineDO_JOB_CLBK(my_machine_STATE_2)
{
  // if you never access event attached data, add the following line
  statemachineNO_DATA();

  // you access the event id with statemachineEVENT_ID()
  //Example :
  switch (statemachineEVENT_ID())
	{
    case my_event_eEVENT_1: 
      //some job 
      // you can access attached data address with statemachineEVENT_DATA()
      break;
    case my_event_eEVENT_2:
      // some job with state change
      statemachine_set_state(&my_machine, my_state_eSTATE3);
      break;  
    default:
    break;
  } 
}

## Code example

//TODO !
