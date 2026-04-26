import pygame
import sys
import numpy as np

from core import GameState, SantoriniRules
from renderer import PyGameRenderer
from joueurs import PyGameHumanPlayer, IAPlayer
from santorini import Santorini
from core import MoveAction, BuildAction
import cProfile

def handle_buttons(buttons, event):
    """
    Parcourt les boutons affichés et retourne le callback déclenché si un bouton est activé.
    """
    if not buttons:
        return None

    for btn in buttons:
        result = btn.handle_event(event)
        if result is not None:
            return result
    return None


def main():
    pygame.init()

    screen = pygame.display.set_mode((0,0), flags=pygame.FULLSCREEN)
    pygame.display.set_caption("Santorini")
    clock = pygame.time.Clock()

    renderer = PyGameRenderer(screen)
    rules = SantoriniRules()

    Toni = PyGameHumanPlayer("Moreau", "Toni")
    Thomas = PyGameHumanPlayer("Ide", "Thomas")
    ia_3 = IAPlayer("ia", "ai", evaluation_n=3, depth=3)
    ia_1 = IAPlayer("ia2", "ia2", evaluation_n=1, depth=5)
    ia_2 = IAPlayer("ia2", "ia2", evaluation_n=2, depth=4)

    santorini = Santorini([ia_1, ia_2], renderer)
    santorini.rules = rules
    ia_1.rules = santorini.rules
    ia_3.rules = santorini.rules
    ia_2.rules = santorini.rules
    state = GameState()
    state.current_phase = "MENU"

    running = True
    displayed_buttons = []
    renderer.ui_state.plateau_owner = [[None for j in range(santorini.rules.taille_plateau[1])] for i in range(santorini.rules.taille_plateau[0])]

    while running:
        screen.fill(renderer.ui_state.SABLE)
        # 1) RENDER SELON PHASE
        displayed_buttons = renderer.render(state) or []
       
        #tour IA:
        #if state.current_phase in ["PLACEMENT", "MOVE", "BUILD"]
        player = None if state.current_player is None else santorini.players[state.current_player]
        if isinstance(player, IAPlayer):
            print("ia turn")
            import pstats

            profiler = cProfile.Profile()
            profiler.enable()

            build_move_actions = player.alpha_beta(state)  # ton appel existant
            profiler.disable()
            stats = pstats.Stats(profiler)
            stats.sort_stats('cumulative')
            stats.print_stats(20)  # top 20 fonctions les plus coûteuses

            for action in build_move_actions:
                if isinstance(action, MoveAction) and state.current_phase =="PLACEMENT":
                    santorini.rules.apply_action(state, action)
                    state.current_player = santorini.rules.next_player(state)
                    # Vérifie si tout le monde a placé tous ses ouvriers
                    all_placed = True
                    for worker_id, worker_pos in state.worker_pos_by_worker.items():
                        if worker_pos is None:
                            all_placed = False
                            if worker_id in state.workers_by_player[state.current_player]:
                                if not(isinstance(santorini.players[state.current_player], IAPlayer)):
                                    renderer.ui_state.selected_worker = selected_worker = worker_id
                                    actions = santorini.rules.legal_actions(state, wkr = selected_worker)
                                    allowed_cells = [a.move_to_pos for a in actions]
                                
                    if all_placed:
                        state.current_phase = state.PHASES[0]
                        allowed_cells = []
                        selected_worker = None
                    
                elif isinstance(action, MoveAction) and state.current_phase == "MOVE":
                    santorini.rules.apply_action(state, action)
                    if state.current_phase == state.PHASES[-1]:
                        state.current_player = santorini.rules.next_player(state)
                        allowed_cells = []
                        selected_worker = None
                    state.current_phase = santorini.rules.next_phase(state)
                elif isinstance(action, BuildAction) and state.current_phase == "BUILD":
                    santorini.rules.apply_action(state, action)
                    state.cumsum_plateau +=1
                    renderer.ui_state.plateau_owner[action.build_to_pos[0]][action.build_to_pos[1]] = state.current_player
                    allowed_cells = []
                    if state.current_phase == state.PHASES[-1]:
                        state.current_player = santorini.rules.next_player(state)
                        allowed_cells = []
                        selected_worker = None
                    state.current_phase = santorini.rules.next_phase(state)
                    
            renderer.ui_state.selected_worker = selected_worker
            renderer.ui_state.allowed_cells = allowed_cells
            renderer.update_pion_buttons(state)
            renderer.update_active_case_buttons(allowed_cells, state)
        
        # 2) EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEMOTION:
                renderer.ui_state.mouse_pos = event.pos

            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                callback_result = handle_buttons(displayed_buttons, event)
                if callback_result == "QUITTER":
                    running = False

                elif callback_result == "MENU":
                    state = GameState()
                    state.current_phase = "MENU"

                elif callback_result == "SELECT_NB_JOUEURS":
                    state.current_phase = "SELECT_NB_JOUEURS"

                elif callback_result == "DEUX_JOUEURS":
                    ordre_tour = list(range(len(santorini.players)))
                    np.random.shuffle(ordre_tour)
                    
                    state = santorini.rules.initial_state(ordre_tour)
                    state.current_phase = "PLACEMENT"

                    renderer.ui_state.selected_worker = selected_worker = state.workers_by_player[state.current_player][0]
                    if isinstance(state.current_player, IAPlayer):
                        allowed_cells = []
                    else:
                        actions = santorini.rules.legal_actions(state, wkr = selected_worker)
                        allowed_cells = [a.move_to_pos for a in actions]
                    
                    renderer.ui_state.allowed_cells = allowed_cells
                    renderer.update_active_case_buttons(allowed_cells, state)
                    
                elif callback_result == "FIN":
                    state = GameState()
                    state.current_phase = "MENU"

                elif isinstance(callback_result, int) and callback_result in state.workers_by_player[state.current_player]:
                    if (state.current_phase == state.PHASES[0]):
                        renderer.ui_state.selected_worker = callback_result
                        actions = santorini.rules.legal_actions(state,wkr =  callback_result)
                        if state.current_phase == "MOVE":
                            allowed_cells = [a.move_to_pos for a in actions]
                        else:
                            allowed_cells = [a.build_to_pos for a in actions]
                        renderer.ui_state.allowed_cells = allowed_cells
                        renderer.update_active_case_buttons(allowed_cells, state)
                    elif (state.current_phase == state.PHASES[1]):
                        wkr=renderer.ui_state.selected_worker  
                        actions = santorini.rules.legal_actions(state, wkr = wkr)
                        if state.current_phase == "MOVE":
                            allowed_cells = [a.move_to_pos for a in actions]
                        else:
                            allowed_cells = [a.build_to_pos for a in actions]
                        renderer.ui_state.allowed_cells = allowed_cells
                        renderer.update_active_case_buttons(allowed_cells, state)
                    
                elif isinstance(callback_result, tuple):
                    # Cas des cases du plateau : callback_result = (ligne, col)
                    cell = callback_result
                    if state.current_phase == "PLACEMENT":
                        actions = santorini.rules.legal_actions(state)

                        chosen_action = None
                        for action in actions:
                            if action.move_to_pos == cell:
                                chosen_action = action
                                break

                        if chosen_action is not None:
                            selected_worker = renderer.ui_state.selected_worker

                            state = santorini.rules.apply_action(state, chosen_action)
                            state.current_player = santorini.rules.next_player(state)
                            renderer.update_pion_buttons(state)

                            # Vérifie si tout le monde a placé tous ses ouvriers
                            all_placed = True
                            for worker_id, worker_pos in state.worker_pos_by_worker.items():
                                if worker_pos is None:
                                    all_placed = False
                                    if worker_id in state.workers_by_player[state.current_player]:
                                        renderer.ui_state.selected_worker = selected_worker = worker_id
                            if all_placed:
                                state.current_phase = state.PHASES[0]
                                renderer.ui_state.selected_worker = selected_worker = state.workers_by_player[state.current_player][0]
                                
                            if isinstance(santorini.players[state.current_player], IAPlayer):
                                print("ch")
                                allowed_cells = []
                            else: 
                                actions = santorini.rules.legal_actions(state, wkr = selected_worker)
                                allowed_cells = [a.move_to_pos for a in actions]
                            
                            renderer.ui_state.allowed_cells = allowed_cells
                            renderer.update_active_case_buttons(allowed_cells, state)


                    elif state.current_phase == "MOVE":
                        selected_worker = renderer.ui_state.selected_worker
                        actions = santorini.rules.legal_actions(state, wkr = selected_worker)
                        chosen_action = None
                        for action in actions:
                            if action.move_to_pos == cell:
                                chosen_action = action
                                break

                        if chosen_action is not None:
                            state = santorini.rules.apply_action(state, chosen_action)
                            renderer.update_pion_buttons(state)
                            if state.current_phase == state.PHASES[-1]:
                                state.current_player = santorini.rules.next_player(state)
                                renderer.ui_state.selected_worker = state.workers_by_player[state.current_player][0]
                            state.current_phase = santorini.rules.next_phase(state)
                            
                            actions = santorini.rules.legal_actions(state, wkr = selected_worker )
                            allowed_cells = [a.build_to_pos for a in actions]
                            renderer.ui_state.allowed_cells = allowed_cells
                            renderer.update_active_case_buttons(allowed_cells, state)
                            
                    elif state.current_phase == "BUILD":
                        selected_worker = renderer.ui_state.selected_worker
                        actions = santorini.rules.legal_actions(state, wkr = selected_worker)

                        chosen_action = None
                        for action in actions:
                            if action.build_to_pos == cell:
                                chosen_action = action
                                break

                        if chosen_action is not None:
                            state = santorini.rules.apply_action(state, chosen_action)
                            state.cumsum_plateau +=1
                            renderer.ui_state.plateau_owner[action.build_to_pos[0]][action.build_to_pos[1]] = state.current_player
                            renderer.update_pion_buttons(state)
                            if state.current_phase == state.PHASES[-1]:
                                state.current_player = santorini.rules.next_player(state)
                                renderer.ui_state.selected_worker = state.workers_by_player[state.current_player][0]
                                renderer.ui_state.allowed_cells = []
                            else:
                                actions = santorini.rules.legal_actions(state, wkr = selected_worker)
                                allowed_cells = [a.move_to_pos for a in actions]
                                renderer.ui_state.allowed_cells = allowed_cells
                            
                            state.current_phase = santorini.rules.next_phase(state)
                            renderer.update_active_case_buttons(renderer.ui_state.allowed_cells, state)
        
        # 3) REDESSIN FINAL
        screen.fill(renderer.ui_state.SABLE)
        renderer.render(state)
        
        # 4) FIN DE PARTIE
        if state.current_phase in ("MOVE", "BUILD"):
            winner = santorini.rules.winner(state)
            if winner is not None:
                print(f"Le joueur {winner} a gagné !")
                state.current_phase = "FIN"
                state.winner = winner
                state.cumsum_plateau =0
                state.current_player = None

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()