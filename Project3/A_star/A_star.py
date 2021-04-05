# Importing required libraries
import numpy as np
import cv2
import heapq
import math
import time

# Creating a blank image of scale 2X
blank_image = np.zeros((600, 800, 3), np.uint8)

out = cv2.VideoWriter('A_star.avi', cv2.VideoWriter_fourcc(*'DIVX'), 650, (800, 600))


# Assigning all values as gray
blank_image[:, :] = (128, 128, 128)  # (B, G, R)

# Setting max size of the search area
x_max = 300
y_max = 400

# Setting the workspace to 2x model
work_space = np.zeros((600, 800))


def cvt_str(point_given):
    """
    This function will convert list of coordinates to 3 digits of leading zero and then to string
    :param point_given: Given list of points
    :return: string
    """
    string = ''
    point_cpy = [0, 0]
    point_cpy[0] = 10*point_given[0]
    point_cpy[1] = 10*point_given[1]
    point_cpy[0] = "{0:0=4d}".format(int(point_cpy[0]))
    point_cpy[1] = "{0:0=4d}".format(int(point_cpy[1]))
    string = string + str(point_cpy[0]) + str(point_cpy[1])
    return string


def plot_point(r, l):
    """
    This function will convert point to a scaled opencv image
    :param r: X coordinate of point
    :param l: Y coordinate of point
    :return: None
    """
    blank_image[r * 2:(r + 1) * 2, l * 2:(l + 1) * 2] = (255, 0, 0)


def round_to_half(point_given):
    point_temp = [0, 0]
    point_temp[0] = round(point_given[0]*2)/2
    point_temp[1] = round(point_given[1]*2)/2
    return point_temp


def euclieandistance(point_given_1, point_given_2):
    x1 = point_given_1[0]
    y1 = point_given_1[1]
    x2 = point_given_2[0]
    y2 = point_given_2[1]
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)


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


def not_in_workspace(y, x):
    y = 300 - y
    if x < 0 or x > 400 or y < 0 or y > 300:
        return True
    else:
        return False


def threshold(x, y):
    if (x - goal[0]) ** 2 + (y - goal[1]) ** 2 < (step * step):
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
            in_peri_obst_l_(pointer[0], pointer[1]) or not_in_workspace(pointer[0], pointer[1]):
        return False
    else:
        return True


def possible_moves(current_position):
    """
    Generate all possible nodes for given point
    :param current_position: The point as a list
    :return: List of possible moves and cost as tuple
    """
    init_theta = current_position[3]
    var = int(360/theta)
    legal_actions = []
    for i in range(var):
        legal_actions.append([step*math.cos(math.radians(init_theta + (i * theta))), step * math.sin(math.radians(init_theta + (i * theta))), (init_theta + (i * theta)), step])
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
    if r > 360:
        r = r - 360

    current_pos_op = [0, [0, 0], [0, 0], 0, 0]      # Cost, node, parent, theta, ctc
    current_pos_op[1][0] = current_pos[1][0] + p      # X
    current_pos_op[1][1] = current_pos[1][1] + q      # Y
    current_pos_op[2] = current_pos[1]
    current_pos_op[3] = current_pos[3] + r
    current_pos_op[0] = current_pos[4] + int(euclieandistance(current_pos_op[1], goal,))
    current_pos_op[4] = current_pos[4] + step
    return current_pos_op


# Taking user input and commenting if its valid or not
flag = True
while flag:
    print("---"*15)
    print('Enter the initial position...')
    xi = int(input("Enter your value of X-Axis: "))
    yi = int(input("Enter your value of Y-Axis: "))
    zi = int(input("Enter your initial orientation theta: "))
    print("---"*15)
    dim = int(input("Enter the radius of robot:"))
    clearance = int(input("Enter the clearance:"))
    print("---"*15)
    theta = int(input("Enter your step theta: "))
    step = int(input("Enter your step size: "))
    print("---"*15)
    print('Enter the goal position...')
    xg = int(input("Enter your value of X-Axis: "))
    yg = int(input("Enter your value of Y-Axis: "))
    zg = int(input("Enter your goal orientation theta "))
    print("---"*15)
    print("Processing... Please wait...")

    increase = dim + clearance
    if increase == 0 and step > 10:
        print("Step size is too large, decrease the step size or increase clearance")
        continue
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
start_node = [int(euclieandistance(init, goal,)), init, [0, 0], zi, 0]       # Cost, node, parent, theta, cost to come
goal_node = [0, goal, [0, 0], zg, 0]
visited = {}
visited[init_str] = [int(euclieandistance(init, goal,)), 0, start_node, 0]   # Cost, index, parent, cost to come
tree_list = [[parent_index, init]]
not_solved = True


# Creating obstacle on image
for i in range(300):
    for j in range(400):
        if in_ellipse_obst(i, j):
            blank_image[i * 2:(i + 1) * 2, j * 2:(j + 1) * 2] = (0, 0, 0)
        if in_circle_obst(i, j):
            blank_image[i * 2:(i + 1) * 2, j * 2:(j + 1) * 2] = (0, 0, 0)
        if in_rectangle_obst(i, j):
            blank_image[i * 2:(i + 1) * 2, j * 2:(j + 1) * 2] = (0, 0, 0)
        if in_c_obst(i, j):
            blank_image[i * 2:(i + 1) * 2, j * 2:(j + 1) * 2] = (0, 0, 0)
        if threshold(i, j):
            blank_image[i * 2:(i + 1) * 2, j * 2:(j + 1) * 2] = (255, 255, 255)

