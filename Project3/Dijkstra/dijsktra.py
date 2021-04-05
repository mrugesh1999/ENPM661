# Importing required libraries
import numpy as np
import cv2
import heapq
import math

# Creating a blank image of scale 3X
blank_image = np.zeros((900, 1200, 3), np.uint8)

# Assigning all values as gray
blank_image[:, :] = (128, 128, 128)  # (B, G, R)

# Setting max size of the search area
x_max = 300
y_max = 400


def plot_point(r, l):
    """
    This function will convert point to a scaled opencv image
    :param r: X coordinate of point
    :param l: Y coordinate of point
    :return: None
    """
    blank_image[r * 3:(r + 1) * 3, l * 3:(l + 1) * 3] = (255, 0, 0)


def cvt_str(point_given):
    """
    This function will convert list of coordinates to 3 digits of leading zero and then to string
    :param point_given: Given list of points
    :return: string
    """
    string = ''
    point_cpy = point_given[:]
    point_cpy[0] = "{0:0=3d}".format(int(point_cpy[0]))
    point_cpy[1] = "{0:0=3d}".format(int(point_cpy[1]))
    string = string + str(point_cpy[0]) + str(point_cpy[1])
    return string


# Functions for each obstacle
def in_ellipse_obst(y, x):
    y = 300 - y
    if (((x - 246) ** 2) / (60 * 60) + ((y - 145) ** 2) / (30 * 30)) <= 1:
        return True
    else:
        return False


def in_rectangle_obst(y, x):
    y = 300 - y
    if (y - 0.7 * x - 74.4 >= 0) and (y - 0.7 * x - 90.8 <= 0) and (y + 1.43 * x - 176.64 >= 0) and \
            (y + 1.43 * x - 438.64 <= 0):
        return True
    else:
        return False


def in_circle_obst(y, x):
    y = 300 - y
    if (x - 90) ** 2 + (y - 70) ** 2 <= (35*35):
        return True
    else:
        return False


def in_c_obst(y, x):
    if (200 <= x <= 210 and 20 <= y <= 70) or (210 <= x <= 230 and 60 <= y <= 70) or \
            (210 <= x <= 230 and 20 <= y <= 30):

        return True
    else:
        return False


# Function for each obstacle for coloring visited nodes
def in_ellipse_obst_(y, x):
    y = 300 - y
    rx = 60 + increase
    ry = 30 + increase
    if (((x - 246) ** 2) / (rx * rx) + ((y - 145) ** 2) / (ry * ry)) < 1:
        return True
    else:
        return False


def in_rectangle_obst_(y, x):
    y = 300 - y
    if (y - 0.7 * x - 74.4 + increase * 1.22) >= 0 and (y - 0.7 * x - 90.8 - (increase*1.22) <= 0) and (y + 1.43 * x - 176.64 + (increase * 1.744) >= 0) and \
            (y + 1.43 * x - 438.64 - (increase * 1.744) <= 0):
        return True
    else:
        return False


def in_circle_obst_(y, x):
    y = 300 - y
    rx = 35 + increase
    if (x - 90) ** 2 + (y - 70) ** 2 < (rx * rx):
        return True
    else:
        return False


def in_c_obst_(y, x):
    if (200 - increase <= x <= 210 + increase and 20 - increase <= y <= 70 + increase) or \
            (210 - increase <= x <= 230 + increase and 60 - increase <= y <= 70 + increase) or \
            (210 - increase <= x <= 230 + increase and 20 - increase <= y <= 30 + increase):
        return True
    else:
        return False


def in_peri_obst_t_(y, x):
    y = 300 - y
    if 0 < x < increase:
        return True
    else:
        return False


def in_peri_obst_b_(y, x):
    y = 300 - y
    if 400 - increase < x < 401:
        return True
    else:
        return False


def in_peri_obst_l_(y, x):
    y = 300 - y
    if 0 < y < increase:
        return True
    else:
        return False


def in_peri_obst_r_(y, x):
    y = 300 - y
    if 300 - increase < y < 301:
        return True
    else:
        return False


