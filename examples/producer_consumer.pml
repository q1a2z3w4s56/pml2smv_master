/*
 * Producer-Consumer Example using Channels
 * Demonstrates channel operations: send (!), receive (?), empty, full
 */

mtype = {ITEM1, ITEM2, ITEM3};

chan buffer = [2] of {mtype};

active proctype Producer() {
    mtype item;
    do
    :: true ->
        /* Produce an item */
        if
        :: item = ITEM1
        :: item = ITEM2
        :: item = ITEM3
        fi;
        
        /* Send to buffer (blocks if full) */
        buffer ! item
    od
}

active proctype Consumer() {
    mtype item;
    do
    :: true ->
        /* Receive from buffer (blocks if empty) */
        buffer ? item
        /* Consume the item */
    od
}
