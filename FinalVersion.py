# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 17:42:56 2022
"""
import sys
import random

def create_board():
    row_str = input("Number of rows: ")
    if row_str=='exit': #type 'exit' at any user input to exit program
        sys.exit()
    set_row = [str(x) for x in range(2,8)] #set for number of rows allowed
    while row_str not in set_row:
        row_str = input('Please enter a number between 2 and 7: ')
        if row_str=='exit':
            sys.exit()
    row = int(row_str)
    board = [0 for n in range((row)*7)]  #generate board(1D-list)
    return board

def display_board(board):
    board_temp = []
    for r in range(int(len(board)/7)):
        for x in range(7):
            board_temp.append(board[7*(int(len(board)/7)-r-1)+x])  #to change the order of print from bottom to top row
    counter = 0
    for x in board_temp: #to print board out
        if counter<6: #
            print(x,end=' ')
            counter+=1
        else:
            print(x) #prints final element of row and goes to next line
            counter=0
            continue
    print()

def apply_move(board,turn,col,pop):
    board_temp = board.copy() #to not change the board until check_move is true
    if pop==False:
        for r in range(int(len(board)/7)):
            if board_temp[7*r+col] == 0: #to only fill the first empty(0) slot of the column
                board_temp[7*r+col] = turn
                break
    elif pop==True:
        for r in range(int(len(board)/7-1)):
            board_temp[7*r+col]=board_temp[7*(r+1)+col] #move every element a row down
        board_temp[int(7*(len(board)/7-1)+col)] = 0  #ensure top row is replaced by 0
    return board_temp

def check_move(board,turn,col,pop):
    if pop==True:
        if board[col]==0: #if the first element is 0, pop is not allowed
            print ('There is nothing to pop.')
            return False
        if board[col]!=turn: #turn is defined such that player 1 takes odd turns
            print("You cannot pop another person's disc!")
            return False
        else: return True
        
    elif pop==False: #if the top column isn't empty(0), invalid move
        if board[7*(int(len(board)/7)-1)+col]!=0:
            print("Column is already full of discs...")
            return False
        else: return True

def check_com_move(board,turn,col,pop): #same as check_move, but for com so no error msg is printed
    if pop==True:
        if board[col]==0:
            return False
        if board[col]!=turn:
            return False
        else: return True
        
    elif pop==False:
        if board[7*(int(len(board)/7)-1)+col]!=0:
            return False
        else: return True

def computer_move(board,turn,level): #assign to separate computer levels
    if level==1:
        return com_random(board,turn)
    elif level==2:
        return com_intermediate(board,turn)

def com_random(board,turn):
    col = random.randint(0,6)
    pop_choices = [True,False]
    pop = random.choice(pop_choices)
    while check_com_move(board,turn,col,pop)==False: #if the move is invalid
            col = random.randint(0,6)
            pop = random.choice(pop_choices)
    return col,pop #returns the col and pop

def com_intermediate(board,turn):
    if check_previctory(board,turn) != (None,None):
        return check_previctory(board,turn)
    elif check_avoid_victory(board, turn) != (None,None):
        return check_avoid_victory(board, turn)
    else:
        return com_random(board,turn)
       
def check_previctory(board,turn): #to check whether there is a move that can lead to victory, if yes, return that col and pop
    board_temp = board.copy()
    for c in range(7):
        for pop_value in [False,True]:
            if check_victory(apply_move(board_temp,turn,c,pop_value),turn) == turn and \
                check_com_move(board_temp,turn,c,pop_value) == True:
                win_col = c
                win_pop = pop_value
                return (win_col,win_pop)
            else: continue
        else: continue
    else:
        return (None,None)
            
def check_avoid_victory(board,turn): #to avoid opposition victory, first check if opposition can win in next move
    if turn == 1:
        opp_turn = 2
    elif turn == 2:
        opp_turn = 1
        
    if check_previctory(board, opp_turn) != (None,None): #if opposition can win in next move, block that move (will only do pop=False)
        for col in range(7):      #in the case of us already blocking opposition, we wan to avoid accidentally pop that blocked disc (eg: 1,1,1,2,then u have 1 on top of 2)
            if check_victory(apply_move(board, turn, col, True),opp_turn)==True: #check victory for player after computer apply a move)
                c = random.randint(0,6) 
                if c == col and check_com_move(board,turn,c,False)==True: #we want to avoid (col, True), where col is the position of blocked disc
                    return (c,False)
                else:
                    pop_choices = [True,False]
                    pop = random.choice(pop_choices)
                    if c == col and check_com_move(board,turn,c,pop)==True:
                        return (c,pop)
                    else: continue
            else: continue
        else: pass
                                      
    column_list=[0,1,2,3,4,5,6] #next, randomize a move and check if this create a winning situation for opposition, if no then return
    random.shuffle(column_list) #shuffle to ensure that computer take a different value every time it runs here
    for c in column_list:    
        pop_choices = [True,False]
        pop = random.choice(pop_choices)        
        board_temp = apply_move(board, turn, c, pop).copy()
        if check_previctory(board_temp,opp_turn) == (None, None): #if applying this move won't create a winning opportunity for player, return this move
            safe_column = c
            safe_pop = pop
            if check_com_move(board, turn, safe_column, safe_pop)==True:
                return (safe_column,safe_pop)
            else: continue
        else:
            continue 
    else:
        return (None,None)   

def column(): #player input
    col = input('Enter the column to drop/pop disc: ')
    if col=='exit':
        sys.exit() #exit game anytime
    while col not in ('1','2','3','4','5','6','7'):
            col = input('Please enter an integer value between 1-7: ')
            if col=='exit':
                sys.exit()
    return int(col)-1 #as we want the user to input between col 1 to col 7

def pop_choice(): #player input whether to pop or not
    chc = input('Do you want to pop (y/n): ')
    if chc=='exit':
        sys.exit()
    if chc=='y':
        pop=True
    elif chc=='n':
       pop=False
    else:
        while chc!='y' or chc!='n':
            chc = input('Please only enter y or n: ')
            if chc=='y':
                pop=True
                break
            elif chc=='n': 
                pop=False
                break
    return pop

def pop_check(board,turn): #to disable pop ability for the first 2 turns
    if 1 in board and turn==1: 
        pop = pop_choice()
    elif 2 in board and turn==2:
        pop = pop_choice()
    else: pop = False
    return pop

def turn_number(counter): #player 1 gets odd turns, player 2 gets even turns
    if counter%2==0:
        return 2
    else: return 1

def check_victory(board,who_played):
    victory1 = 0 
    victory2 = 0
   
    for r in range(7): #vertical_victory
        for row in range(int(len(board)/7)-3):
            for x in range(1,3):
                b = board[7*row+r]==board[7*row+r+7]==board[7*row+r+14]==board[7*row+r+21]==x
                if x==1 and b==True:
                    victory1+=1
                elif x==2 and b==True:
                    victory2+=1
                else: pass
    
    for row in range(int(len(board)/7)): #horizontal_victory
        for r in range(4):
            for x in range(1,3):
                i = 7*row+r
                b = board[i]==board[i+1]==board[i+2]==board[i+3]==x
                if x==1 and b==True:
                    victory1+=1
                elif x==2 and b==True:
                    victory2+=1
                else: pass

    for r in range(4): #diagonal_pos_grad_victory
        for row in range(int(len(board)/7)-3):
            for x in range(1,3):
                b = board[7*row+r]==board[7*row+r+8]==board[7*row+r+16]==board[7*row+r+24]==x
                if x==1 and b==True:
                    victory1+=1
                elif x==2 and b==True:
                    victory2+=1
                else: pass
     
    for r in range(4): #diagonal_neg_grad_victory
        for row in range(int(len(board)/7)-1,2,-1):
            for x in range(1,3):
                b = board[row*7+r]==board[row*7+r-6]==board[row*7+r-12]==board[row*7+r-18]==x
                if x==1 and b==True:
                    victory1+=1
                elif x==2 and b==True:
                    victory2+=1
                else: pass
            
    if victory1>=1 and victory2==0:
        return 1
    elif victory2>=1 and victory1==0:
        return 2
    elif victory1>=1 and victory2>=1:
        if who_played==1:
            return 2
        else:
            return 1
    else:
        return 0

def winner(win,board,turn,col,pop):
    if win>0: #if there is a win condition
        if win==1:
            print ('Player 1 wins!')
            display_board(board)
            once_again()
        elif win==2:
            print ('Player 2 wins!')
            display_board(board)
            once_again()
    else: pass

def once_again(): #mou yikkai == to play the game again
    ans = input('Play again?\n[y]es [n]o\n')
    while ans not in ('n','y','N','Y'):
        ans = input('Please enter only small or capital Y or N: ')
    if ans=='y' or ans=='Y':
        print()
        menu()
    else: sys.exit()

def vs_human():
    board = create_board()
    display_board(board)
    turn_counter = 0
    while True: #to keep game running
        pop = False
        turn_counter+=1
        turn = who_played = turn_number(turn_counter)
        print ('Turn',turn_counter)
        col = column()
        pop = pop_check(board,turn)
        while check_move(board,turn,col,pop)==False: #if move is invalid, will continue to ask for input
            display_board(board)
            col = column()
            pop = pop_check(board,turn)
            continue
        else: pass
        board = apply_move(board,turn,col,pop)
        win_chk = check_victory(board, who_played)
        winner(win_chk,board,turn,col,pop)
        display_board(board)

def vs_computer():
    difficulty = input('Select computer difficulty: (E)asy (M)edium\n')
    if difficulty == 'E' or difficulty=='e':
        level = 1
    elif difficulty== 'M' or difficulty=='m': level = 2
    player = input('Which player will you be (1/2)?\n')
    while player not in ('1','2'):
        player = input('Enter only 1 or 2.\n')
    board = create_board()
    display_board(board)
    
    turn_counter = 0 #if player goes second
    if player == '2':
        turn_counter+=1
        print('Turn',turn_counter)
        turn = turn_number(turn_counter)
        cm = com_random(board, turn) #cm==computer move
        board = apply_move(board, turn, cm[0], cm[1])
        print('Computer apply move',(cm[0]+1,cm[1]))
        display_board(board)
    elif player == '1':
        pass
    
    while True:
        pop = False #player's turn
        turn_counter+=1
        turn = who_played = turn_number(turn_counter)
        print ('Turn',turn_counter)
        col = column()
        pop = pop_check(board,turn)
        while check_move(board,turn,col,pop)==False:
            display_board(board)
            col = column()
            pop = pop_check(board,turn)
            continue
        else: pass
        board = apply_move(board,turn,col,pop)
        win_chk = check_victory(board, who_played)
        winner(win_chk,board,turn,col,pop)
        display_board(board)
    
        turn_counter+=1 #computer's turn
        turn = who_played = turn_number(turn_counter)
        print ('Turn',turn_counter)
        cm = computer_move(board, turn, level)
        print("Computer apply move",(cm[0]+1,cm[1]))
        board = apply_move(board, turn, cm[0], cm[1])
        win_chk = check_victory(board, who_played)
        winner(win_chk, board, turn, cm[0], cm[1])
        display_board(board)

def menu(): #'exit' at any point of the game using user input
    print("Welcome to Connect-4.\nType 'exit' at any user input to exit game.")
    print()
    opponent = input('[vs (H)uman] [vs (C)omputer]\nPlease select your opponent (H/C): ')
    while opponent not in ['H','C','h','c','exit']:
        opponent=input('Please only enter H/h or C/c: ')
    if opponent=='H' or opponent=='h':
        vs_human() #function for human opponent
    elif opponent=='C' or opponent=='c':
        vs_computer() #function for computer opponent
    elif opponent=='exit':
        sys.exit()

if __name__ == "__main__":
    menu()
