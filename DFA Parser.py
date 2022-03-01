import sys
from re import split as spl

if len(sys.argv) == 1:      # 1st case: only python file name passed as argument in CLI
    print('Fatal error: Config file must be given.')
    quit()
elif len(sys.argv) == 2:    # 2nd case: only config file name passed as argument in CLI, no word passed for validation
    print('Parser: No word received for validation. Checking validity of config file.\n\n')
elif len(sys.argv) == 3:    # 3rd case: both config file name and word passed as arguments in CLI
    print('Parser: Checking validity of config file.\n\n')
else:                       # 4th case: too many arguments passed in CLI
    print('Fatal error: Too many arguments.')
    quit()

sigma = []
states = []
transitions = []
F = []
S = ''

# for debugging:
# with open('dfa_config_file') as f:

with open(sys.argv[1]) as f:
    lines = f.readlines()

    if not lines:   # config file empty
        print('Fatal error: Config file cannot be empty.')
        quit()

    index = 0           # using variable index to go through each line
    while index < len(lines):
        if not (lines[index].strip()):  # if line is empty, return error
            print('Format error: Lines cannot be empty.')
            quit()

        elif lines[index][0] != '#':                # if current line is not commented, begin search
            if 'Sigma:' == lines[index].strip():    # beginning of 'Sigma' section
                index += 1
                while index < len(lines) and 'End' != lines[index].strip():
                    if lines[index][0] != '#':
                        # if either beginning of other sections or empty line is encountered, throw error message
                        if lines[index].strip() in {'', 'States:', 'Transitions:'}:
                            print('Format error: Section "Sigma" must end with "End" line.')
                            quit()
                        elif not (lines[index].strip().isalnum()):      # only alphanumerical characters allowed for declaring letters
                            print('Format error: Section "Sigma" can only contain alphanumerical values.')
                            quit()
                        sigma.append(lines[index].strip())

                    index += 1
                index += 1

            elif 'States:' == lines[index].strip():     # beginning of 'States' section
                index += 1
                while index < len(lines) and 'End' != lines[index].strip():
                    if lines[index][0] != '#':
                        if lines[index].strip() in {'', 'Sigma:', 'Transitions:'}:
                            print('Format error: Section "States" must end with "End" line.')
                            quit()

                        # state name is stored for validation, regardless of identifiers (S or F)
                        state = lines[index].strip().rstrip(",FS").strip()
                        if not (state.strip().isalnum()):
                            print('Format error: Section "States" can only contain alphanumerical values.')
                            quit()

                        states.append(state)
                        # if F identifier (by itself or along with S identifier) is found in current line, the state is stored
                        if ',F' in lines[index] or ',FS' in lines[index] or ',SF' in lines[index]:
                            F.append(state)
                        # if S identifier (by itself or along with F identifier) is found in current line, we check
                        # if initial state has already been set. either an error is thrown or the state is stored
                        if ',S' in lines[index] or ',FS' in lines[index] or ',SF' in lines[index]:
                            if S != '':
                                print('Condition error: There can only be one initial state.')
                                quit()
                            else:
                                S = state

                    index += 1
                index += 1

            elif 'Transitions:' == lines[index].strip():        # beginning of 'Transitions' section
                index += 1
                while index < len(lines) and 'End' != lines[index].strip():
                    if lines[index][0] != '#':
                        if lines[index].strip() in {'', 'Sigma:', 'States:'}:
                            print('Format error: Section "Transitions" must end with "End" line.')
                            quit()

                        # we split the line and store the values in a tuple for additional validation.
                        # if either more than 3 elements are encountered or non-alphanumerical characters
                        # are found, an error is thrown.
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


# for debugging:
# print(states)
# print(sigma)
# print(transitions)
# print(F, S)