def check_validity(pointer):
    """
    # This function will check if the function is valid or not
    :param pointer:
    :return: Boolean value
    """
    if in_ellipse_obst_(pointer[0], pointer[1]) or in_circle_obst_(pointer[0], pointer[1]) or in_rectangle_obst_(
            pointer[0], pointer[1]) or in_c_obst_(pointer[0], pointer[1]) or in_peri_obst_b_(pointer[0], pointer[
            1]) or in_peri_obst_t_(pointer[0], pointer[1]) or in_peri_obst_r_(pointer[0], pointer[1]) or \
            in_peri_obst_l_(pointer[0], pointer[1]):

        return False
    else:
        return True


def possible_moves(current_position):
    """
    Generate all possible nodes for given point
    :param current_position: The point as a list
    :return: List of possible moves and cost as tuple
    """
    x = current_position[1][0]
    y = current_position[1][1]

    # All points
    if x != 0 and y != 0 and x != x_max and y != y_max:
        legal_actions = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), (1, 1, 1.41), (-1, 1, 1.41),
                         (1, -1, 1.41), (-1, -1, 1.41)]

    # Top side
    if x == 0 and (y != 0 or y != y_max):
        legal_actions = [(0, -1, 1), (1, -1, 1.41), (1, 0, 1), (1, 1, 1.41), (0, 1, 1)]

    # Left side
    if y == 0 and (x != 0 or x != x_max):
        legal_actions = [(-1, 0, 1), (-1, 1, 1.41), (0, 1, 1), (1, 0, 1), (1, 1, 1.41)]

    # Bottom side
    if x == x_max and (y != 0 or y != y_max):
        legal_actions = [(0, -1, 1), (-1, -1, 1.41), (-1, 0, 1), (-1, 1, 1.41), (0, 1, 1)]

    # Right side
    if y == y_max and (x != 0 or x != x_max):
        legal_actions = [(1, 0, 1), (-1, 0, 1), (0, -1, 1), (-1, -1, 1.41), (1, -1, 1.41)]

    # Top right corner
    if x == 0 and y == 0:
        legal_actions = [(1, 0, 1), (1, 1, 1.41), (0, 1, 1)]

    # Bottom right corner
    if x == x_max and y == y_max:
        legal_actions = [(0, -1, 1), (-1, -1, 1.41), (-1, 0, 1)]

    # Top left corner
    if x == 0 and y == y_max:
        legal_actions = [(0, -1, 1), (1, -1, 1.41), (1, 0, 1)]

    # Bottom left corner
    if x == x_max and y == 0:
        legal_actions = [(-1, 0, 1), (-1, 1, 1.41), (0, 1, 1)]

    return legal_actions


def move_point(current_pos, legal_move_given):
    """
    Function to apply a possible move
    :param current_pos: Current coordinates of the point as a list
    :param legal_move_given: Legal move with cost as a tuple
    :return: New position coordinates
    """
    p = legal_move_given[0]
    q = legal_move_given[1]
    r = legal_move_given[2]
    current_pos_op = [0, [0, 0], 0, 0]
    current_pos_op[0] = current_pos[0] + r      # cost
    current_pos_op[1][0] = current_pos[1][0] + p      # X
    current_pos_op[1][1] = current_pos[1][1] + q      # Y
    current_pos_op[2] = current_pos[2]
    return current_pos_op


# Taking user input and commenting if its valid or not
flag = True
global increase
while flag:
    print('Enter the initial position...')
    xi = int(input("Enter your value of X-Axis: "))
    yi = int(input("Enter your value of Y-Axis: "))
    print('Enter the goal position...')
    xg = int(input("Enter your value of X-Axis: "))
    yg = int(input("Enter your value of Y-Axis: "))
    print("Enter the dimension of the robot...")
    dim = int(input("Enter the radius of robot:"))
    print("Enter the clearance of robot...")
    clearance = int(input("Enter the clearance:"))
    increase = dim + clearance
    init = [yi, xi]
    goal = [yg, xg]
    if check_validity(init) and check_validity(goal):
        flag = False
    else:
        print("Either point is in obstacle space")