# Generate first layer manually
legal_moves = possible_moves(start_node)
list_of_all_nodes = []
# Iterating through each possible move while considering cost
for i in range(len(legal_moves)):
    possible_nodes = move_point(start_node, legal_moves[i])
    list_of_all_nodes.append([possible_nodes, i])
heapq.heapify(list_of_all_nodes)
no_of_branch = int(360/(3*theta))
list_of_all_nodes = list_of_all_nodes[:no_of_branch]
possible_moves_to_be = []
for i in range(no_of_branch):
    possible_moves_to_be.append(list_of_all_nodes[i][1])
for i in range(len(possible_moves_to_be)):
    possible_node = move_point(start_node, legal_moves[possible_moves_to_be[i]])
    possible_node_rounded = round_to_half(possible_node[1])
    possible_node_string = cvt_str(possible_node_rounded)
    if check_validity(possible_node[1]):
        if possible_node_string in closed_node:
            continue
        else:
            index = index + 1
            visited[possible_node_string] = [possible_node[0], index, possible_node, possible_node[4]]
            tree_list.append([parent_index, possible_node[1]])
            heapq.heappush(left_to_check, possible_node)
            blank_image[int(possible_node_rounded[0] * 2):(int(possible_node_rounded[0]) + 1) * 2, int(possible_node_rounded[1] * 2):int((possible_node_rounded[1] + 1) * 2)] = (0, 0, 255)

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
    legal_moves = possible_moves(current_node)
    list_of_all_nodes = []
    for i in range(len(legal_moves)):
        possible_nodes = move_point(current_node, legal_moves[i])
        list_of_all_nodes.append([possible_nodes, i])
    heapq.heapify(list_of_all_nodes)
    no_of_branch = int(360 / (4 * theta)) + 1
    list_of_all_nodes = list_of_all_nodes[:no_of_branch]
    possible_moves_to_be = []
    for i in range(no_of_branch):
        possible_moves_to_be.append(list_of_all_nodes[i][1])
    for i in range(len(possible_moves_to_be)):
        possible_node = move_point(current_node, legal_moves[possible_moves_to_be[i]])
        possible_node_rounded = round_to_half(possible_node[1])
        possible_node_string = cvt_str(possible_node_rounded)
        if check_validity(possible_node[1]):
            if str(possible_node_string) in closed_node:
                continue
            elif str(possible_node_string) in visited:
                cost_index = visited[possible_node_string]
                if cost_index[0] > possible_node[0]:
                    tree_list[cost_index[1]] = [parent_index, possible_node[1]]
                    visited[possible_node_string] = [possible_node[0], cost_index[1], possible_node[2], possible_node[4]]
                    continue
                else:
                    continue
            else:
                index = index + 1
                time.sleep(0.01)
                closed_node.add(possible_node_string)
                visited[possible_node_string] = [possible_node[0], index, possible_node]
                heapq.heappush(left_to_check, possible_node)
                blank_image[int(possible_node_rounded[0] * 2):(int(possible_node_rounded[0]) + 1) * 2, int(possible_node_rounded[1] * 2):int((possible_node_rounded[1] + 1) * 2)] = (0, 0, 255)
                blank_image_cache = np.copy(blank_image)
                current_node_rounded = round_to_half(current_node[1])
                image = cv2.arrowedLine(blank_image_cache, (int(2 * current_node_rounded[1]), int(2 * current_node_rounded[0])), (int(2 * possible_node_rounded[1]), int(2 * possible_node_rounded[0])), (255, 0, 255), 1, tipLength=0.5)
                if threshold(possible_node_rounded[0], possible_node_rounded[1]):
                    goal = possible_node[1]
                    possible_node_rounded = round_to_half(possible_node[1])
                    goal_str = cvt_str(possible_node_rounded)
                    not_solved = False
                    break
    # result.write(blank_image)
    op = op + 1
    if op % 500 == 0:
        cv2.imshow("bk", image)
        # break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    out.write(image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
if not path_not_found:
    path = []
    x = visited[goal_str]
    y = x[2][2]
    y = round_to_half(y)
    path.append(y)
    while y != [0, 0]:
        x = visited[cvt_str(y)]
        y = x[2][2]
        y = round_to_half(y)
        path.append(y)

    path.reverse()
    path.append(goal)
    for i in range(len(path)):
        plot_point(int((path[i][0])), int((path[i][1])))
        if i > 1:
            time.sleep(0.2)
            image = cv2.arrowedLine(blank_image, (int(2*path[i-1][1]), int(2*path[i-1][0])), (int(2*path[i][1]), int(2*path[i][0])), (255, 0, 255), 2, tipLength=0.5)
            cv2.imshow("bk", blank_image)
            # result.write(blank_image)
            # break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        # ret, frame = cap.read() #returns ret and the frame

    while True:
        out.write(image)
        cv2.imshow("bk", blank_image)
        # result.write(blank_image)
        # break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

out.release()