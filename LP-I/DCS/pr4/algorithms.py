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
