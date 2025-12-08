/*
 * Peterson's Mutual Exclusion Algorithm
 * Two processes competing for critical section access
 */

bool flag[2];
byte turn;

active proctype P0() {
    do
    :: true ->
        flag[0] = true;
        turn = 1;
        (flag[1] == false || turn == 0);
        /* critical section */
        flag[0] = false
    od
}

active proctype P1() {
    do
    :: true ->
        flag[1] = true;
        turn = 0;
        (flag[0] == false || turn == 1);
        /* critical section */
        flag[1] = false
    od
}
