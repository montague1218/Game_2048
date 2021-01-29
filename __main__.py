import random

instruction = '''
The game is called '2048'.
In the game, you are provided a 4x4 matrix, which is mostly filled with zeros.
Otherwise, it is either 2 or 4.

During the game, you can 'push' any numbers appearing in the matrix (except 0) vertically or horizontally, namely 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048.
Visually, you can treat the matrix as a 4x4 grid, zeros as empty sapce, and non-zero powers of 2 as movable blocks.

In each push, if two numbers are of the same magnitude, they will merge into one single number with the double of the original magnitude of the combining numbers along the direction of the push (e.g. 4 and 4 give 8)

Your task is to combine as many numbers as possible until you get '2048'.
You win the game if you get '2048'.
Otherwise, if you cannot move any number and combine any two of them, you lose.

Start with combining 2 and 2, which gives 4. Then 4 and 4, 8 and 8, 16 and 16, etc..
Input direction w, a, s, d representing up, left, down, right. (Check your keyboard)
'''

direction_choice = {'w', 'a', 's', 'd'}
generator = [2, 4]
height, width = 4, 4

case1 = [[2,16,4,8],[4,8,16,32],[2,4,32,16],[4,2,16,32]]
case2 = [[4,0,0,0],[2,0,0,0],[4,0,0,0],[4,2,0,0]]


def generate(matrix, size):
    empty = zeros_in_matrix(matrix)
    if len(empty) == 0:
        return matrix
    count = size
    numbers = random.choices(generator, k=size)

    while count > 0:
        i, j = random.choice(empty)
        matrix[i][j] = numbers.pop()
        empty.remove((i, j))
        count -= 1
    return matrix

def check_win(matrix):
    win = False
    for column in matrix:
        if 2048 in column:
            win = True

    return win
            
def movability(matrix):
    movable = set()
    for i in range(width - 1):
        for j in range(height):
            n1, n2 = matrix[i][j], matrix[i + 1][j]
            if n1 == n2 and n1 != 0:
                movable.add('a')
                movable.add('d')
            if n1 != n2:
                if n1 == 0 and n2 != 0:
                    movable.add('a')
                if n1 != 0 and n2 == 0:
                    movable.add('d')
                
    for j in range(height - 1):
        for i in range(width):
            n1, n2 = matrix[i][j], matrix[i][j + 1]
            if n1 == n2 and n1 != 0:
                movable.add('w')
                movable.add('s')
            if n1 != n2:
                if n1 == 0 and n2 != 0:
                    movable.add('w')
                if n1 != 0 and n2 == 0:
                    movable.add('s')
    return movable

def zeros_in_matrix(matrix):
    return [(i, j) for i in range(height) for j in range(width) if matrix[i][j] == 0]

def empty_matrix():
    return [[0 for j in range(height)] for i in range(width)]

def merge_column_up(column):
    size = height
    if size > 0:
        non_zeros = [e for e in column if e != 0]
        nz_count = len(non_zeros)
        if nz_count == 0:
            pass
        elif nz_count == 1:
            column = [0 for i in range(size)]
            column[0] = non_zeros.pop(0)
        else: 
            current = non_zeros.pop(0)
            new_column = []
            while len(non_zeros) > 0:
                if current == -1:
                    current = non_zeros.pop(0)
                else:
                    successor = non_zeros.pop(0)
                    if current == successor:
                        new_column.append(current + successor)
                        current = -1
                    else:
                        new_column.append(current)
                        current = successor
            new_column.append(current)
                
            nc_count = len(new_column)
            for i in range(size):
                if i < nc_count and new_column[i] > 0:
                    column[i] = new_column[i]
                else:
                    column[i] = 0
    return column

def move(matrix, direction):
    if direction == 'w':
        for j in range(width):
            matrix[j] = merge_column_up(matrix[j])
    elif direction == 's':
        for j in range(width):
            column = matrix[j]
            invert = column[::-1]
            invert = merge_column_up(invert)
            matrix[j] = invert[::-1]
    elif direction == 'a':
        matrix = transpose_matrix(matrix)
        for j in range(width):
            matrix[j] = merge_column_up(matrix[j])
        matrix = transpose_matrix(matrix)
    elif direction == 'd':
        matrix = transpose_matrix(matrix)
        for j in range(width):
            column = matrix[j]
            invert = column[::-1]
            invert = merge_column_up(invert)
            matrix[j] = invert[::-1]
        matrix = transpose_matrix(matrix)
    else:
        print('No such direction as %s!' % direction)
    return matrix

def transpose_matrix(matrix):
    m1 = empty_matrix()
    for i in range(width):
        for j in range(height):
            m1[i][j] = matrix[j][i]
    return m1

def print_matrix(matrix):
    print('********************')
    for j in range(height):
        row = ' '.join([str(matrix[i][j]).rjust(3, ' ') for i in range(width)])
        print(row)
    print('********************')

def main():
    m = empty_matrix()
    m = generate(m, 4)
    turn = 1
    print_matrix(m)
    
    while True:
        movable = movability(m)
        
        if check_win(m):
            print('Congratulations, you have won the game in %s turns!' % turn)
            break
        if len(movable) == 0:
            print('You have lost the game......')
            break
        
        print(movable)
        while True:
            direction = input('Input your direction: ')
            if direction in movable:
                break
            else:
                print('You cannot move by %s.' % direction)
                print('Choose one from ', movable)
        print('')
        
        m = move(m, direction)
        m = generate(m, 1)
        
        
            
        print_matrix(m)
        turn += 1

#print(movability(case2))
print(instruction)
main()
