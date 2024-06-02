from constants import *

Board = list[list[str]]
Pieces = list[int]
Move = tuple[int, int, int]

# Write your functions here

def num_hours() -> float:
    """Returns the number of hours spent on the assignment."""
    hours=2.5
    return hours


def generate_initial_pieces(num_pieces: int) -> Pieces:
    """Generates a list of initial game pieces."""
    return [i for i in range(1,num_pieces+1)]


def initial_state() -> Board:
    """Creates an initial empty  board."""
    return [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]



def place_piece(board: Board, player: str, pieces_available: Pieces,move: Move ) -> None:
    """Places a game piece on the board and updates available pieces."""
    row=move[0]
    col=move[1]
    piece=move[2]

    board[row][col]=player+str(piece)
    pieces_available.remove(piece)


def print_game(board: Board, naught_pieces: Pieces, cross_pieces: Pieces)-> None:
    """Prints the current game state and available pieces for both players."""


    Naught_pieces=', '.join(map(str,naught_pieces))
    Cross_pieces=', '.join(map(str,cross_pieces))
    print(f'{NAUGHT} has: {Naught_pieces}')
    print(f'{CROSS } has: {Cross_pieces}')
    print()


    boards=""""""
    boards+='   '+'  '.join([str(i) for i in range(1,GRID_SIZE+1)])+'\n'
    boards += '  ' + '---' * GRID_SIZE + "\n"
    for i in range(1,GRID_SIZE+1):
        boards+=str(i)+"|"+'|'.join(['{'+str(i)+'}' for i in range((i-1)*GRID_SIZE,(i-1)*GRID_SIZE+GRID_SIZE)])+"|"+"\n"
        if i==GRID_SIZE:

            boards += '  ' + '---' * GRID_SIZE
        else:
            boards += '  ' + '---' * GRID_SIZE + "\n"



    deel_bordas=[]
    for row in board:
        for c in row:
            deel_bordas.append(c)


    borads=boards.format(*deel_bordas)
    print(borads)





def process_move(move: str) -> Move | None:
    """Processes the user's move input and returns a tuple representing the move."""
    moves=move.split()
    # 检查输入数量是否为3
    if len(moves) != 3:
        print(INVALID_FORMAT_MESSAGE)
        return



    try:
        row = int(moves[0])
    # 检查行列是否超过范围
        if row <= 0 or row > GRID_SIZE:
            print(INVALID_ROW_MESSAGE)
            return


    except:
        print(INVALID_ROW_MESSAGE)
        return

    try:
        col=int(moves[1])
        if col <= 0 or col > GRID_SIZE:
            print(INVALID_COLUMN_MESSAGE)
    except:
        print(INVALID_COLUMN_MESSAGE)
        return

    try:
        size=int(moves[2])
        if size <= 0 or size > PIECES_PER_PLAYER:
            print(INVALID_SIZE_MESSAGE)
    except:
        print(INVALID_SIZE_MESSAGE)
        return


    moves = [int(i) for i in moves]
    moves[0] -= 1
    moves[1] -= 1
    return tuple(moves)



def get_player_move() -> Move:
    """Gets a valid move from the player."""
    while True:
        move = input("Enter your move: ").strip()
        if move.lower() == 'h':
            print(HELP_MESSAGE)
            continue

        result=process_move(move)
        if result:
            return result



def check_move(board: Board, pieces_available: Pieces, move: Move) ->bool:
    """  Check if a move is valid on the board."""
    # move=[int(i) for i in move]
    row=move[0]
    col=move[1]
    size=move[2]
    flage=False
    if size in pieces_available:#填充值是否在pieces里面

        if row>=0 and col>=0:
            origin_size=board[row][col][1:]

            if origin_size!=' ':#检查当前格子是否有数字
                if int(origin_size)<size:
                    flage=True

            else:
                flage=True

        else:
            flage=False
    else:
        flage=False

    return flage

def check_win(board: Board) -> str | None:

    """  Check if a move is valid on the board."""

    #检查行是否有相同
    for row in board:
        row_player=[i[0] for i in row if i]

        if ' ' not in row_player:
            if row_player.count(row_player[0])==GRID_SIZE:

                return row_player[0]

    #检查列是否有相同
    for i in range(GRID_SIZE):
        cow_palyer=[board[j][i][0] for j in range(GRID_SIZE)]
        if ' ' not in cow_palyer:

            if cow_palyer.count(cow_palyer[0])==GRID_SIZE:
                return cow_palyer[0]

    #检查对角是否有相同
    cow_row_player=[board[i][i][0] for i in range(GRID_SIZE)]

    if ' ' not in cow_row_player:
        if cow_row_player.count(cow_row_player[0])==GRID_SIZE:
            return cow_row_player[0]

    #检查反对角是否有相同

    cow_row_player_t=[board[i][GRID_SIZE-i-1][0] for i in range(GRID_SIZE)]
    if ' ' not in cow_row_player_t:

        if cow_row_player_t.count(cow_row_player_t[0]) == GRID_SIZE:
            return cow_row_player_t[0]

    return None


def check_stalemate(board: Board, naught_pieces: Pieces, cross_pieces:Pieces) -> bool:
    """  Check if a move is valid on the board."""

    #如果还有空，返回flase
    for row in board:
        for c in row:
            if c==EMPTY:
                return False

    #r如果剩下pieces存在任一大于board里面的返回flase
    flages=[]
    for row in board:
        for c in row:
            for s in naught_pieces+cross_pieces:
                flages.append(s>int(c[1]))

    if True in flages:
        flage=False
    else:
        flage=True

    return flage



def play(name,board, naught_pieces,cross_pieces)->None:
    while True:
        while True:
            # NAUGHT输入
            print()
            print(f'{name} turn to move')
            print()
            moves = get_player_move()  # 得到位置与输入

            if check_move(board, naught_pieces, moves):  # 检查是否合法，填充，打印，退出循环

                place_piece(board, NAUGHT, naught_pieces, moves)
                print_game(board, naught_pieces, cross_pieces)
                break
            else:
                print(INVALID_MOVE_MESSAGE)
                print()

        result = check_win(board)  # 第一次检查结果，返回结果，退出本轮游戏，返回空，继续
        if result:
            print(f'{result} wins!')
            break

        if check_stalemate(board, naught_pieces, cross_pieces):  # 检查是否相持，无法继续游戏，退出循环
            print('Stalemate!')
            break

def main()->None:
    """main func"""
    while True:#循环游戏
        board = initial_state()#初始化board
        naught_pieces = generate_initial_pieces(PIECES_PER_PLAYER)#初始化pieces
        cross_pieces = generate_initial_pieces(PIECES_PER_PLAYER)
        print_game(board, naught_pieces, cross_pieces)  # 展示
        play(NAUGHT,board,naught_pieces,cross_pieces)
        play(CROSS,board,naught_pieces,cross_pieces)


        options=input('Play again? ')#是否继续游戏
        if options=='n':
            break





if __name__ == '__main__':

    main()
