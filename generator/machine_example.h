
#ifndef MACHINE_EXAMPLE_H
#define MACHINE_EXAMPLE_H

/**
 * @brief State list
 */
typedef enum
{
  example_machine_state_eState1 = 0,
  example_machine_state_eState2,
  example_machine_state_eState3,
  example_machine_state_eState4,
  example_machine_state_eCOUNT
}
example_machine_state_t;

/**
 * @brief Event list
 */
typedef enum
{
  example_machine_event_eEvent1 = 0,
  example_machine_event_eEvent2,
  example_machine_event_eEvent3,
  example_machine_event_eEvent4,
  example_machine_event_eEvent5,
  example_machine_event_eEvent6,
  example_machine_event_eCOUNT
}
example_machine_event_t;


void example_machine_init( void );
void example_machine_compute( example_machine_event_t event, void * data );

#endif