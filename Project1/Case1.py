# Importing required libraries
import numpy as np
import timeit

# Creating a text file to store result
txt_file = open("Case1.txt", "w+")

# Starting the timer to calculate the time taken
start = timeit.timeit()

# Defining the initial position
initial = [[1, 2, 3, 4], [5, 6,0, 8], [9, 10, 7, 12], [13, 14, 11, 15]]

# Defining final state
final = '01020304050607080910111213141500'

# Converting the input to a double digit by accessing every element
# To prevent issues with duplicates because of double digits
for i in range(len(initial)):
    for j in range(len(initial)):
        # This function will convert the int to double digit by adding a leading zero
        initial[i][j] = "{0:0=2d}".format(initial[i][j])

# Creating a NP array for ease of operations
initial_arr = np.array(initial)


# Creating a function to find the blank
def find_blank(search_matrix):
    # Accessing each element from array
    for i in range(search_matrix.shape[0]):
        for j in range(search_matrix.shape[1]):

            # If that element is blank then return it
            if int(search_matrix[i, j]) == 00:
                return (i, j)


# Creating a function to convert array to string to match and store later
def cvt_arr_to_str(array_in):
    # Initializing the empty string to append to
    str_out = ''

    # Accessing each element
    for i in range(len(array_in)):
        for j in range(len(array_in)):
            # Appending each element to the string
            # Note that the array consists of elements in string type
            str_out = str_out + array_in[i][j]

    # Return the string
    return str_out


# Creating a function to move the blank by swapping it
def swap_values(of_matrix, prev_zero, new_zero):
    # Creating a copy to give to swap easily
    final_state = np.copy(of_matrix)

    # Copying element from previous state at position of new zero
    final_state[prev_zero] = final_state[new_zero]

    # Putting the blank at the new position
    final_state[new_zero] = '00'
    return final_state


# Creating legal moves for each position of current blank
for_00 = [(0, 1), (1, 0)]
for_01 = [(0, 0), (0, 2), (1, 1)]
for_02 = [(0, 1), (1, 2), (0, 3)]
for_03 = [(0, 2), (1, 3)]
for_10 = [(0, 0), (1, 1), (2, 0)]
for_11 = [(0, 1), (1, 0), (1, 2), (2, 1)]
for_12 = [(0, 2), (1, 1), (2, 2), (1, 3)]
for_13 = [(0, 3), (1, 2), (2, 3)]
for_20 = [(1, 0), (2, 1), (3, 0)]
for_21 = [(2, 0), (1, 1), (2, 2), (3, 1)]
for_22 = [(2, 1), (1, 2), (2, 3), (3, 2)]
for_23 = [(1, 3), (2, 2), (3, 3)]
for_30 = [(2, 0), (3, 1)]
for_31 = [(3, 0), (2, 1), (3, 2)]
for_32 = [(3, 1), (2, 2), (3, 3)]
for_33 = [(3, 2), (2, 3)]


# Storing legal moves in an array with corresponding position
all_combi = [[for_00, for_01, for_02, for_03], [for_10, for_11, for_12, for_13], [for_20, for_21, for_22, for_23],
             [for_30, for_31, for_32, for_33]]

# Creating an array to temporarily store parent till execution
left_to_check = []

# Creating parent index to count iteration
parent_index = 0

# Index for the children
index = 0

# Creating the first parent / root of the tree
parent = initial_arr

# Converting it to an string to store into visited nodes
initial_srt = cvt_arr_to_str(initial_arr)

# Initializing a set of visited nodes
visited_nodes = set(initial_srt)

# Creating a tree list to tracebacks including parent index and the child
tree_list = [[parent_index, initial_arr]]

# Creating a variable to break the loop
not_solved = True


# Finding the blank location for the first time
blank_loc = find_blank(parent)

# Calculating the possible moves for the first parent / root
possible_moves = all_combi[blank_loc[0]][blank_loc[1]]


# Creating child for the first parent, it is hardcoded
# Doing this to first fill up the left_to_check list
# Iterating through all possible moves
for i in range(len(possible_moves)):

    # Each child could be a possible parent so applying swap and storing them
    possible_parent = swap_values(parent, blank_loc, possible_moves[i])

    # Converting it to string to check if that is visited (Fact!! Ii will not be for sure)
    possible_parent_str = cvt_arr_to_str(possible_parent)

    # Checking if it has been visited or Not
    if possible_parent_str in visited_nodes:
        continue

    # If not, store them to temporary list to generate their child
    # and adding it with its index to the tree_list for tracing back
    # Also adding it to the visited nodes, since it has been visited
    else:
        visited_nodes.add(possible_parent_str)
        index = index + 1
        tree_list.append([parent_index, possible_parent])
        left_to_check.append(possible_parent)


# Now iterating through all other parents and creating their child
# over and over till we have our solution
while not_solved:

    # Popping the first added node from the temp. list.
    # Not that pop(0) will be a FIFO type of system
    current_matrix = left_to_check.pop(0)

    # Incrementing the parent index
    parent_index = parent_index + 1

    # Finding the blank
    blank_loc = find_blank(current_matrix)

    # Getting list of possible moves
    possible_moves = all_combi[blank_loc[0]][blank_loc[1]]

    # Iterating through all possible moves
    for i in range(len(possible_moves)):

        # Each child could be a possible parent so applying swap and storing them
        possible_parent = swap_values(current_matrix, blank_loc, possible_moves[i])

        # Converting it to string to check if that is visited
        possible_parent_str = cvt_arr_to_str(possible_parent)

        # Checking if the result is the solution
        if possible_parent_str == final:

            # Changing the variable name to False to break out of the loop
            not_solved = False

            # Incrementing the index of the solution
            index = index + 1

            # Adding the solution to the tree
            tree_list.append([parent_index, possible_parent])
            break

        # Checking if it has been visited or Not
        elif possible_parent_str not in visited_nodes:

            # Adding that to set of visited nodes
            visited_nodes.add(possible_parent_str)

            # Incrementing index
            index = index + 1

            # Appending it to the tree
            tree_list.append([parent_index, possible_parent])

            # Appending it to temp. list to check next
            left_to_check.append(possible_parent)

# Now since we have the solution tracing back the path
# Creating a variable to check if traced back to initial state
Var = True

# creating a variable
m = len(tree_list) - 1
list_of_path = []
# Looping through to find the path
while Var:

    # Printing the path
    print(tree_list[m][1])

    # Saving the path
    list_of_path.append(tree_list[m][1])

    # Accessing the index and getting the parent index
    m = tree_list[m][0]

    # If reached the initial state, change variable to false
    # This will exit the loop
    if m == 0:
        print(tree_list[m][1])
        list_of_path.append(tree_list[m][1])
        Var = False

# Saving the path in caseX.txt file
txt_file.write("The path to solution is as follows \n\n")

# Saving the file to the caseX.txt file
for i in range(len(list_of_path)):
    txt_file.write("%s\n\n" %list_of_path[i])

# Stopping the clock
end = timeit.timeit()

# Printing the time taken
time_taken = abs(end - start)
print("Time Taken: ", time_taken)
