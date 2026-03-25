import pygame
import sys
import numpy as np

from core import GameState, SantoriniRules
from renderer import PyGameRenderer
from joueurs import PyGameHumanPlayer
from santorini import Santorini


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

    screen = pygame.display.set_mode((1200, 900))
    pygame.display.set_caption("Santorini")
    clock = pygame.time.Clock()

    renderer = PyGameRenderer(screen)
    rules = SantoriniRules()

    Toni = PyGameHumanPlayer("Moreau", "Toni")
    Thomas = PyGameHumanPlayer("Ide", "Thomas")

    santorini = Santorini([Toni, Thomas], renderer)
    santorini.rules = rules

    state = GameState()
    state.current_phase = "MENU"

    running = True
    displayed_buttons = []

    while running:
        screen.fill(renderer.ui_state.SABLE)

        # 1) RENDER SELON PHASE

        displayed_buttons = renderer.render(state) or []

        # 2) EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEMOTION:
                renderer.ui_state.mouse_pos = event.pos

            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                callback_result = handle_buttons(displayed_buttons, event)
                print( not(state.current_phase in state.PHASES))
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
                    actions = santorini.rules.legal_actions(state)
                    allowed_actions = [a for a in actions if a.worker_id == selected_worker]
                    allowed_cells = [a.move_to_pos for a in allowed_actions]
                    renderer.ui_state.allowed_cells = allowed_cells
                    renderer.update_active_case_buttons(allowed_cells)
                    
                elif callback_result == "FIN":
                    state = GameState()
                    state.current_phase = "MENU"

                elif type(callback_result) == int and (state.current_phase in state.PHASES):
                    renderer.ui_state.selected_worker = callback_result
                    actions = santorini.rules.legal_actions(state)
                    allowed_actions = [a for a in actions if a.worker_id == callback_result]
                    if state.current_phase == "MOVE":
                        allowed_cells = [a.move_to_pos for a in allowed_actions]
                    else:
                        allowed_cells = [a.build_to_pos for a in allowed_actions]
                    renderer.ui_state.allowed_cells = allowed_cells
                    renderer.update_active_case_buttons(allowed_cells)
                    
                elif isinstance(callback_result, tuple):
                    # Cas des cases du plateau : callback_result = (ligne, col)
                    cell = callback_result
                    print("yes")
                    if state.current_phase == "PLACEMENT":
                        actions = santorini.rules.legal_actions(state)

                        chosen_action = None
                        for action in actions:
                            if action.move_to_pos == cell:
                                chosen_action = action
                                break

                        if chosen_action is not None:
                            state = santorini.rules.apply_action(state, chosen_action)
                            state.current_player = santorini.rules.next_player(state)
                            renderer.update_pion_buttons(state)

                            # Vérifie si tout le monde a placé tous ses ouvriers
                            all_placed = True
                            for worker_id, worker_pos in state.worker_pos_by_worker.items():
                                if worker_pos is None:
                                    all_placed = False
                                    if worker_id in state.workers_by_player[state.current_player]:
                                        print("yes worker ")
                                        renderer.ui_state.selected_worker = worker_id
                            if all_placed:
                                state.current_phase = state.PHASES[0]
                            
                            actions = santorini.rules.legal_actions(state)
                            print("selected worker : ", {renderer.ui_state.selected_worker})
                            allowed_actions = [a for a in actions if a.worker_id == renderer.ui_state.selected_worker]
                            allowed_cells = [a.move_to_pos for a in allowed_actions]
                            renderer.ui_state.allowed_cells = allowed_cells
                            renderer.update_active_case_buttons(allowed_cells)


                    elif state.current_phase == "MOVE":
                        print("MOVE")
                        actions = santorini.rules.legal_actions(state)
                        print(len(actions))
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
                            
                            actions = santorini.rules.legal_actions(state)
                            print("selected worker : ", {renderer.ui_state.selected_worker})
                            allowed_actions = [a for a in actions if a.worker_id == renderer.ui_state.selected_worker]
                            allowed_cells = [a.build_to_pos for a in allowed_actions]
                            renderer.ui_state.allowed_cells = allowed_cells
                            renderer.update_active_case_buttons(allowed_cells)
                            
                    elif state.current_phase == "BUILD":
                        actions = santorini.rules.legal_actions(state)

                        chosen_action = None
                        for action in actions:
                            if action.build_to_pos == cell:
                                chosen_action = action
                                break

                        if chosen_action is not None:
                            state = santorini.rules.apply_action(state, chosen_action)
                            renderer.update_pion_buttons(state)
                            if state.current_phase == state.PHASES[-1]:
                                state.current_player = santorini.rules.next_player(state)
                                renderer.ui_state.selected_worker = state.workers_by_player[state.current_player][0]
                            state.current_phase = santorini.rules.next_phase(state)
                            
                            actions = santorini.rules.legal_actions(state)
                            print("selected worker : ", {renderer.ui_state.selected_worker})
                            allowed_actions = [a for a in actions if a.worker_id == renderer.ui_state.selected_worker]
                            allowed_cells = [a.move_to_pos for a in allowed_actions]
                            renderer.ui_state.allowed_cells = allowed_cells
                            renderer.update_active_case_buttons(allowed_cells)
                    
              
        # 3) REDESSIN FINAL
        screen.fill(renderer.ui_state.SABLE)
        renderer.render(state)

        # 4) FIN DE PARTIE
        if state.current_phase in ("MOVE", "BUILD"):
            winner = santorini.rules.winner(state)
            if winner is not None:
                print(f"Le joueur {winner} a gagné !")
                state.current_phase = "MENU"

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()