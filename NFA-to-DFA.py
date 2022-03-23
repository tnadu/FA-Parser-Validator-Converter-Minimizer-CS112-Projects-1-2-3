# *1 = tuple members of comverted NFA


states1=[S]
newStates={}
transitions1={}
F1=[*F]

notationIndex=0
i=0
while i<len(states1):
    if type(states1[i]) != set:
        newStateTransitions = {}
        for letter in sigma:
            newState = []
            finalState=False
            for i in range(len(states)):
                if T[getIndex(states1[i])][i] == letter:
                    newState.append(sigma[i]) # getState receives index of state and returns state itself
                    if sigma[i] in F:
                        finalState=True

            if newState:
                if set(newState) not in newStates:
                    newStates[set(newState)] = f'new_state_{notationIndex}'
                    notationIndex+=1
                    if finalState:
                        F1.append(set(newState))
                newStateTransitions[letter]=set(newState)
            else:
                newStateTransitions[letter] = None
        transitions1[states1[i]]=newStateTransitions

    else:
        newStateTransitions = {}
        for letter in sigma:
            newState = []
            finalState=False
            for state in states1[i]:
                for i in range(len(states)):
                    if T[getIndex(state)][i] == letter:
                        newState.append(sigma[i])  # getState receives index of state and returns state itself
                        if sigma[i] in F:
                            finalState=True

            if newState:
                if set(newState) not in newStates:
                    newStates[set(newState)] = f'new_state_{notationIndex}'
                    notationIndex += 1
                    if finalState:
                        F1.append(set(newState))
                newStateTransitions[letter] = set(newState)
            else:
                newStateTransitions[letter] = None
        transitions1[states1[i]] = newStateTransitions
    i+=1

