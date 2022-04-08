def getIndex(element):
    for i in range(len(states)):
        if element == states[i]:
            return i


states = []
sigma = []
T = {{[]}}
F = []
S = ''


def minimizeDFA():
    # transitions1 contains the path each state is following within the DFA through each letter of sigma
    # transitions1 = {q0:{letter0:qi, letter1:qj...}, q1:{...}, ...}
    transitions1 = {}
    for state in states:
        transitions1[state] = {}
        for letter in sigma:
            for transitionedState in states:
                if letter in T[getIndex(state)][getIndex(transitionedState)]:
                    transitions1[state][letter] = transitionedState
                    break

    newStates = []  # newStates contains tuples of equivalent states - that will be merged in order to create a new general state

    # markings - matrix used to mark tuples of equivalent types (final or non-final) states
    # markings[i][j] = {0, if both state[i] and state[j] are either final states or non-final states
    #                   1, otherwise}
    markings = [[None for i in range(len(states))] for i in range(len(states))]
    for i in range(len(states)):
        for j in range(i):
            if (states[i] in F and states[j] in F) or (states[i] not in F and states[j] not in F):
                # markings[i][j] = markings[j][i] = 0
                markings[i][j] = 0
                newStates.append([states[i], states[j]])
            else:
                markings[i][j] = 1
                # markings[i][j] = markings[j][i] = 1



    # checking if all tuples in newStates are prone to be merged into a new state
    verify = False
    # verification proceeds as long as modifications in markings have been made during the previous iteration
    while not verify:
        verify = True
        for newState in newStates:  # verifying every tuple whose marking is still 0
            # we check every letter in sigma, as long as the marking hasn't been modified to 1 (thus verify no longer being true)
            for letter in sigma and verify:
                # current letter transitions first state from newState (newState[0]) tuple into another state
                if letter in transitions1[newState[0]].keys() and verify:
                    # the corresponding index of state[0] within matrix markings
                    index0 = getIndex(transitions1[newState[0]][letter])

                    # current letter transitions second state from newState (newState[1]) tuple into another state
                    if letter in transitions1[newState[1]].keys():
                        # the corresponding index of state[1] within matrix markings
                        index1 = getIndex(transitions1[newState[1]][letter])

                        # the tuple cannot be merged, hence it is removed from newStates
                        if markings[index0][index1] == 1 or markings[index1][index0] == 1:
                            verify = False
                            markings[getIndex(newState[0])][getIndex(newState[1])]
                            # markings[getIndex(newState[0])][getIndex(newState[1])] = markings[getIndex(newState[1])][getIndex(newState[0])] = 1
                            newStates.remove(newState)
                            break



    finalStatesNames = {}  # compressed final states will be added here
    index = 0
    for pair in newStates:  # checking all tuples that have passed the marking verification
        # checking if pair has common elements with a finalState
        added = False
        for element in pair and not added:
            for finalState in finalStatesNames:
                if element in finalState:
                    finalState.add(pair[0])
                    finalState.add(pair[1])
                    added = True
                    break
        # if pair was found not to have any common elements with any of the final states,
        # a new final state will be created
        if not added:
            finalStatesNames[f'newState{index}'] = set(pair)
            index += 1

    # after creating the new states, we check if there are any old states
    # remaining which haven't been contained in any of the new ones.
    finalStates = []
    for state in states:
        found = False
        # checking if 'state' is part of any new state
        for finalState in finalStatesNames:
            if state in finalState:
                found = True
                break
        # if it hasn't been found, we add it to both finalStates and finalStatesNames
        if not found:
            finalStates.append(state)
            finalStatesNames[state] = state
    # adding the new states in finalStates
    for key in finalStatesNames.keys():
        finalStates.append(key)



    transitionSets = {}  # will be used to store the states each final state transitions into, as sets
    S1 = ''  # new start state
    F1 = []  # new final states
    for key in finalStatesNames.keys():  # iterating through the final states
        transitionSets[finalStatesNames[key]] = {}

        if set(finalStatesNames[key]).intersection(F):
            F1.append(key)  # finalStatesNames[key] is a new final state
        if S1 == '' and S in finalStatesNames[key]:
            S1 = key  # finalStatesNames[key] is the new start state

        for letter in sigma:  # for every letter, the set of transitioned states from the states in finalStatesNames[key] is found
            transitionSets[finalStatesNames[key]][letter] = set()
            for state in finalStatesNames[key]:
                transitionSets[finalStatesNames[key]][letter].add(transitions1[state][letter])

    finalTransitions = {}
    for finalState in finalStates:
        finalTransitions[finalState] = {}
        for letter in sigma:
            for key in finalStatesNames.keys():
                if finalStatesNames[finalState][letter].intersection(finalStatesNames[key]):
                    finalTransitions[finalState][letter] = key
                    break

    return finalStates, finalTransitions, S1, F1
