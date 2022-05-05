OVH project:

The goal of this task is to prepare statistical analysis of set of data from disks.

Each entry of the data set consists of following fields separated by ;
character:

    datacenter
    hostname
    disk serial
    disk age (in s)
    total reads
    total writes
    average IO latency from 5 minutes (in ms)
    total uncorrected read errors
    total uncorrected write errors

The proper solution (a script in Python) should output following
information:

DONE:    How many disks are in total and in each DC

DONE:    Which disk is the youngest/oldest one and what is its age (in days)

DONE:    What's the average disk age per DC (in days)

DONE:    How many read/write IO/s disks processes on average

DONE:    Find top 5 disks with lowest/highest average IO/s (reads+writes, print disks and their avg IO/s)

DONE:    Find disks which are most probably broken, i.e. have non-zero uncorrected errors (print disks and error counter)

DONE:    There should also be tests that verify if parts of the script are processing data properly.
