class GameState:
    def __init__(self):
        self.hauteur_plateau = [] #représentation matricielle de la hauteur du plateau (case par case)
        
        self.workers_by_player   = {} # id player rend liste de workers
        
        self.worker_pos_by_worker = {} # id worker rend position worker (ligne, col)
        self.occupants ={}             #dictionnaire : emplacement rend None si pas dedans, ou un ouvrier si un ouvrier est sur l'emplacement
        self.current_player = None
        
        self.nb_joueurs = 0              #initialisé à 0, géré par le Santorini Rules.
        self.nb_workers_per_player = 0   #initialisé à 0, géré par le Santorini Rules.
        
        self.PHASES = ["MOVE", "BUILD"]  #Grande phases de jeu, hormis la phase de placement initial
        self.current_phase = ""          #Permet le placement initial lorsque mis sur ""
        
        self.ordre_passage_joueurs_liste  = []
        self.ordre_passage_index : int = 0
    
    #Méthodes utiles
    def is_occupied(self, cell):
        #permet de verifier si la case est occupée (nous même y compris) et renvoie un tuple (bool, ouvrier)
        #ce tuple permet de check ensuite si la cell testée est occupée par nous meme ou pas. Utile 
        for worker_pos in self.worker_pos_by_worker.values():
            if cell == worker_pos:
                return (True, self.occupants[worker_pos])
        return (False, None)
