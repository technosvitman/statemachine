/**
 * AUTO GENERATED FILE
 */ 

#ifndef __TEST_MACHINE_H__
#define __TEST_MACHINE_H__

/**
 * @brief State list
 */
typedef enum
{
    /**
     * @brief 
     */
    test_machine_state_eSTATE1 = 0,
    /**
     * @brief 
     */
    test_machine_state_eSTATE2,
    /**
     * @brief 
     */
    test_machine_state_eSTATE3,
    /**
     * @brief amount of values
     */
    test_machine_state_eCOUNT
}
test_machine_state_t;

/**
 * @brief Event list
 */
typedef enum
{
    /**
     * @brief Conditional test event
     */
    test_machine_event_eEVENT1 = 0,
    /**
     * @brief Conditional test event from state 2
     */
    test_machine_event_eEVENT2,
    /**
     * @brief test event for transition to state 2
     */
    test_machine_event_eEVENT_1_2,
    /**
     * @brief amount of values
     */
    test_machine_event_eCOUNT
}
test_machine_event_t;


void test_machine_Init( void );
void test_machine_Compute( test_machine_event_t event, void * data );

#endif // __TEST_MACHINE_H__