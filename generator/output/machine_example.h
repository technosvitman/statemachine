
#ifndef MACHINE_EXAMPLE_H
#define MACHINE_EXAMPLE_H

/**
 * @brief State list
 */
typedef enum
{
    /**
     * @brief My first state
     */
    example_machine_state_eSTATE1 = 0,
    /**
     * @brief My secibd state
     */
    example_machine_state_eSTATE2,
    /**
     * @brief My third state
     */
    example_machine_state_eSTATE3,
    /**
     * @brief My fourth state
     */
    example_machine_state_eSTATE4,
    /**
     * @brief amount of values
     */
    example_machine_state_eCOUNT
}
example_machine_state_t;

/**
 * @brief Event list
 */
typedef enum
{
    /**
     * @brief my seventh event
     */
    example_machine_event_eEVENT7 = 0,
    /**
     * @brief my fourth event
     */
    example_machine_event_eEVENT4,
    /**
     * @brief my sixth event
     */
    example_machine_event_eEVENT6,
    /**
     * @brief my first event
     */
    example_machine_event_eEVENT1,
    /**
     * @brief my second event
     */
    example_machine_event_eEVENT2,
    /**
     * @brief my third event
     */
    example_machine_event_eEVENT3,
    /**
     * @brief my fifth event
     */
    example_machine_event_eEVENT5,
    /**
     * @brief amount of values
     */
    example_machine_event_eCOUNT
}
example_machine_event_t;


void example_machine_Init( void );
void example_machine_Compute( example_machine_event_t event, void * data );

#endif