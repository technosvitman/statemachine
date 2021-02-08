# statemachine

## Introduction

In many microcontroler programs, without the help of tiny OS (like FreeRTOS), we need to implement a non-blocking state machine.
In many programs we just can see the easy way, which will be quite difficult to maintain afterwards : a switch/case called each time in the main loop.
This library uses a more efficient way and has lower energy costs : State's action and state change on event.

## What is a state ?

A state is described by 3 actions: 

* *on_enter* : what to do on enter
* *do_job* : what to do on *event*
* *on_exit* : what to do on exit

Switching from a state to another is managed by *do_job* regarding which *event* is recieved. 

## What is an event ?

An event is identified by an integer value and sometimes has attached data.
For example, an event can be "button pushed" and the attached data can be "the button identifier"

## Build your state machine

### Initialization 

#### In your header file

```C
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

//declare an enumeration with wanted event

typedef enum
{
  my_event_eEVENT_1 = 0,
  my_event_eEVENT_2,
  my_event_eEVENT_3
}my_event_t;
```
#### In your source file

```C
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
```

### Implement callbacks

```C
// Do job callback
statemachineDO_JOB_CLBK(my_state_eSTATE_2)
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


// On enter callback
statemachineON_ENTER_CLBK(my_state_eSTATE_2)
{
	//some job	
}


// On exit callback
statemachineON_EXIT_CLBK(my_state_eSTATE_2)
{
	//some job	
}
```

### Send event to state machine

```C
// every where in your code call this function
statemachine_compute(&my_machine, my_event_eEVENT_1, data); 

// in this exemple we send my_event_eEVENT_1 whith some data
// you can also send nothing by passing NULL

statemachine_compute(&my_machine, my_event_eEVENT2, NULL);

```
