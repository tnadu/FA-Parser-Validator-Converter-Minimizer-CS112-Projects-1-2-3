if len(sys.argv) == 3:
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
                if word[queueIndex] in T[index(current_state)][index(state)]:
                    nextStates.append(state)
    queue = nextStates
    queueIndex += 1

if valid and set(F).intersection(set(queue)):
    print("word accepted")
else:
    print("word not accepted, fuck off!")
