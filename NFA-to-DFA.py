# *1 = tuple members of comverted NFA

states1 = [S]  # new DFA states
newStates = {}  # dictionary for keeping track of new states' names
transitions1 = {}  # new DFA transitions
F1 = [*F]  # new DFA final states

notationIndex = 0  # int variable for new states naming
index = 0  # variable for traversing new DFA states (states1)
# unless no more new states have been added and all previously added states have been checked, proceed
while index < len(states1):
    # current DFA state is one of the original NFA's states
    if type(states1[index]) != tuple:
        newStateTransitions = {}  # dictionary for each DFA state, which will be nested in transitions1
        for letter in sigma:  # for every letter of the alphabet, a new possible state will be created to store the states ->
            newState = []  # that the current state transitions into
            finalState = False  # bool variable to check whether newState contains an original final state
            for i in range(len(states)):
                if T[getIndex(states1[index])][i] == letter:
                    newState.append(states[i])
                    if states[i] in F:  # newState contains an original final state
                        finalState = True

            if newState:  # we check if any states have been found
                if len(newState) == 1:  # newState is an original NFA state
                    newState = ''.join(newState)
                    if newState not in states1:  # original NFA state is checked for in DFA states
                        states1.append(newState)
                    newStateTransitions[letter] = newState  # original NFA state - letter pair is added to current states1 state's transitions

                else:  # newState contains multiple original NFA states
                    # check whether newState is an unstored state
                    found = False
                    for state in states1:
                        if set(newState) == set(state):
                            found = True
                            break

                    if not found:  # if newState is unstored ->
                        newStates[tuple(newState)] = f'new_state_{notationIndex}'  # it is assigned a new name ->
                        states1.append(tuple(newState))  # and it's stored in the DFA's states
                        notationIndex += 1
                        # newState contains an original NFA state, therefore it's a final state of the DFA
                        if finalState:
                            F1.append(set(newState))
                    # original NFA state - letter pair is added to current states1 state's transitions
                    newStateTransitions[letter] = tuple(newState)
            else:  # newState is empty, so current DFA state doesn't transition into any other state
                newStateTransitions[letter] = None
        transitions1[states1[index]] = newStateTransitions

    # current DFA state isn't an original NFA state, therefore it's composed
    else:
        newStateTransitions = {}  # dictionary for each DFA state, which will be nested in transitions1
        for letter in sigma:  # for every letter of the alphabet, a new possible state will be created to store the states ->
            newState = []  # that the current state transitions into
            finalState = False  # bool variable to check whether newState contains an original final state
            # all component states' transitioned states will be added to newState
            for state in states1[index]:
                for i in range(len(states)):
                    if T[getIndex(state)][i] == letter:
                        if states[i] not in newState:
                            newState.append(states[i])
                        if states[i] in F:  # newState contains an original final state
                            finalState = True

            if newState:  # we check if any states have been found
                if len(newState) == 1:  # newState is an original NFA state
                    newState = ''.join(newState)
                    if newState not in states1:  # original NFA state is checked for in DFA states
                        states1.append(newState)
                    newStateTransitions[letter] = newState  # original NFA state - letter pair is added to current states1 state's transitions

                else:  # newState contains multiple original NFA states
                    # check whether newState is an unstored state
                    found = False
                    for state in states1:
                        if set(newState) == set(state):
                            found = True
                            break

                    if not found:  # if newState is unstored ->
                        newStates[tuple(newState)] = f'new_state_{notationIndex}'  # it is assigned a new name ->
                        states1.append(tuple(newState))  # and it's stored in the DFA's states
                        notationIndex += 1
                        # newState contains an original NFA state, therefore it's a final state of the DFA
                        if finalState:
                            F1.append(set(newState))
                    # original NFA state - letter pair is added to current states1 state's transitions
                    newStateTransitions[letter] = tuple(newState)
            else:  # newState is empty, so current DFA state doesn't transition into any other state
                newStateTransitions[letter] = None
        transitions1[states1[index]] = newStateTransitions
    index += 1