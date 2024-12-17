import random  # Pour choisir une case pour l'IA
import threading 
import time  # (timer)
import os  # Pour nettoyer la console

# Fonction pour nettoyer la console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fonction pour afficher le terrain de jeu
def display_board(board):
    clear_console()
    for i in range(0, 9, 3):
        print(f"| {board[i]} | {board[i+1]} | {board[i+2]} |")
        if i < 6:
            print("----+---+----")


# Fonction pour gérer le tour d'un joueur avec un timer
def play_turn(board, player, is_ai):
    if is_ai:
        choice = ia(board, player)
        if choice is not False:
            board[choice] = player
    else:
        valid_choice = False
        choice = None
        timer_expired = [False]

# Fonction pour gérer le compte à rebours (timer)
        def timer():
            time.sleep(15)
            if not valid_choice:
                timer_expired[0] = True
                print("\nTemps écoulé ! Une case sera choisie automatiquement.")

        timer_thread = threading.Thread(target=timer)
        timer_thread.start()
# Boucle permettant au joueur de choisir une case
        while not valid_choice and not timer_expired[0]:
            try:
                choice = int(input(f"Joueur {player}, choisissez une case (1-9) : ")) - 1
                if 0 <= choice <= 8 and board[choice] == " ":
                    board[choice] = player
                    valid_choice = True
                else:
                    print("Choix invalide. Réessayez.")
            except ValueError:
                print("Entrez un numéro valide (1-9).")
# Choix automatique si le temps est écoulé
        if timer_expired[0]:
            free_spaces = [i for i in range(9) if board[i] == " "]
            if free_spaces:
                choice = random.choice(free_spaces)
                board[choice] = player
                print(f"Le coup du joueur {player} a été choisi automatiquement : case {choice + 1}")


# Fonction pour vérifier si un joueur a gagné
def check_victory(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    return any(all(board[i] == player for i in combo) for combo in winning_combinations)


# Fonction de l'IA pour choisir une case
def ia(board, signe):
    opponent = "O" if signe == "X" else "X"
# 1. Vérifie si l'IA peut gagner en un seul coup
    for i in range(9):
        if board[i] == " ":
            board[i] = signe
            if check_victory(board, signe):
                board[i] = " "
                return i
            board[i] = " "
# 2. Bloque l'adversaire s'il est sur le point de gagner
    for i in range(9):
        if board[i] == " ":
            board[i] = opponent
            if check_victory(board, opponent):
                board[i] = " "
                return i
            board[i] = " "

    free_spaces = [i for i in range(9) if board[i] == " "]# 3. Choisit une case libre au hasard
    if free_spaces:
        return random.choice(free_spaces)

    return False
# Nouvelle fonction pour permettre au joueur de choisir son signe
def choose_player_sign():
    sign = ""
    while sign not in ["X", "O"]:
        sign = input("Choisissez votre signe (X ou O) : ").upper()
        if sign not in ["X", "O"]:
            print("Saisie invalide. Choisissez X ou O.")
    return sign
# Fonction principale pour jouer contre l'IA
def play_with_ai():
    board = [" " for _ in range(9)]
    player_sign = choose_player_sign()
    ai_sign = "O" if player_sign == "X" else "X"
    current_player = "X"

    for turn in range(9):
        display_board(board)
        if current_player == ai_sign:
            print("Tour de l'IA...")
            play_turn(board, current_player, is_ai=True)
        else:
            play_turn(board, current_player, is_ai=False)

        if check_victory(board, current_player):
            display_board(board)
            print(f"Le joueur {current_player} a gagné !")
            return

        current_player = "O" if current_player == "X" else "X"
 # Si personne n'a gagné après 9 tours, c'est un match nul
    display_board(board)
    print("Match nul !")
# Lance le jeu
play_with_ai()





