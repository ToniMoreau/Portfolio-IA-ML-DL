
from core.gameState import GameState
from core.action import MoveAction, BuildAction, Action

import numpy as np

class SantoriniRules:
    #L'unique classe qui s'occupe de toues les rêgles du Santorini, de sorte à ce que la classe Santorini ne soit qu'un exécutant.
    #Permet une grande flexibilité des rêgles
    def __init__(self):
        self.taille_plateau = (5,5,3)                           #lignes/colonnes/hauteur
        self.hauteur_victoire : int = 3                         #permet de changer les regles de condition de victoire par hauteur
        self.perimetre_deplacement : int = 1                    #permet de changer les regles de perimetre de deplacement
        self.perimetre_construction : int = 1                   #permet de changer les regles de perimetre de construction
        self.nb_workers_per_player :int = 2
        self.hauteur_max_building :int = self.hauteur_victoire+1#on peut construire sur la hauteur de victoire mais pas plus haut.
        self.nb_joueur = 2
        
        
    def __str__(self):
        pass
    ## METHODES UTILES
    def next_player(self, state : GameState) -> int: # le % (modulo) gère parfaitement la rotation (retour au joueur 1 apres le dernier joueur)
        state.ordre_passage_index = (state.ordre_passage_index + 1) % len(state.ordre_passage_joueurs_liste)
        return state.ordre_passage_joueurs_liste[state.ordre_passage_index]
    def next_phase(self, state : GameState) -> int: # le % (modulo) gère parfaitement la rotation (retour à la phase 1 apres la derniere phase)
        state.current_phase = state.PHASES[((state.PHASES == state.current_phase) +1) % len(state.PHASES)]
        return state.current_phase
    ## Réinitialisation de l'état de jeu
    def initial_state(self, liste_joueurs_dans_l_ordre) -> GameState:
        # On intialise ici la classe qui regroupe tous les états essentiels du jeu. Tout se remet à zéro.
        # Le GameState s'initialise ainsi selon toutes les règles de la classe Rules.
        state = GameState()
        
        state.PHASES = ["MOVE", "BUILD"]                                    #les phases de jeux sont réinitialisés
        state.current_phase =""                                             #début sur aucune phase, permet la phase de lancement 
        
        state.nb_joueurs = self.nb_joueur                                   #GameState initialise le nb de joueur en fonction des règles
        state.nb_workers_per_player = self.nb_workers_per_player            #GameState initialise le nb d'ouvriers par joueur en fonction des règles
        
        
        worker_id = 0
        for player in range(state.nb_joueurs):                              #initialise les ouvriers un par un, joueur par joueur.
            state.workers_by_player[player] = []
            for _ in range(state.nb_workers_per_player):
                state.workers_by_player[player].append(worker_id) 
                state.worker_pos_by_worker[worker_id] = None                # pas encore placé
                worker_id += 1
                
        state.occupants = {}                                                #dictionnaire : keys : position, value : ouvrier
                
        state.hauteur_plateau = [[0]*5 for _ in range(5)]                   #hauteurs remises à zéro
        state.ordre_passage_index = 0                                               #début de partie sur premier joueur de la liste des joueurs ordonnés
        state.ordre_passage_joueurs_liste = liste_joueurs_dans_l_ordre
        state.current_player = liste_joueurs_dans_l_ordre[state.ordre_passage_index]#Le joueur 0 de la liste des joueurs dans l'ordre de passage et le joueur actuel
        return state
    
    ## GESTION DES ACTIONS DU JEUX : autorisation et exécution des actions
    def legal_actions(self, state: GameState, player= None) -> list[Action]: 
        #Gestion des actions possibles selon la phase
        #return une liste d'actions (classe Action) à proposer au joueur dans le jeu.
        if state.current_phase == "PLACEMENT":
            actions = self.initial_legal_move(state)
        elif state.current_phase == "MOVE":
            actions = self.legal_moves(state)
        elif state.current_phase == "BUILD":
            actions = self.legal_builds(state)
        else:
            raise ValueError("La phase choisi n'est pas définie")
        return actions
            
    def apply_action(self, state : GameState, action : MoveAction | BuildAction) -> GameState:
        #Pour chaque type d'action, essaie de faire l'action, et renvoie une erreur précise si action impossible.
        if state.current_phase == "BUILD":
            try:
                if action.build_to_pos:
                    ligne_build, col_build  = action.build_to_pos 
                    state.hauteur_plateau[ligne_build][col_build] +=1
                    return state
                else: 
                    print("L'emplacement de construction est nul, pas de construction.")
                    return state
                    
            except Exception as e:
                print("Exception : ",e)
                return state
        else:
            try:
                if action.move_to_pos:
                    state.worker_pos_by_worker[action.worker_id] = action.move_to_pos
                    state.occupants[action.move_to_pos] = action.worker_id
                    return state
                    
            except Exception as e:
                print("Exception : ", e)
                return state
   
    def initial_legal_move(self,state: GameState) -> list[Action]:
        #plan initial de placement des ouvriers.
        player = state.current_player
        actions= []
        for worker in state.workers_by_player[player]:
            #si l'ouvrier courant à déja une position, alors on passe au suivant
            if state.worker_pos_by_worker[worker]:
                continue
            else:
            #sinon, on récupère toutes les actions permissibles de l'ouvrier courant
                for ligne in range(self.taille_plateau[0]):
                    for col in range(self.taille_plateau[1]): 
                        #En phase initial, il suffit de vérifier que la case testée n'est pas encore occupée.
                        is_occupied, _ = state.is_occupied((ligne,col))
                        if is_occupied:
                            continue
                        else:
                            #si elle est libre, alors elle est ajoutée à la liste des actions possibles
                            action = MoveAction(worker, (ligne,col))
                            actions.append(action)
        return actions

    def legal_moves(self, state :  GameState, player = None) -> list[MoveAction]:
        #LA méthode qui teste si un déplacement est possible.
        def is_legal_move(worker_pos, move_pos) -> bool:
            #petite sous méthode qui vérifie si le déplacement est autorisé, donc renvoie True pour oui, False pour non.
            is_occupied , _ = state.is_occupied(move_pos)
            if is_occupied: #pas de déplacement sur un joueur
                return False
            
            #récupère l'emplacement du déplacement futur, et celui de l'ouvrier
            move_ligne,move_col = move_pos
            ligne_ouvrier, col_ouvrier = worker_pos

            #récupère la hauteur du joueur actuel vs la hauteur du déplacement à venir
            worker_height = state.hauteur_plateau[ligne_ouvrier][col_ouvrier]
            move_to_height = state.hauteur_plateau[move_ligne][move_col]
            
            if (abs(move_ligne- ligne_ouvrier) <= self.perimetre_deplacement) and (abs(move_col - col_ouvrier) <= self.perimetre_deplacement):
                #Teste si le déplacement futur est dans le périmètre autorisé par les rêgle
                if move_to_height - worker_height > 1:
                    #teste si la hauteur du déplacement futur permet le déplacement
                    return False #trop haut
                return True #hauteur + distance valide
            return False #distance trop grande
            #FIN SOUS METHODE
        
        player = player if player else state.current_player #si en entrée on a mis aucun joueur, on prend le joueur courant.
        move_actions =[]
        for worker in state.workers_by_player[player]:
            #Pour chaque ouvrier du joueur testé : récup son emplacement, teste pour chaque case du jeu si on peut s'y déplacer.
            ligne_worker, col_worker = state.worker_pos_by_worker[worker]
            for ligne_move in range(self.taille_plateau[0]):
                for col_move in range(self.taille_plateau[1]): 
                    if is_legal_move((ligne_worker,col_worker), (ligne_move,col_move)):
                        #On peut s'y déplacer, donc on enregistre l'action et l'ajoute à la liste des actions possibles.
                        move_action = MoveAction(worker, (ligne_move, col_move))
                        move_actions.append(move_action)
        return move_actions
                                   
    def legal_builds(self, state : GameState, player = None) -> list[BuildAction]:
        #LA méthode qui teste si une construction est possible.
        def is_legal_build(worker_pos, build_pos):
            #sous méthode teste si la construction est possible, donc bool True pour oui, False pour non
            is_occupied, _ = state.is_occupied(build_pos)
            if is_occupied: #pas de construction sur un joueur, mais valide sur mon ancienne position
                return False
            
            #récup l'emplacement de la construction future, et celui de l'ouvrier
            build_ligne,build_col = build_pos
            ligne_ouvrier, col_ouvrier = worker_pos
            
            #récup la hauteur de la construction future
            move_to_height = state.hauteur_plateau[build_ligne][build_col]    
            
            if (abs(build_ligne- ligne_ouvrier) <=self.perimetre_construction) and (abs(build_col - col_ouvrier) <= self.perimetre_construction):
                if move_to_height == (self.hauteur_max_building): #pas de construction si hauteur max déja atteinte
                    print("Pas de construction car hauteur max déja atteinte.")
                    return False
                return True #Construction valide
            #FIN SOUS METHODE
            
        player = player if player else state.current_player #récup le joueur courant si aucun joueur spécifié en entrée de méthode
        build_actions = []
        for worker in state.workers_by_player[player]:
            #Pour chaque ouvrier du joueur : récup sa position, teste pour chaque case de jeu la validité de la construction
            ligne_worker, col_worker = state.worker_pos_by_worker[worker]
            for ligne_build in range(self.taille_plateau[0]):
                for col_build in range(self.taille_plateau[1]): 
                    if is_legal_build((ligne_worker,col_worker), (ligne_build,col_build)):
                        #le build est autorisé donc enregistrement de l'action + ajout à la liste des actions autorisés
                        build_action = BuildAction(worker, (ligne_build, col_build))
                        build_actions.append(build_action)
        return build_actions
    
    # GESTION DE LA FIN DE PARTIE : victoire, défaite
    def winner(self, state: GameState) -> int:
        # victoire hauteur
        for joueur_id in state.ordre_passage_joueurs_liste:
            #pour chaque joueur dans la liste des joueur dans l'ordre de passage, 
            if self.is_winner_by_height(state, joueur_id):
                #teste si le joueur est vainqueur par hautuer
                return joueur_id

        # victoire par élimination aussi possible : seul joueur survivant
        survivors = [j for j in range(self.nb_joueur) if not self.is_looser(state, j)]
        if len(survivors) == 1:
            #un seul survivant == vainqueur
            return survivors[0]

        return None #personne n'est a la hauteur de victoire et il reste plusieurs survivants.

    def is_winner_by_height(self, state: GameState, joueur = None) -> bool:
        #La victoire classique du jeu, hauteur de victoire atteinte, return True pour victoire, False pour pas de victoire courante
        player = joueur if joueur else state.current_player
        
        for worker in state.workers_by_player[player]:
            #pour chaque ouvrier du joueur testé, est-ce qu'il est à la hauteur de victoire?
            pos = state.worker_pos_by_worker[worker]
            if pos is None:
                continue
            i,j = pos
            if state.hauteur_plateau[i][j] == self.hauteur_victoire:
                return True #OUI, donc True
        return False #NON, False
            
    def is_looser(self, state: GameState, joueur = None) -> bool:
        #teste si le joueur est éliminé, pas de move possible.
        joueur = joueur if joueur else state.current_player
        if not self.legal_moves(state, joueur):
            return True #le joueur a perdu car il ne peut plus bouger
        else: return False #le joueur peut bouger.
                     
    def fin_partie(self, state: GameState) -> bool:
        #la partie est terminée si il y a un vainqueur
        return self.winner(state) is not None
