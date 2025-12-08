/*
 * Dynamic Process Creation Example
 * Demonstrates the 'run' statement for spawning processes
 */

byte counter = 0;

proctype Worker(byte id) {
    counter = counter + 1;
    /* Worker does some work */
    counter = counter - 1
}

init {
    /* Create multiple worker processes */
    run Worker(1);
    run Worker(2);
    run Worker(3);
    
    /* Wait for workers */
    (counter == 0)
}
