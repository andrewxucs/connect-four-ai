from ConnectFour import ConnectFour
import math
import sys
import pygame

# ng stands for new game
ng = ConnectFour()

board = ng.create_board()
game_over = False
ng.display_board()

# turn = 0 means player 1's turn
# turn = 1 means player 2's turn
turn = 0

while not game_over:

    for event in pygame.event.get():
        
        # If user clicks the exit button, the game ends
        if event.type == pygame.QUIT:
            sys.exit()

        # when the user is dragging the circle to the target column
        elif event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(ng.user_interface, ng.UNOCCUPIED_CIRCLE, (0, 0, ng.WIDTH, ng.SQUARE_RADIUS))
            pos_x_coor = event.pos[0]
            if turn == 0:
                pygame.draw.circle(ng.user_interface, ng.FIRST_PLAYER_CIRCLE, (pos_x_coor, 45), ng.CIRCLE_RADIUS)
            else:
                pygame.draw.circle(ng.user_interface, ng.SECOND_PLAYER_CIRCLE, (pos_x_coor, 45), ng.CIRCLE_RADIUS)
            pygame.display.update()

        # when the user makes a decision and clicks on a column
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(ng.user_interface, ng.UNOCCUPIED_CIRCLE, (0, 0, ng.WIDTH, ng.SQUARE_RADIUS))
            
            # Player 1 Move
            if turn == 0:
                pos_x_coor = event.pos[0]
                column = int(math.floor(pos_x_coor / ng.SQUARE_RADIUS))
                
                if ng.is_column_valid(column):
                    row = ng.get_row(column)
                    ng.add_circle(row, column, 1)
                    
                    if ng.check_win(1):
                        label = ng.game_font.render("Player 1 Victory!", 1, ng.FIRST_PLAYER_CIRCLE)
                        ng.user_interface.blit(label, (40,10))
                        game_over = True

            # Player 2 Move
            else:                
                pos_x_coor = event.pos[0]
                column = int(math.floor(pos_x_coor / ng.SQUARE_RADIUS))
                
                if ng.is_column_valid(column):
                    row = ng.get_row(column)
                    ng.add_circle(row, column, 2)
                    
                    if ng.check_win(2):
                        label = ng.game_font.render("Player 2 Victory!", 1, ng.SECOND_PLAYER_CIRCLE)
                        ng.user_interface.blit(label, (40,10))
                        game_over = True

            # Update user interface and turn
            ng.display_board()
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3500)
