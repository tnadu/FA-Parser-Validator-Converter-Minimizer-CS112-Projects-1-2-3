from asyncio.windows_events import NULL
from os import remove
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


# Function that returns the index of a given element in a list
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
                        newStateTransitions[letter] = newStates[tuple(newState)] #current state's new name is added to newStateTransitions
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
                        newStateTransitions[letter] = newStates[tuple(newState)] #current state's new name is added to newStateTransitions
                else:  # newState is empty, so current DFA state doesn't transition into any other state
                    newStateTransitions[letter] = None
            transitions1[states1[index]] = newStateTransitions
        index += 1

    return states1, newStates, transitions1, F1

def MinimizeDFA():
    # transitions3 contains the path each state is following within the DFA through each letter of sigma
    # transitions3 = {q0:{letter0:qi, letter1:qj...}, q1:{...}, ...}
    transitions3={}
    for state in states:
        transitions3[state]={}
        for letter in sigma:
            for state1 in states:
                if T[getIndex(state)][getIndex(state1)]==letter:
                    transitions3[state][letter]=state1
                    break
    # states0 contains tuples of equivalent states - that will be merged in order to create a new general state
    states0=[]

    # T1 - tool used to collect tuples of equivalent states
    # T1[i][j]={0, if both state[i] and state[j] are either final states or simple states
    #           1, if state[i] and state[j] are different on this matter}

    T1=[[NULL for i in range(len(states))] for i in range(len(states))]
    for i in range(len(states)):
        for j in range(i):
            if (states[i] in F and states[j] in F) or (states[i] not in F and states[j] not in F):
                T1[i][j]=T1[j][i]=0
                states0.append((states[i], states[j]))
            else:
                T1[i][j]=T1[j][i]=1
    # checking if all tuples in states0 are prone to be merged into a new state
    verify=0
    while not verify: 
        verify=1
        for state in states0:
            for letter in sigma:
                if verify:
                    if transitions3[state[0]].get(letter, NULL)!=NULL:
                        # the corresponding index of state[0] within array T1
                        index1=getIndex(transitions3[state[0]][letter])

                        if transitions3[state[1]].get(letter, NULL)!=NULL:
                            # the corresponding index of state[1] within array T1
                            index2=getIndex(transitions3[state[1]][letter])

                            if T1[index1] [index2]==1 or T1[index2] [index1]==1:
                                # the tuple cannot be merged, hence it is removed from states0
                                verify=0
                                T1[getIndex(state[0])] [getIndex(state[1])]=T1[getIndex(state[1])] [getIndex(state[0])]=1
                                states0.remove(state)
                                break
    clasa={}
    index=0
    for pair in states0:
        #verific daca are vreun element comun cu o clasa de echivalenta
        added=False
        for element in pair:
            if added==False:
                for key in clasa.keys():
                    if element in clasa[key]:
                        clasa[key].add(pair[0])
                        clasa[key].add(pair[1])
                        added=True
        #daca nu l-am adaugat in dictionar,creez o noua clasa de echivaenta
        if added==False:
            index+=1
            clasa[f'new_state_{index}']=set(pair)
    '''
    #dupa ce am creeat noile stari(clasele de echivalenta)
    #le updatez in lista states, care contine starile initiale
    cum fac asta? sterg starile care au fost "comprimate" in dictionarul clasa
    '''

    #elimin starile care au fost comprimate
    finalstates=[]
    for state in states:
        found=0
        for key in clasa.keys():
            if state in clasa[key]:
                found=1
                break
        if found==0:
            finalstates.append(state)
            clasa[state]=state
    #adaug starile noi, adica clasele de echivalenta
    for key in clasa.keys():
        finalstates.append(key)

    
    print(finalstates)
    print(clasa)

    return finalstates, clasa







#function that prints the converted DFA
def DFAdisplay():
    #SIGMA
    print("Sigma:")
    for i in range(len(sigma)):
        print(f"\t{sigma[i]}")
    print("End\n")

    #STATES
    print("States:")
    for i in range(len(states1)):
        if type(states1[i]) != tuple:
            print(f"\t{states1[i]}", end="")
        else:
            print(f"\t{newStates[states1[i]]}", end="")
        #the first index indicates the first state of the DFA
        if i==0:
            print(f", S", end="")
        #checking if the current state is final
        if set(states1[i]) in F1 or states1[i] in F1:
            print(f", F", end="")
        print()
    print("End:")

    #TRANSITIONS
    print("Transitions:")
    for state in transitions1:
        for letter in transitions1[state]:
            if transitions1[state][letter]!=None:
                if type(state)!=tuple:
                    print(f"\t{state}, {letter}, {transitions1[state][letter]}")
                else:
                    state2=transitions1[state][letter]
                    state1=newStates[state] #current state's new name will be displayed
                    print(f"\t{state1}, {letter}, {state2}")     
    print("End")

# T-list that stores each 3-tuple in transitions (state1, letter, state2) where T[state1_index][state2_index]=letter
# initially, each value within it is null
T = [["null" for i in range(len(states))] for i in range(len(states))]

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
        if letter in T[state1]:  # testing for determinism; we check if current letter is already an element of T[state1]
            print("Condition error: DFA must have unique transition letters for each state")
            quit()
        else:  # registers the current tuple
            T[state1][state2] = letter

    print("Analyzed DFA is valid!")

    if len(sys.argv) == 3:
        print('Type \'0\' to quit or select one or both of the following options: ')
        print('1) simulate the Myhill-Nerode theorem - minimize a DFA to the smallest DFA with the same level of completeness')
        print('2) check word validity')
        command = [int(x) for x in input('>>> ').split()]
        check = True

        # command input format checking
        while check:
            check = False
            if len(command) > 3:
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
                MinimizeDFA()######
                #DFAdisplay()

            
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
                        print(f"The word '{word}' was not accepted by the DFA")
                        quit()
                        break

                if not stop and currentState in [int(x) for x in F]:  # finally, we check that the final state is a member of F
                    print(f"The word '{word}' was accepted by the DFA!")
                else:
                    print(f"The word '{word}' was not accepted by the DFA")

    # no word received for validation
    else:
        print('Would you like to simulate the Myhill-Nerode theorem - minimize a DFA to the smallest DFA with the same level of completeness?')
        print('Type \'1\' for \'yes\' or \'0\' for \'no\'')
        command = int(input('>>> '))

        while command > 1 or command < 0:
            print(f'Error: \'{command}\' not a valid option')
            command = int(input('>>> '))

        if command == 0:
            quit()
        elif command == 1:
            MinimizeDFA()
            #DFAdisplay()###########

            quit()

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
        T[state1][state2] = letter

    print("Analyzed NFA is valid!")

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
            DFAdisplay()

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
            if len(command) > 3:
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
                states1, newStates, transitions1, F1 = convertToDFA()
                DFAdisplay()

            elif num == 2:
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
