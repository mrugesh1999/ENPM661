# Importing required libraries
import numpy as np
import cv2

blank_image = np.zeros((900, 1200, 3), np.uint8)

blank_image[:, :] = (128, 128, 128)  # (B, G, R)

calc_arr = np.zeros((300, 400), dtype='int')
x_max = calc_arr.shape[0]
y_max = calc_arr.shape[1]
# result = cv2.VideoWriter('Tag0.avi',
#                          cv2.VideoWriter_fourcc(*'MJPG'),
#                          10, (blank_image.shape[1], blank_image.shape[0]))


def plot_point(r, l):
    blank_image[r * 3:(r + 1) * 3, l * 3:(l + 1) * 3] = (255, 0, 0)


def cvt_str(point):
    string = ''
    point_cpy = point.copy()
    point_cpy[0] = "{0:0=3d}".format(int(point_cpy[0]))
    point_cpy[1] = "{0:0=3d}".format(int(point_cpy[1]))
    string = string + str(point_cpy[0]) + str(point_cpy[1])
    return string


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
    if (x - 90) ** 2 + (y - 70) ** 2 <= (35 * 35):
        return True
    else:
        return False


def in_c_obst(y, x):
    if (200 <= x <= 210 and 20 <= y <= 70) or (210 <= x <= 230 and 60 <= y <= 70) or \
            (210 <= x <= 230 and 20 <= y <= 30):
        return True
    else:
        return False


def in_blob_obst1(y, x):
    y = 300 - y
    if (y + (42/43)*x - (16485/43) >= 0) and (y - x + 265 >= 0) and (x <= 354) and (y - x + 180 <= 0) and (y + (7/29)*x - (6480/29) <= 0):
        return True
    else:
        return False


def in_blob_obst2(y, x):
    y = 300 - y
    if (y - x + 265 >= 0) and (y - x + 216 <= 0) and (x >= 354) and (x <= 381):
        return True
    else:
        return False


def in_ellipse_obst_(y, x):
    y = 300 - y
    if (((x - 246) ** 2) / (60 * 60) + ((y - 145) ** 2) / (30 * 30)) < 1:
        return True
    else:
        return False


def in_rectangle_obst_(y, x):
    y = 300 - y
    if (y - 0.7 * x - 74.4 > 0) and (y - 0.7 * x - 90.8 < 0) and (y + 1.43 * x - 176.64 > 0) and \
            (y + 1.43 * x - 438.64 < 0):
        return True
    else:
        return False


def in_circle_obst_(y, x):
    y = 300 - y
    if (x - 90) ** 2 + (y - 70) ** 2 < (35 * 35):
        return True
    else:
        return False


def in_c_obst_(y, x):
    if (199 < x < 211 and 19 < y < 71) or (210 < x < 231 and 59 < y < 71) or \
            (210 < x < 231 and 19 < y < 31):
        return True
    else:
        return False


def in_blob_obst_(y, x):
    y = 300 - y
    if (y - x + 265 > 0) and (y + x - 391 > 0) and (y - x + 222.6 < 0) and (x < 381.03) and \
            (y - x + 210 < 0) and (y + 0.3639 * x - 263.33 < 0):
        return True
    else:
        return False


def check_validity(pointer):
    if in_ellipse_obst_(pointer[0], pointer[1]) or in_circle_obst_(pointer[0], pointer[1]) or \
            in_blob_obst_(pointer[0], pointer[1]) or in_rectangle_obst_(pointer[0], pointer[1]) or in_c_obst_(
        pointer[0], pointer[1]):
        return False
    else:
        return True


# def check_validity1(o, p):
#     if in_ellipse_obst(o, p) or in_circle_obst(o, p) and \
#             in_blob_obst(o, p) and in_rectangle_obst(o, p):
#         return True
#     else:
#         return False


def possible_moves(current_position):
    x = current_position[0]
    y = current_position[1]

    # All points
    if x != 0 and y != 0 and x != x_max and y != y_max:
        legal_actions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

    # Top side
    if x == 0 and (y != 0 or y != y_max):
        legal_actions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1)]

    # Left side
    if y == 0 and (x != 0 or x != x_max):
        legal_actions = [(-1, 0), (-1, 1), (0, 1), (1, 0), (1, 1)]

    # Bottom side
    if x == x_max and (y != 0 or y != y_max):
        legal_actions = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    # Right side
    if y == y_max and (x != 0 or x != x_max):
        legal_actions = [(1, 0), (-1, 0), (0, -1), (-1, -1), (1, -1)]

    # Top right corner
    if x == 0 and y == 0:
        legal_actions = [(1, 0), (1, 1), (0, 1)]

    # Bottom right corner
    if x == x_max and y == y_max:
        legal_actions = [(0, -1), (-1, -1), (-1, 0)]

    # Top left corner
    if x == 0 and y == y_max:
        legal_actions = [(0, -1), (1, -1), (1, 0)]

    # Bottom left corner
    if x == x_max and y == 0:
        legal_actions = [(-1, 0), (-1, 1), (0, 1)]

    return legal_actions


def move_point(current_pos, legal_move_given):
    p = legal_move_given[0]
    q = legal_move_given[1]
    current_pos_op = [0, 0]
    current_pos_op[0] = current_pos[0] + p
    current_pos_op[1] = current_pos[1] + q
    return [current_pos_op[0], current_pos_op[1]]


