import sys
from re import split as spl

if len(sys.argv) == 1:  # 1st case: only python file name passed as argument in CLI
    print('Error: Config file must be given')
    quit()
elif len(sys.argv) == 2:  # 2nd case: only config file name passed as argument in CLI, no word passed for validation
    print('No word received for validation\nChecking validity of config file...')
elif len(sys.argv) == 3:  # 3rd case: both config file name and word passed as arguments in CLI
    print('Checking validity of config file...')
    word = sys.argv[2]
else:  # 4th case: too many arguments passed in CLI
    print('Error: Too many arguments')
    quit()

sigma = []
states = []
transitions = []
F = []
S = ''

with open(sys.argv[1]) as f:
    lines = f.readlines()

    if not lines:  # config file empty
        print('Error: Config file cannot be empty')
        quit()

    index = 0  # using variable index to go through each line
    while index < len(lines):
        if not (lines[index].strip()):  # if line is empty, return error
            print('Format error: Lines cannot be empty')
            quit()

        elif lines[index][0] != '#':  # if current line is not commented, begin search
            if 'Sigma:' == lines[index].strip():  # beginning of 'Sigma' section
                index += 1
                while index < len(lines) and 'End' != lines[index].strip():
                    if lines[index][0] != '#':
                        # if either beginning of other sections or empty line is encountered, throw error message
                        if lines[index].strip() in {'', 'States:', 'Transitions:'}:
                            print('Format error: Section "Sigma" must end with "End" line')
                            quit()
                        elif not (
                                lines[index].strip().isalnum()):  # only alphanumerical characters allowed for declaring letters
                            print('Format error: Section "Sigma" can only contain alphanumerical values')
                            quit()
                        sigma.append(lines[index].strip())

                    index += 1
                index += 1

            elif 'States:' == lines[index].strip():  # beginning of 'States' section
                index += 1
                while index < len(lines) and 'End' != lines[index].strip():
                    if lines[index][0] != '#':
                        if lines[index].strip() in {'', 'Sigma:', 'Transitions:'}:
                            print('Format error: Section "States" must end with "End" line')
                            quit()

                        # state name is stored for validation, regardless of identifiers (S or F)
                        state = lines[index].strip().rstrip(" ,FS").strip()
                        if not (state.strip().isalnum()):
                            print('Format error: Section "States" can only contain alphanumerical values')
                            quit()

                        states.append(state)

                        # if F identifier (by itself or along with S identifier) is found in current line, the state is stored
                        if ',F' in lines[index] or ',FS' in lines[index] or ',SF' in lines[index] or ', F' in lines[
                            index] or ', FS' in lines[index] or ', SF' in lines[index]:
                            F.append(state)

                        # if S identifier (by itself or along with F identifier) is found in current line, we check
                        # if initial state has already been set. either an error is thrown or the state is stored
                        if ',S' in lines[index] or ',FS' in lines[index] or ',SF' in lines[index] or ', S' in lines[
                            index] or ', FS' in lines[index] or ', SF' in lines[index]:
                            if S != '':
                                print('Condition error: There can only be one initial state')
                                quit()
                            else:
                                S = state

                    index += 1
                index += 1

            elif 'Transitions:' == lines[index].strip():  # beginning of 'Transitions' section
                index += 1
                while index < len(lines) and 'End' != lines[index].strip():
                    if lines[index][0] != '#':
                        if lines[index].strip() in {'', 'Sigma:', 'States:'}:
                            print('Format error: Section "Transitions" must end with "End" line')
                            quit()

                        # we split the line and store the values in a tuple for additional validation.
                        # if either more than 3 elements are encountered or non-alphanumerical characters
                        # are found, an error is thrown.
                        currentTransition = tuple([x for x in spl('[,\s+]+', lines[index]) if x])
                        if len(currentTransition) != 3:
                            print('Format error: Section "Transitions" must contain 3 values for each line')
                            quit()

                        transitions.append(currentTransition)

                    index += 1
                index += 1

            else:
                print('Format error: Config file can only contain "Sigma:", "States:" and "Transitions:" sections')
                quit()

        else:
            index += 1



def getIndex(element):
    for i in range(len(states)):
        if element == states[i]:
            return i