# Initiate the variables
plot_point(init[0], init[1])
plot_point(goal[0], goal[1])
init_str = cvt_str(init)
goal_str = cvt_str(goal)
parent = [0, 0]
left_to_check = []
closed_node = set()
closed_node.add(init_str)
parent_index = 0
index = 0
start_node = [0, init, [0, 0]]
goal_node = [0, goal, [0, 0]]
visited = {}
visited[init_str] = [0, 0, start_node]
tree_list = [[parent_index, init]]
not_solved = True

# Creating obstacle on image
for i in range(300):
    for j in range(400):
        if in_ellipse_obst(i, j):
            blank_image[i * 3:(i + 1) * 3, j * 3:(j + 1) * 3] = (0, 0, 0)
        if in_circle_obst(i, j):
            blank_image[i * 3:(i + 1) * 3, j * 3:(j + 1) * 3] = (0, 0, 0)
        if in_rectangle_obst(i, j):
            blank_image[i * 3:(i + 1) * 3, j * 3:(j + 1) * 3] = (0, 0, 0)
        if in_c_obst(i, j):
            blank_image[i * 3:(i + 1) * 3, j * 3:(j + 1) * 3] = (0, 0, 0)

# Generate first layer manually
legal_moves = possible_moves(start_node)

# Iterating through each possible move while considering cost
for i in range(len(legal_moves)):
    possible_node = move_point(start_node, legal_moves[i])
    possible_node[2] = init
    possible_node_string = cvt_str(possible_node[1])
    if check_validity(possible_node[1]):
        if possible_node_string in closed_node:
            continue
        else:
            index = index + 1
            visited[possible_node_string] = [possible_node[0], index, possible_node]
            tree_list.append([parent_index, possible_node[1]])
            heapq.heappush(left_to_check, possible_node)
            blank_image[possible_node[1][0] * 3:(int(possible_node[1][0]) + 1) * 3, possible_node[1][1] * 3:(possible_node[1][1] + 1) * 3] = (0, 0, 255)

# Adding the initial node in the closed node set
closed_node.add(init_str)

# Initializing variable for displaying the image frame at certain intervals
op = 0
path_not_found = False

# Creating a loop til we reach node
while not_solved:
    if len(left_to_check) == 0:
        print("The path can not be found as point is outside search area.")
        path_not_found = True
        break
    current_node = heapq.heappop(left_to_check)
    parent_index = parent_index + 1
    legal_moves = possible_moves(current_node)
    for i in range(len(legal_moves)):
        possible_node = move_point(current_node, legal_moves[i])
        possible_node[2] = current_node[1]
        possible_node_string = cvt_str(possible_node[1])
        if check_validity(possible_node[1]):
            if str(possible_node_string) in closed_node:
                continue
            elif str(possible_node_string) in visited:
                cost_index = visited[possible_node_string]
                if cost_index[0] > possible_node[0]:
                    tree_list[cost_index[1]] = [parent_index, possible_node[1]]
                    visited[possible_node_string] = [possible_node[0], cost_index[1], possible_node]
                    continue
                else:
                    continue
            else:
                index = index + 1
                possible_node[3] = index
                closed_node.add(possible_node_string)
                tree_list.append([possible_node[2], possible_node[1]])
                visited[possible_node_string] = [possible_node[0], index, possible_node]
                heapq.heappush(left_to_check, possible_node)
                blank_image[possible_node[1][0] * 3:(int(possible_node[1][0]) + 1) * 3, possible_node[1][1] * 3:(possible_node[1][1] + 1) * 3] = (0, 0, 255)
                if possible_node_string == goal_str:
                    not_solved = False
                    break
    # result.write(blank_image)
    op = op + 1
    if op % 500 == 0:
        cv2.imshow("bk", blank_image)
        # break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
if not path_not_found:
    path = []
    x = visited[goal_str]
    y = x[2][2]
    path.append(y)
    while y != [0, 0]:
        x = visited[cvt_str(y)]
        y = x[2][2]
        path.append(y)

    for i in range(len(path)):
        plot_point(path[i][0], path[i][1])
        # ret, frame = cap.read() #returns ret and the frame

    while True:
        cv2.imshow("bk", blank_image)
        # result.write(blank_image)
        # break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break