flag = True
while flag:
    print('Enter the initial position...')
    xi = int(input("Enter your value of X-Axis: "))
    yi = int(input("Enter your value of Y-Axis: "))
    print('Enter the goal position...')
    xg = int(input("Enter your value of X-Axis: "))
    yg = int(input("Enter your value of Y-Axis: "))
    init = [yi, xi]
    goal = [yg, xg]
    if check_validity(init) or check_validity(goal):
        flag = False
    else:
        print("Either point is in obstacle space")


plot_point(init[0], init[1])
plot_point(goal[0], goal[1])
goal_str = cvt_str(goal)
visited = set()
visited.add(cvt_str(init))
left_to_check = []
parent_index = 0
index = 0
child = []
tree_list = [[parent_index, init]]
not_solved = True


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
        if in_blob_obst1(i, j):
            blank_image[i * 3:(i + 1) * 3, j * 3:(j + 1) * 3] = (0, 0, 0)
        if in_blob_obst2(i, j):
            blank_image[i * 3:(i + 1) * 3, j * 3:(j + 1) * 3] = (0, 0, 0)

legal_moves = possible_moves(init)
# print(move_point(init, legal_moves[0]))
for i in range(len(legal_moves)):
    possible_node = move_point(init, legal_moves[i])
    possible_node_string = cvt_str(possible_node)
    if check_validity(possible_node):
        if possible_node_string in visited:
            continue
        else:
            visited.add(possible_node_string)
            index = index + 1
            tree_list.append([parent_index, possible_node])
            left_to_check.append(possible_node)
            if not in_ellipse_obst_(possible_node[0], possible_node[1]):
                blank_image[possible_node[0] * 3:(int(possible_node[0]) + 1) * 3,
                possible_node[1] * 3:(possible_node[1] + 1) * 3] = (0, 0, 255)
            if not in_circle_obst_(possible_node[0], possible_node[1]):
                blank_image[possible_node[0] * 3:(int(possible_node[0]) + 1) * 3,
                possible_node[1] * 3:(possible_node[1] + 1) * 3] = (0, 0, 255)
            if not in_rectangle_obst_(possible_node[0], possible_node[1]):
                blank_image[possible_node[0] * 3:(int(possible_node[0]) + 1) * 3,
                possible_node[1] * 3:(possible_node[1] + 1) * 3] = (0, 0, 255)
            if not in_c_obst_(possible_node[0], possible_node[1]):
                blank_image[possible_node[0] * 3:(int(possible_node[0]) + 1) * 3,
                possible_node[1] * 3:(possible_node[1] + 1) * 3] = (0, 0, 255)
            if not in_blob_obst_(possible_node[0], possible_node[1]):
                blank_image[possible_node[0] * 3:(int(possible_node[0]) + 1) * 3,
                possible_node[1] * 3:(possible_node[1] + 1) * 3] = (0, 0, 255)

    possible_node = [0, 0]

while not_solved:
    current_point = left_to_check.pop(0)
    parent_index = parent_index + 1
    legal_moves = possible_moves(current_point)
    for i in range(len(legal_moves)):
        possible_node = move_point(current_point, legal_moves[i])
        possible_node_string = cvt_str(possible_node)
        if check_validity(possible_node):
            if possible_node_string in visited:
                continue
            else:
                visited.add(possible_node_string)
                index = index + 1
                tree_list.append([parent_index, possible_node])
                left_to_check.append(possible_node)
                if not in_ellipse_obst_(possible_node[0], possible_node[1]):
                    blank_image[possible_node[0] * 3:(int(possible_node[0]) + 1) * 3,
                    possible_node[1] * 3:(possible_node[1] + 1) * 3] = (0, 0, 255)
                if not in_circle_obst_(possible_node[0], possible_node[1]):
                    blank_image[possible_node[0] * 3:(int(possible_node[0]) + 1) * 3,
                    possible_node[1] * 3:(possible_node[1] + 1) * 3] = (0, 0, 255)
                if not in_rectangle_obst_(possible_node[0], possible_node[1]):
                    blank_image[possible_node[0] * 3:(int(possible_node[0]) + 1) * 3,
                    possible_node[1] * 3:(possible_node[1] + 1) * 3] = (0, 0, 255)
                if not in_c_obst_(possible_node[0], possible_node[1]):
                    blank_image[possible_node[0] * 3:(int(possible_node[0]) + 1) * 3,
                    possible_node[1] * 3:(possible_node[1] + 1) * 3] = (0, 0, 255)
                if not in_blob_obst_(possible_node[0], possible_node[1]):
                    blank_image[possible_node[0] * 3:(int(possible_node[0]) + 1) * 3,
                    possible_node[1] * 3:(possible_node[1] + 1) * 3] = (0, 0, 255)
                if possible_node_string == goal_str:
                    not_solved = False
                    break
    # result.write(blank_image)
    cv2.imshow("bk", blank_image)
    # break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # ret, frame = cap.read() #returns ret and the frame

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
    # print(list_of_path)
    # print(list_of_path[0])
    # print(list_of_path[0][0])
    for i in range(len(list_of_path)):
        from_x = int(list_of_path[i][0] * 3)
        to_x = int((list_of_path[i][0] + 1) * 3)
        from_y = int(list_of_path[i][1] * 3)
        to_y = int((list_of_path[i][1] + 1) * 3)
        blank_image[from_x:to_x, from_y:to_y] = (0, 255, 0)


while True:
    cv2.imshow("bk", blank_image)
    # result.write(blank_image)
    # break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# result.release()
