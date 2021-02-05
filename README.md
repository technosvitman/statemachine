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

## Code example

//TODO !
