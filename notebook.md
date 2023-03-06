# Engineering Notebook

## Part 1: Design
Instead of the producer/consumer structure that we were advised to follow in lab, we constructed a `VirtualMachine` class that had internal methods to initialize the machine, send messages, receive messages, connect, update the Lamport clock, and write to a log file for that machine. This yielded the added benefits of neither needing to store global data structures nor using pairwise buffers.

We chose to store incoming messages in a `Queue` object from the `multiprocessing` package, because its existing `put` and `get` functionalities made it easy for what we wanted to achieve. 

## Part 2: Experimental Analysis

### Procedure

We ran our code 5 times, each run lasting a random duration between 1-3 minutes.

### Results and Reflections
- discuss (in the lab book) the size of the jumps in the values for the logical clocks, drift in the values of the local logical clocks in the different machines (you can get a god’s eye view because of the system time), and the impact different timings on such things as gaps in the logical clock values and length of the message queue. 
- Observations and reflections about the model and the results of running the model are more than welcome.
- TODO: add the pictures/graphs from data analysis

