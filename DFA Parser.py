import sys
from re import split as spl

if len(sys.argv) == 1:
    print('Fatal error: Config file must be given.')
    quit()

sigma = []
states = []
transitions = []
F = []
S = ''

with open(sys.argv[1]) as f:
    lines = f.readlines()

    if not lines:
        print('Fatal error: Config file cannot be empty.')
        quit()

    index = 0
    while index < len(lines):
        if not (lines[index].strip()):
            print('Format error: Lines cannot be empty.')
            quit()

        elif lines[index][0] != '#':
            if 'Sigma:' == lines[index].strip():
                index += 1
                while index < len(lines) and 'End' != lines[index].strip():
                    if lines[index][0] != '#':
                        if lines[index].strip() in {'', 'States:', 'Transitions:'}:
                            print('Format error: Section "Sigma" must end with "End" line.')
                            quit()
                        elif not (lines[index].strip().isalnum()):
                            print('Format error: Section "Sigma" can only contain alphanumerical values.')
                            quit()
                        sigma.append(lines[index].strip())

                    index += 1
                index += 1

            elif 'States:' == lines[index].strip():
                index += 1
                while index < len(lines) and 'End' != lines[index].strip():
                    if lines[index][0] != '#':
                        if lines[index].strip() in {'', 'Sigma:', 'Transitions:'}:
                            print('Format error: Section "States" must end with "End" line.')
                            quit()

                        state = lines[index].strip().rstrip(" ,F").rstrip(" ,S")
                        if not (state.strip().isalnum()):
                            print('Format error: Section "States" can only contain alphanumerical values.')
                            quit()

                        states.append(state)
                        if ',F' in lines[index]:
                            F.append(state)
                        if ',S' in lines[index]:
                            if S != '':
                                print('Condition error: There can only be one initial state.')
                                quit()
                            else:
                                S = state

                    index += 1
                index += 1

            elif 'Transitions:' == lines[index].strip():
                index += 1
                while index < len(lines) and 'End' != lines[index].strip():
                    if lines[index][0] != '#':
                        if lines[index].strip() in {'', 'Sigma:', 'States:'}:
                            print('Format error: Section "Transitions" must end with "End" line.')
                            quit()

                        currentTransition = tuple([x for x in spl('[,\s+]+', lines[index]) if x])
                        if len(currentTransition) != 3:
                            print('Format error: Section "Transitions" must contain 3 values for each line.')
                            quit()
                        for transition in currentTransition:
                            if not (transition.strip().isalnum()):
                                print('Format error: Section "Transitions" can only contain alphanumerical values.')
                                quit()

                        transitions.append(currentTransition)

                    index += 1
                index += 1

            else:
                print('Format error: Config file can only contain "Sigma:", "States:" and "Transitions:" sections.')
                quit()

        else:
            index += 1