def convertToDFA():
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
                    if letter in T[getIndex(states1[index])][i]:
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
                        newStateTransitions[letter] = newStates[tuple(newState)]  # current state's new name is added to newStateTransitions
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
                        if letter in T[getIndex(state)][i]:
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
                        newStateTransitions[letter] = newStates[tuple(newState)]  # current state's new name is added to newStateTransitions
                else:  # newState is empty, so current DFA state doesn't transition into any other state
                    newStateTransitions[letter] = None
            transitions1[states1[index]] = newStateTransitions
        index += 1

    return states1, newStates, transitions1, F1


def printConvertedDFA():
    print("Sigma:")
    for i in range(len(sigma)):
        print(f"\t{sigma[i]}")
    print("End\n#")

    print("States:")
    for i in range(len(states1)):
        # current state is an original state
        if type(states1[i]) != tuple:
            print(f"\t{states1[i]}", end="")
        # current state is newly generated
        else:
            print(f"\t{newStates[states1[i]]}", end="")

        if i == 0:  # the first state of the DFA
            print(f", S", end="")

        if set(states1[i]) in F1 or states1[i] in F1:  # checking if the current state is final
            print(f", F", end="")
        print()
    print("End\n#")

    print("Transitions:")
    for state in transitions1:
        for letter in transitions1[state]:
            if transitions1[state][letter]:
                # current state is an original state
                if type(state) != tuple:
                    print(f"\t{state}, {letter}, {transitions1[state][letter]}")
                # current state is newly generated
                else:
                    state2 = transitions1[state][letter]
                    state1 = newStates[state]  # current state's new name will be displayed
                    print(f"\t{state1}, {letter}, {state2}")

    print("End")


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
                markings[i][j] = 0
                newStates.append([states[i], states[j]])
            else:
                markings[i][j] = 1

    # for marking in markings:
    #     print(*marking)
    #     print()
    #
    # print(newStates)
    # print()

    # checking if all tuples in newStates are prone to be merged into a new state
    verify = False
    # verification proceeds as long as modifications in markings have been made during the previous iteration
    while not verify:
        verify = True
        for newState in newStates:  # verifying every tuple whose marking is still 0
            # we check every letter in sigma, as long as the marking hasn't been modified to 1 (thus verify no longer being true)
            for letter in sigma:
                if verify:
                    # current letter transitions first state from newState (newState[0]) tuple into another state
                    if letter in transitions1[newState[0]].keys():
                        # the corresponding index of state[0] within matrix markings
                        index0 = getIndex(transitions1[newState[0]][letter])

                        # current letter transitions second state from newState (newState[1]) tuple into another state
                        if letter in transitions1[newState[1]].keys():
                            # the corresponding index of state[1] within matrix markings
                            index1 = getIndex(transitions1[newState[1]][letter])

                            # the tuple cannot be merged, hence it is removed from newStates
                            if markings[index0][index1] == 1 or markings[index1][index0] == 1:
                                verify = False
                                markings[getIndex(newState[0])][getIndex(newState[1])] = 1
                                newStates.remove(newState)
                                break


    # print(newStates)
    # print()

    finalStatesNames = {}  # compressed final states will be added here
    index = 0
    for pair in newStates:  # checking all tuples that have passed the marking verification
        # checking if pair has common elements with a finalState
        added = False
        for element in pair:
            if not added:
                for finalStateName in finalStatesNames:
                    if element in finalStatesNames[finalStateName]:
                        finalStatesNames[finalStateName].add(pair[0])
                        finalStatesNames[finalStateName].add(pair[1])
                        added = True
                        break
            else:
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
            if state in finalStatesNames[finalState]:
                found = True
                break
        # if it hasn't been found, we add it to both finalStates and finalStatesNames
        if not found:
            finalStates.append(state)
            finalStatesNames[state] = {state}
    # adding the new states in finalStates
    for finalState in finalStatesNames:
        if finalState not in finalStates:
            finalStates.append(finalState)

    # print(finalStatesNames)
    # print()
    # print(finalStates)

    transitionSets = {}  # will be used to store the states each final state transitions into, as sets
    S1 = ''  # new start state
    F1 = []  # new final states
    for finalStateName in finalStatesNames:  # iterating through the final states
        transitionSets[finalStateName] = {}

        if set(finalStatesNames[finalStateName]).intersection(F):
            F1.append(finalStateName)  # finalStatesNames[key] is a new final state
        if S1 == '' and S in finalStatesNames[finalStateName]:
            S1 = finalStateName  # finalStatesNames[key] is the new start state

        for letter in sigma:  # for every letter, the set of transitioned states from the states in finalStatesNames[key] is found
            transitionSets[finalStateName][letter] = set()
            for state in finalStatesNames[finalStateName]:
                transitionSets[finalStateName][letter].add(transitions1[state][letter])

    finalTransitions = {}
    for finalState in finalStates:
        finalTransitions[finalState] = {}
        for letter in sigma:
            for finalStateName in finalStatesNames:
                if transitionSets[finalState][letter].intersection(finalStatesNames[finalStateName]):
                    finalTransitions[finalState][letter] = finalStateName
                    break

    # print()
    # print(finalTransitions)

    return finalStates, finalTransitions, S1, F1


