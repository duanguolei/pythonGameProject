import time
import turtle
import random

screen = turtle.Screen()
screen.title("Sliding Puzzle Game")
t = turtle.Turtle()
turtle.tracer(0, 0)
t.speed(0)


turtle.bgcolor("white")

#事先定义一下

board = []

#每个格子的尺寸
tile_size = 80
# 定义颜色
color = "green"

suncess_color='red'

# 定义华容道游戏板

#胜利版


def generate_board():

    global suncess_board
    global board
    suncess_board=[]
    number=1
    for _ in range(puzzle_size):
        new_row=[]
        for _ in range(puzzle_size):
            new_row.append(number)
            number+=1

        suncess_board.append(new_row)

    suncess_board[-1][-1]=None


    data_list = [i for row in suncess_board for i in row]
    random.shuffle(data_list)
    board = [data_list[i:i + puzzle_size] for i in range(0, len(data_list), puzzle_size)]


def draw_board():
    t.penup()
    t.goto(-board_size // (puzzle_size-1)-puzzle_size*15, board_size // (puzzle_size-1)+puzzle_size*15)
    t.pendown()
    for _ in range(4):
        t.forward(board_size)
        t.right(90)


def draw_tile(row, col, num,color):
    t.penup()
    x = -board_size // (puzzle_size-1) + col * tile_size-puzzle_size*15
    y = board_size // (puzzle_size-1) - row * tile_size+puzzle_size*15
    t.goto(x, y)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(tile_size)
        t.right(90)
    t.end_fill()
    t.penup()
    t.goto(x + tile_size // (puzzle_size-1)+puzzle_size*5, y - tile_size // (puzzle_size-1)-puzzle_size*5)
    t.write(num, align="center", font=("Arial", 20, "normal"))





# 初始化游戏板
def init_board(color):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is not None:
                draw_tile(i, j, board[i][j],color)


# 移动拼图块
def move_piece(row, col):
    if row < (puzzle_size-1) and board[row + 1][col] is None:
        board[row][col], board[row + 1][col] = board[row + 1][col], board[row][col]
    elif row > 0 and board[row - 1][col] is None:
        board[row][col], board[row - 1][col] = board[row - 1][col], board[row][col]
    elif col < (puzzle_size-1) and board[row][col + 1] is None:
        board[row][col], board[row][col + 1] = board[row][col + 1], board[row][col]
    elif col > 0 and board[row][col - 1] is None:
        board[row][col], board[row][col - 1] = board[row][col - 1], board[row][col]
    # Set the original position to None after moving
    board[row][col] = None


# 寻找空格位置
def find_blank_position():
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                return i, j

#判断是否可移动
def judge_move(row,col):
    flage=False
    cols=[row[col] for row in board]
    rows=board[row]
    if None in rows:
        if abs(rows.index(None)-col)==1:
            flage=True
    elif None in cols:
        if abs(cols.index(None) - row) == 1:
            flage=True

    if 0 <= row < puzzle_size and 0 <= col < puzzle_size:
        if board[row][col] is not None and flage:
            return True

    return False





def judge_sunceess(board):
    if board==suncess_board:
        return True
    else:
        return False





# 鼠标拖动事件处理函数
def drag_handler(x, y):
    col = int((x + board_size-puzzle_size*15 // (puzzle_size-1)) // tile_size)
    row = int((-y + board_size+puzzle_size*15 // (puzzle_size-1)) // tile_size)
    col=col-puzzle_size+2
    row=row-puzzle_size+2

    if judge_move(row,col):
        move_piece(row, col)
        none_row, none_col = find_blank_position()
        number = board[row][col]
        board[none_row][none_col] = number
        t.clear()
        draw_board()
        if judge_sunceess(board):
            init_board(color=suncess_color)
        else:
            init_board(color=color)

        turtle.update()




def start_game():
    global puzzle_size
    global board_size
    puzzle_size = screen.numinput("Puzzle Size", "Enter the size of the puzzle (3, 4, or 5):", minval=3, maxval=5)
    puzzle_size=int(puzzle_size)
    turtle.setup(width=600, height=600)
    board_size=puzzle_size*tile_size
    turtle.onscreenclick(drag_handler, )
    generate_board()
    draw_board()
    init_board(color=color)
    turtle.done()

if __name__ == '__main__':

    start_game()
    screen.mainloop()

