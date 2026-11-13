# Practical 4: Clock Synchronization and Leader Election

## Aim

To simulate Berkeley clock synchronization and the Bully and Ring leader
election algorithms.

## Theory

Distributed computers can have different local clock readings. In the Berkeley
algorithm, a master asks for the other clocks, calculates their offsets from
its own clock, finds the average offset, and tells each process how much to
adjust its clock.

Leader election is used to select a coordinator when the current coordinator
fails. In the **Bully algorithm**, a process sends election messages to active
processes with higher IDs. The highest active process becomes the coordinator
and announces itself. In the **Ring algorithm**, processes are arranged in a
logical ring. An election message circulates through active processes with
their IDs; the highest ID in the message wins. A coordinator message then
circulates to notify the active processes.

This Python program simulates five processes in one program. The clock values,
process failures, and message exchanges are represented as data and printed;
the script does not start separate computers or send network messages.

## Files and roles

| File | Role |
|---|---|
| `algorithms.py` | Simulates Berkeley synchronization, Bully election, and Ring election in sequence. |

## Program

### `algorithms.py`

```python
def berkeley():
    clocks = [10, 15, 12, 8, 20]
    master = 0

    offsets = [clock - clocks[master] for clock in clocks]
    average_offset = sum(offsets) / len(offsets)

    print("\nBERKELEY CLOCK SYNCHRONIZATION")
    print("Initial clocks:", clocks)
    print("Offsets:", offsets)

    for i in range(len(clocks)):
        clocks[i] += round(average_offset - offsets[i])

    print("Synchronized clocks:", clocks)


def bully():
    processes = [1, 2, 3, 4, 5]
    failed = 5
    active = [pid for pid in processes if pid != failed]
    initiator = 2

    print("\nBULLY LEADER ELECTION")
    print(f"P{failed} (coordinator) has failed.")
    print(f"P{initiator} starts an election.")

    for pid in active:
        if pid > initiator:
            print(f"P{initiator} sends ELECTION to P{pid}; P{pid} replies OK.")

    leader = max(active)
    print(f"P{leader} has no higher active process, so it becomes coordinator.")
    print(f"P{leader} broadcasts COORDINATOR.")


def ring():
    processes = [1, 2, 3, 4, 5]
    failed = 5
    active = [pid for pid in processes if pid != failed]
    initiator = 2
    election_list = []

    print("\nRING LEADER ELECTION")
    print(f"P{failed} has failed.")
    print(f"P{initiator} starts an election.")

    index = processes.index(initiator)
    while True:
        pid = processes[index]
        if pid in active:
            election_list.append(pid)
            print(f"P{pid} is added to the election message: {election_list}")

        index = (index + 1) % len(processes)
        if processes[index] == initiator:
            break

    leader = max(election_list)
    print(f"P{leader} has the highest ID and becomes coordinator.")

    index = processes.index(leader)
    while True:
        pid = processes[index]
        if pid in active:
            print(f"P{pid} recognizes P{leader} as coordinator.")

        index = (index + 1) % len(processes)
        if processes[index] == leader:
            break


berkeley()
bully()
ring()
```
| Line(s) | Explanation |
|---|---|
| 1 | Defines the Berkeley synchronization function. |
| 2 | Sets the simulated clock reading for each of five processes. |
| 3 | Selects process 0 as the master. |
| 5 | Calculates each clock's offset from the master's reading. |
| 6 | Finds the average of all clock offsets. |
| 8-10 | Prints the algorithm name, initial clock readings, and offsets. |
| 12-13 | Adjusts each clock toward the average offset. |
| 15 | Prints the corrected clock values. |
| 18 | Defines the Bully election function. |
| 19 | Lists the process IDs. The highest ID has the highest priority. |
| 20 | Chooses process 5 as the failed coordinator. |
| 21 | Creates a list of processes that are still active. |
| 22 | Selects process 2 to start the election. |
| 24-26 | Prints the failure and election-start messages. |
| 28 | Checks each active process. |
| 29 | Selects active processes whose IDs are higher than the initiator's. |
| 30 | Displays an ELECTION message and OK reply for each higher process. |
| 32 | Chooses the highest active process ID as the new coordinator. |
| 33-34 | Prints why the winner is selected and shows its coordinator announcement. |
| 37 | Defines the Ring election function. |
| 38 | Stores process IDs in their logical ring order. |
| 39 | Chooses process 5 as failed. |
| 40 | Creates a list containing the active processes. |
| 41 | Selects process 2 as the election initiator. |
| 42 | Creates an empty list for IDs carried in the election message. |
| 44-46 | Prints the failure and election-start messages. |
| 48 | Finds process 2's position in the ring. |
| 49 | Starts the loop that passes the election message around the ring. |
| 50 | Gets the process at the current ring position. |
| 51-53 | If that process is active, adds its ID to the election list and displays the list. |
| 55 | Advances to the next process, wrapping to the start of the ring when needed. |
| 56-57 | Stops after the message has returned to the initiator. |
| 59 | Selects the highest active ID in the election list as the leader. |
| 60 | Announces the selected coordinator. |
| 62 | Starts the coordinator announcement at the leader's position in the ring. |
| 63 | Starts a second circulation loop for the coordinator announcement. |
| 64 | Gets the process at the current ring position. |
| 65-66 | If the process is active, prints that it recognizes the coordinator. |
| 68 | Advances to the next process and wraps around the ring if needed. |
| 69-70 | Stops after the announcement returns to the leader. |
| 73-75 | Calls each algorithm in order so all three demonstrations run. |

## How to run

Open a terminal in this folder and run:

```sh
python algorithms.py
```

If your system uses the `python3` command, run `python3 algorithms.py` instead.
The script runs all three simulations in sequence.

## Execution flow to remember

1. **Berkeley:** calculate clock offsets, average them, and adjust every clock.
2. **Bully:** send election messages to higher active IDs; the highest active ID wins.
3. **Ring:** circulate IDs in an election message; the highest ID wins and the coordinator message goes around the ring.

## Viva questions and short answers

1. **What is clock synchronization?**  
   It is the process of coordinating local clock readings across distributed
   processes or computers.

2. **How does the Berkeley algorithm synchronize clocks?**  
   A master calculates clock offsets, averages them, and sends each process an
   adjustment.

3. **What is a clock offset?**  
   It is the difference between a process's clock and the master's clock.

4. **What is leader election?**  
   It is the process of selecting a coordinator to manage work in a distributed
   system.

5. **Why is it called the Bully algorithm?**  
   A higher-ID active process can take over an election started by a lower-ID
   process, and the highest active ID wins.

6. **Which process wins in this Bully example?**  
   Process 4, because process 5 has failed and 4 is the highest active ID.

7. **How does the Ring election algorithm work?**  
   An election message passes around a logical ring with active process IDs; the
   highest ID in the message becomes the coordinator.

8. **What happens to a failed process in the Ring example?**  
   It is skipped when the election and coordinator messages circulate.

9. **What is the difference between Bully and Ring election?**  
   Bully sends election messages to higher IDs; Ring passes an election message
   around a logical ring.

10. **Does this program communicate over a network?**  
    No. It simulates the processes and messages in one Python program.