def printMinimizedDFA():
    print("Sigma:")
    for i in range(len(sigma)):
        print(f"\t{sigma[i]}")
    print("End\n#")

    print("States:")
    for state in finalStates:
        print(f"\t{state}", end="")

        if state == S1:
            print(f", S", end="")

        if state in F1:
            print(f", F", end="")
        print()
    print("End\n#")

    print("Transitions:")
    for state in finalTransitions:
        for letter in finalTransitions[state]:
            if finalTransitions[state][letter]:
                print(f"\t{state}, {letter}, {finalTransitions[state][letter]}")
    print("End")



# T-list that stores each 3-tuple in transitions (state1, letter, state2) where T[state1_index][state2_index]=letter
# initially, each value within it is null
T = [[[] for i in range(len(states))] for i in range(len(states))]

print('Select the type of finite automaton:')
print('1) deterministic')
print('2) nondeterministic')
command = int(input('>>> '))

while command > 2 or command < 1:
    print(f'Error: \'{command}\' not a valid option')
    command = int(input('>>> '))

# DFA menu
if command == 1:
    for transition in transitions:
        # verifies that all elements inside each tuple are valid members within states and sigma
        if transition[0] not in states:
            print(f'\'{transition[0]}\' not a valid state')
            quit()
        if transition[1] not in sigma:
            print(f'\'{transition[1]}\' not a valid letter')
            quit()
        if transition[2] not in states:
            print(f'\'{transition[2]}\' not a valid state')
            quit()

        state1, letter, state2 = getIndex(transition[0]), transition[1], getIndex(transition[2])
        for letters in T[state1]:
            if letter in letters:  # testing for determinism; we check if current letter is already an element of T[state1]
                print("Condition error: DFA must have unique transition letters for each state")
                quit()
        else:  # registers the current tuple
            T[state1][state2].append(letter)

    print("Analyzed DFA is valid!\n")

    # no word received for validation
    if len(sys.argv) == 2:
        print('Would you like to minimize the current DFA?')
        print('Type \'1\' for \'yes\' or \'0\' for \'no\'')
        command = int(input('>>> '))

        while command > 1 or command < 0:
            print(f'Error: \'{command}\' not a valid option')
            command = int(input('>>> '))

        if command == 0:
            quit()
        elif command == 1:
            print('Is the stored DFA complete?')
            print('Type \'1\' for \'yes\' or \'0\' for \'no\'')
            command = int(input('>>> '))

            while command > 1 or command < 0:
                print(f'Error: \'{command}\' not a valid option')
                command = int(input('>>> '))

            if command == 0:
                print('Algorithm only works for complete DFAs!')
                quit()
            elif command == 1:
                finalStates, finalTransitions, S1, F1 = minimizeDFA()
                print()
                printMinimizedDFA()
                quit()

    # word received for validation
    else:
        print('Type \'0\' to quit or select one or both of the following options: ')
        print('1) minimize DFA')
        print('2) check word validity')
        command = [int(x) for x in input('>>> ').split()]
        check = True

        # command input format checking
        while check:
            check = False
            if len(command) > 2:
                print('Error: Too many options')
                command = [int(x) for x in input('>>> ').split()]
                check = True
            else:
                for num in command:
                    if num > 2 or num < 0:
                        print(f'Error: \'{num}\' is not a valid option')
                        command = [int(x) for x in input('>>> ').split()]
                        check = True
                        break

        if 0 in command:
            quit()

        for num in command:
            if num == 1:
                print('Is the stored DFA complete?')
                print('Type \'1\' for \'yes\' or \'0\' for \'no\'')
                option = int(input('>>> '))

                while option > 1 or option < 0:
                    print(f'Error: \'{option}\' not a valid option')
                    option = int(input('>>> '))

                if option == 0:
                    print('Algorithm only works for complete DFAs!\n')
                elif option == 1:
                    finalStates, finalTransitions, S1, F1 = minimizeDFA()
                    print()
                    printMinimizedDFA()
                    print()

            elif num == 2:
                print("Checking validity for the given word...")
                # currentState ==> using this variable to navigate through each state
                currentState = 0

                for i in range(len(word)):  # each letter of the given word is verified
                    stop = True  # we assume that the word would not pass the verification test
                    for j in range(len(states)):
                        if T[currentState][j] == word[i]:
                            currentState = j
                            stop = False  # we continue the validation since the current letter was correct
                            break

                    if stop:
                        break

                if not stop and currentState in [int(x) for x in F]:  # finally, we check that the final state is a member of F
                    print(f"The word '{word}' was accepted by the DFA!")
                else:
                    print(f"The word '{word}' was not accepted by the DFA")


# NFA menu
elif command == 2:
    for transition in transitions:
        # verifies that all elements inside each tuple are valid members within states and sigma
        if transition[0] not in states:
            print(f'\'{transition[0]}\' not a valid state')
            quit()
        if transition[1] not in sigma and transition[1] != '*':
            print(f'\'{transition[1]}\' not a valid letter')
            quit()
        if transition[2] not in states:
            print(f'\'{transition[2]}\' not a valid state')
            quit()

        state1, letter, state2 = getIndex(transition[0]), transition[1], getIndex(transition[2])
        T[state1][state2].append(letter)

    print("Analyzed NFA is valid!\n")

    # no word received for validation
    if len(sys.argv) == 2:
        print('Would you like to convert the current NFA to an equivalent DFA?')
        print('Type \'1\' for \'yes\' or \'0\' for \'no\'')
        command = int(input('>>> '))

        while command > 1 or command < 0:
            print(f'Error: \'{command}\' not a valid option')
            command = int(input('>>> '))

        if command == 0:
            quit()
        elif command == 1:
            states1, newStates, transitions1, F1 = convertToDFA()
            print()
            printConvertedDFA()
            quit()

    # word received for validation
    else:
        print('Type \'0\' to quit or select one or both of the following options: ')
        print('1) convert NFA to DFA')
        print('2) check word validity')
        command = [int(x) for x in input('>>> ').split()]
        check = True

        # command input format checking
        while check:
            check = False
            if len(command) > 2:
                print('Error: Too many options')
                command = [int(x) for x in input('>>> ').split()]
                check = True
            else:
                for num in command:
                    if num > 2 or num < 0:
                        print(f'Error: \'{num}\' is not a valid option')
                        command = [int(x) for x in input('>>> ').split()]
                        check = True
                        break

        if 0 in command:
            quit()

        for num in command:
            if num == 1:  # convert NFA to DFA
                states1, newStates, transitions1, F1 = convertToDFA()
                print()
                printConvertedDFA()
                print()

            elif num == 2:  # NFA word acceptance
                print("Checking validity for the given word...")
                queue = [S]
                valid = True
                queueIndex = 0

                while queueIndex < len(word) and valid and queue:
                    nextStates = []
                    if word[queueIndex] not in sigma:
                        valid = False
                    else:
                        for current_state in queue:
                            for state in states:
                                if word[queueIndex] in T[getIndex(current_state)][getIndex(state)]:
                                    nextStates.append(state)
                    queue = nextStates
                    queueIndex += 1

                if valid and set(F).intersection(set(queue)):
                    print(f"The word '{word}' was accepted by the NFA!")
                else:
                    print(f"The word '{word}' was not accepted by the NFA")