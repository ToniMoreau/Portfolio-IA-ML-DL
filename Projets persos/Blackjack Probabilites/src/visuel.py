import tkinter as ttk
import customtkinter as ctk
import probabilites as probas
from PIL import Image, ImageTk
import time


# === Configuration globale de CustomTkinter ===
ctk.set_appearance_mode("Dark")   # "Light", "Dark" ou "System"
ctk.set_default_color_theme("blue") # "blue", "green", "dark-blue", etc.



LIMITE_NB_CARTES_A_AFFICHER = 6

VERT_BLACKJACK = "#006400"  # vert foncé style casino


"""img_check = ctk.CTkImage(Image.open("check.png"), size=(20,20))
"""
# === Application principale ===
class App(ctk.CTk):
    def __init__(self, bj):
        super().__init__()
        self.bj = bj
        self.verbose = True
        self.perfcount = True
        self.proba_in_game = True
        # Fenêtre principale
        t_lancement_app = time.perf_counter()
        
        self.title("Black")
        self.geometry("1000x800")

        # === menu latéral (sidebar)===
            ## === initialisation de la sidebar ===
                ### === Fenêtre sidebar sur le coté ===
        self.sidebar_frame = ctk.CTkFrame(self, width=300, height= 2000, corner_radius=0) 
        self.sidebar_frame.grid(row = 0, column = 0)
                ### === Titre de la sidebar ===
        self.sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="Menu", font=ctk.CTkFont(size=16, weight="bold")) 
        self.sidebar_label.grid(row = 0, column = 0, pady=(20,10))
        
        self.proba_btn = ctk.CTkButton(self.sidebar_frame, text=f"appuie pour {"activer" if not self.proba_in_game else "désactiver"}", command= self.activer_probas)
        self.proba_btn.grid(row = 2, column = 0)
            ## === Installation de l'environnement statistiques des cartes (cartes counter) ===
                ### === Fenêtre Statistiques dans la sidebar ===
        self.stats_side_frame = ctk.CTkFrame(self.sidebar_frame)
        self.stats_side_frame.grid(row = 1, column=0)
                ### === Création des labels de chaque card counter
                    #### === Titre du tableau
        self.stats_title = ctk.CTkLabel(self.stats_side_frame, text= "Carte | qté | proba")
        self.stats_title.grid(row = 0, column = 0)
        
        self.stats = [] #liste des labels stats pour les manipuler plus tard
                    #### === boucle pour creer efficacement les labels de chaque card counter 
        for i in range(1,10):
            #on y trouvera numero de carte | nombre de carte | proba de tirer cette carte
            self.stat_label = ctk.CTkLabel(self.stats_side_frame,text=f"{i} | {self.bj.deck.cpt_cartes[i]} | {round(probas.proba_de_tirer_un(i,bj),2)}")
            self.stat_label.grid(row = i, column = 0)
            self.stats.append(self.stat_label)
        
        dix_cpt = bj.deck.cpt_cartes[10] + bj.deck.cpt_cartes[11] + bj.deck.cpt_cartes[12] + bj.deck.cpt_cartes[13]
    
        self.stat_label = ctk.CTkLabel(self.stats_side_frame,text=f"{10} | {dix_cpt} | {round(probas.proba_de_tirer_un(10,bj),2)}")
        self.stat_label.grid(row = 10, column = 0)
        self.stats.append(self.stat_label)

        # === Zone de contenu principal ===
            ## === fenêtre principale mère ===
                ### === Création ===
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row = 0, column = 1)
                ### === Titre de la  fenêtre principale ===
        self.bj_title_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.bj_title_frame.grid(row = 0, column = 0)
        self.label = ctk.CTkLabel(self.bj_title_frame, text="Bienvenue dans mon Black Jack", font=ctk.CTkFont(size=18))
        self.label.grid(row = 0, column = 1,pady=20)


                ### === Espace pour la table de blackjack ===
        self.tableDeBlackjack_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color=VERT_BLACKJACK)
        self.tableDeBlackjack_frame.grid(row = 1, column = 0)
        
                    #### === Création des espaces joueurs (table joueur) ===    
        self.ChaisesPrisesPar_Dict = {} #Dictionnaire qui recense quel chaise (key) est prise par quelle joueur (value) => chaise : joueur / chaise = espaceJouable
        limiteNbEspacesJoueurs = 5  #on limite le nombre de joueur à 5
        for i in range(limiteNbEspacesJoueurs):
            if i > len(self.bj.joueurs)-1:
                joueur = None
            else:
                joueur = self.bj.joueurs[i]
            self.place_jouable_frame = ctk.CTkFrame(self.tableDeBlackjack_frame, width=200, height=300, fg_color="#009900", border_color="black", corner_radius=10, border_width=1)
            self.place_jouable_frame.grid(row = 1, column = i, pady = 5, padx = 5)
            self.place_jouable_frame.grid_propagate(False)
                        ##### === Simulation des joueurs qui prennent chacun un espace jouable /chaise==
            self.ChaisesPrisesPar_Dict[self.place_jouable_frame] = joueur            
                        
        self.joueursVariables_dict = {}
                        ##### === Installation des espaces occupés par les joueurs (interface visuelle) ===
        t_install_joueurs = time.perf_counter()
        for chaise, joueur in self.ChaisesPrisesPar_Dict.items(): #on récupère la chaise et le joueur assis (si il y a un joueur assis)
            chaiseOccupée = not(joueur == None)
            if chaiseOccupée: #si la chaise est occupée
                
                #self.bj.proba_joueurs_bust()
                            ###### === Espace pour le Nom du joueur ===
                nomDuJoueur_label = ctk.CTkLabel(chaise, text=f"{joueur.nom} : ", font=("Arial", 14), text_color="white", wraplength=140)
                nomDuJoueur_label.grid(row = 0, column = 0 , pady=10, padx= 5)
                
                            ###### === Espace pour l'affichage des cartes ===
                cartes_frame = ctk.CTkFrame(chaise, width=180, height = 75,fg_color="#009900")
                cartes_frame.grid(row =1,column = 0)
                #cartes_frame.grid_propagate(False)
                décalage_image_carte = 15 
                
                cartes_liste = [] #listes des cartes 
                for i in range(LIMITE_NB_CARTES_A_AFFICHER):
                    image1 = ctk.CTkLabel(cartes_frame, text="", fg_color=None)
                    image1.place(x=10 + i * décalage_image_carte, y=0) #place() pour meilleure précision d'ancrage
                    cartes_liste.append(image1) #on l'ajoute à la liste de carte

                            ###### === OBSOLETE Affichage des détails des cartes ===
                
                main_detail_label = ctk.CTkLabel(chaise, text=f"{joueur.main}", wraplength=140) #à dégager
                main_detail_label.grid(row= 1, column = 1, pady = 5, padx = 5)
                            ###### === Affichage Valeur de la main en cours du joueur sur la chaise
                valeur_label = ctk.CTkLabel(chaise, text="", wraplength=140)
                valeur_label.grid(row = 2, column = 0, pady = 5, padx = 5)
                            ###### === Questionne l'utilité et l'utilisation de cette frame ===
                decision_frame = ctk.CTkFrame(chaise, width=200, height= 70,fg_color="#009900")
                decision_frame.grid(row = 3, column =0)
                #decision_frame.grid_propagate(False)
                            ###### === Création du bouton individuel "Tirer" pour tirer une carte
                tirerUneCarte_btn = ctk.CTkButton(decision_frame, text="hit") #command= lambda j = joueur : joueur.tirer_ou_se_coucher(j.choix)
                tirerUneCarte_btn.grid(row= 0, column = 0, pady = 10, padx = 10)
                tirerUneCarte_btn.grid_forget()
                            ###### === Création du bouton individuel "seCoucher_btn" pour se coucher
                seCoucher_btn = ctk.CTkButton(decision_frame, text="sleep") #command= lambda j = joueur : joueur.tirer_ou_se_coucher(j.choix)
                seCoucher_btn.grid(row= 1, column = 0, pady = 10, padx = 10)
                seCoucher_btn.grid_forget()
                
                bankroll_frame = ctk.CTkFrame(chaise, bg_color='black')
                bankroll_frame.grid(row = 4, column = 0)
                
                bankroll_label = ctk.CTkLabel(bankroll_frame, text=f" bankroll : {joueur.compte.montant} €",text_color='white')
                bankroll_label.grid(row = 0,column = 0)
                
                bet_label = ctk.CTkLabel(bankroll_frame, text = f"mise en cours : {joueur.mise} €")
                bet_label.grid(row = 1, column = 0)
                
                """modifier_mise_btn = ctk.CTkButton(decision_frame, text = "+")
                modifier_mise_btn.grid(row = 2, column = 0)"""
                
                            ###### === On ajoute toutes ses variables dans une dict pour les manipuler plus tard : chaque joueur reçoit ses propres variables
                self.joueursVariables_dict[joueur] = {}
                self.joueursVariables_dict[joueur]["nom label"] = nomDuJoueur_label
                self.joueursVariables_dict[joueur]["main detail label"] = main_detail_label
                self.joueursVariables_dict[joueur]["valeur main label"] = valeur_label
                self.joueursVariables_dict[joueur]["tirer une carte btn"] = tirerUneCarte_btn
                self.joueursVariables_dict[joueur]["se coucher btn"] = seCoucher_btn
                self.joueursVariables_dict[joueur]["liste des cartes"] = cartes_liste
                self.joueursVariables_dict[joueur]["bankroll label"] = bankroll_label
                self.joueursVariables_dict[joueur]["bet label"] = bet_label
                #self.joueursVariables_dict[joueur] = [nomDuJoueur_label, main_detail_label, valeur_label, tirerUneCarte_btn, seCoucher_btn, cartes_liste]
        self.perf_counter(time.perf_counter(), t_install_joueurs, "installation joueur a la table")
                ### === Espace Croupier ===
                    #### === Stats du Croupier 
        t_install_croupier = time.perf_counter()
        
        croupier_stats_frame = ctk.CTkFrame(self.tableDeBlackjack_frame, width= 200, height=100)
        croupier_stats_frame.grid(row = 0, column = 3)
        
        
        
        title_stats_croupier = ctk.CTkLabel(croupier_stats_frame, text= "      17   |   18   |   19   |   20   |   21   |   22   |   BUST  |")
        title_stats_croupier.grid(row = 0,column = 0)
        stats_croupier = ""
        for i in range(17,23):
            stats_croupier += f"{probas.proba_score(i,self.bj.croupier, self.bj)} | "
        stats_croupier += f"{probas.proba_score([22,23,24,25,26],self.bj.croupier,self.bj)}"
        
        self.stats_croupier  = ctk.CTkLabel(croupier_stats_frame, text= stats_croupier)
        self.stats_croupier.grid(row = 1, column = 0)
        

                    #### === Table du Croupier ===
        tableDuCroupier_frame = ctk.CTkFrame(self.tableDeBlackjack_frame, width= 150, height=150, fg_color="brown",border_color="black", border_width=1, corner_radius=10)
        tableDuCroupier_frame.grid(row =0, column= 2, pady = 30)
        tableDuCroupier_frame.grid_propagate(False)
                        ##### === Nom du Croupier ===
        self.nomDuCroupier_label = ctk.CTkLabel(tableDuCroupier_frame, text=f"{self.bj.croupier}", font=("Arial", 12), wraplength=140)
        self.nomDuCroupier_label.grid(row = 0, column = 0)
        self.probaCroupier_label = ctk.CTkLabel(tableDuCroupier_frame, text= "")
        self.probaCroupier_label.grid(row =1, column = 0)
                        ##### === Affichage des cartes du Croupier ===
                            ###### === Emplacement des cartes ===
        cartesDuCroupier_frame = ctk.CTkFrame(tableDuCroupier_frame)
        cartesDuCroupier_frame.grid(row = 2,column = 0)
        cartesDuCroupier_frame.grid_propagate(False) #empécher les cartes de dépasser le cadre, elle vont respecter le cadre
        self.cartesCroupier_liste = [] #liste qui regroupe toutes les cartes du croupier
        for i in range(LIMITE_NB_CARTES_A_AFFICHER): #affichage des cartes du croupier (limité)
            carteCroupier_image = ctk.CTkLabel(cartesDuCroupier_frame, text="")
            carteCroupier_image.place(x = 10 + i * décalage_image_carte, y =10)
           
            self.cartesCroupier_liste.append(carteCroupier_image)#ajout à la liste
            
        self.perf_counter(time.perf_counter(), t_install_croupier, "installation croupier")
                ### === Espace fausse/Deck
                    #### === Emplacement fausse ===
        
        self.fausse_frame = ctk.CTkFrame(self.tableDeBlackjack_frame, width = 70, height=70, fg_color="brown")
        self.fausse_frame.grid(row=0,column = 0, padx =5, pady =10)
        #self.fausse_frame.grid_propagate(False)
        
                        ##### === Affichage carte de dos dans la fausse ===
        carteFausse_path = "cartes/dos.jpg"
        carteFausse_image = Image.open(carteFausse_path).convert("RGBA")

        # Redimensionner si nécessaire
        carteFausse_image = carteFausse_image.resize((40, 70))

        # Convertir pour tkinter
        carteFausseTK_image = ImageTk.PhotoImage(carteFausse_image)

        self.carteFausse_affichage = ctk.CTkLabel(self.fausse_frame,image=carteFausseTK_image, text = '')
        self.carteFausse_affichage.grid(row =0, column = 0)
                        ##### === Info de la fausse : nb cartes dedans
        self.fausse_info = ctk.CTkLabel(self.fausse_frame,wraplength=60, text=f"fausse : {self.bj.deck.fausse} ", font=("Arial", 12), text_color="white")
        self.fausse_info.grid(row= 1, column = 0, padx = 5, pady = 5)
                    
                    #### === Emplacement Deck ===
        self.deck_frame = ctk.CTkFrame(self.tableDeBlackjack_frame)
        self.deck_frame.grid(row = 0, column = 1)
                        ##### === Deck info : nb cartes restante dans le deck
        self.deck_counter = ctk.CTkLabel(self.deck_frame, text=f"Deck Info: \n {self.bj.deck}")
        self.deck_counter.grid(row= 0, column = 1)

                ### === Lancer boutton ===
        self.lancer_btn = ctk.CTkButton(self.tableDeBlackjack_frame, text="Lancer Game", command=self.lancer_partie)
        self.lancer_btn.grid(row = 3, column = 2, pady = 10)
        self.perf_counter(time.perf_counter(), t_lancement_app, "pour lancer l'app")
        
    # === Fonctions d'actions ===        
    def activer_probas(self):
        self.proba_in_game = not(self.proba_in_game)
        self.proba_btn.configure(text=f"appuie pour {"activer" if not self.proba_in_game else "désactiver"}")
    def inVerbose(self, liste_vocaux):
        if self.verbose:
            for element in liste_vocaux:
                print("[AFFICHAGE]",element)
    def perf_counter(self, t1,t0, nom):
        if self.perfcount:
            print("[AFFICHAGE]",f"⏱ temps {nom} : {t1 - t0:.6f} seconds")
            print("-"*30)
    def à_shuffle(self): # Modifie l'état visuel de la  fausse
        if self.bj.deck.a_shuffle: #si il faut mélanger ça devient rouge
            self.inVerbose(["a shuffle affiché "])
            self.fausse_frame.configure(border_color = "red", border_width = 3)
        else: #reinitialise la couleur à noir sinon
            self.fausse_frame.configure(border_color = "black", border_width = 3)
    
    def update_stats_deck(self): #refresh des stats de chaque cartes dans le deck
        stats_croupier = ""
        for i in range(17,23):
            stats_croupier += f"{probas.proba_score(i,self.bj.croupier, self.bj)} | "
        stats_croupier += f"{probas.proba_score([22,23,24,25,26],self.bj.croupier,self.bj)}"
        self.stats_croupier.configure(text = stats_croupier)
        
        for i in range(1,len(self.stats)):
            self.stats[i-1].configure(text = f"{i} | {self.bj.deck.cpt_cartes[i]} | {round(probas.proba_de_tirer_un(i,self.bj),2)} %" ) #######
        dix_cpt = self.bj.deck.cpt_cartes[10] + self.bj.deck.cpt_cartes[11] + self.bj.deck.cpt_cartes[12] + self.bj.deck.cpt_cartes[13]
        self.stats[9].configure(text = f"{10} | {dix_cpt} | {round(probas.proba_de_tirer_un(10,self.bj),2)} %" ) #######
        print("SOMME " ,sum(self.bj.deck.cpt_cartes.values()))
        self.inVerbose(["affichage stats du deck à jour ✔"])

    def update_affichage_cartes(self,quel_joueur, image_object ): #refresh les mains sur le tapis
        for i,carte in enumerate(quel_joueur.main.cartes):
            image_path = carte.image
            pil_image = Image.open(image_path).convert("RGBA")

            # Redimensionner si nécessaire
            pil_image = pil_image.resize((40, 70))

            # Convertir pour tkinter
            tk_image = ImageTk.PhotoImage(pil_image)

            # Créer un label pour afficher l'image
            image_object[i].configure(image = tk_image)
        self.inVerbose([f"affichage des cartes de {quel_joueur} updated ✔"])

    def lancer_partie(self):
        t_lancement_partie = time.perf_counter()
        # === Réinitialisation des couleurs des tapis et cartes de chaque joueur ===
        for chaise, joueurAssis in self.ChaisesPrisesPar_Dict.items(): #pour chaque chaise et son joueur associé
                if joueurAssis: #si le joueur est assis sur cette chaise
                    chaise.configure(fg_color = "#009900" ) #on remet la couleur initiale
        for variables in self.joueursVariables_dict.values(): # pour chaque joueur et ses variables
            for i in range(LIMITE_NB_CARTES_A_AFFICHER): #on enlève les cartes des tapis (joueur et croupier)
                #variables[5][i].configure(image = "")
                variables["liste des cartes"][i].configure(image = "")
                self.cartesCroupier_liste[i].configure(image="")
        # === Suppression du bouton lancer       
        self.lancer_btn.grid_forget()
        # === Lancement de la partie ===
        
        self.bj.lancer_partie() 
        for joueur in self.bj.joueurs:
            self.joueursVariables_dict[joueur]['bankroll label'].configure(text = f"bankroll :{joueur.compte.montant} €")
            self.joueursVariables_dict[joueur]["bet label"].configure(text =f"mise : {joueur.mise} €")
        self.à_shuffle() #vérification s'il faut shuffle à la prochaine manche
            ## === Affichage des premiers visuels de la premiere étape de la partie
        if self.proba_in_game:
            probas.proba_bust(self.bj.liste_joueur_debout + [self.bj.croupier],self.bj)                                #######
        self.update_stats_deck() #
        self.affichage_détails_chaise() #On affiche les 2 cartes des joueurs + la carte du croupier 
            ## === Initialisation des méthode de décision des joueurs (récurrence sur joueur 1)
                ### === Récupération du premier joueur de la liste et de ses options
        joueur1 = self.bj.liste_joueur_debout[0]
        options = self.joueursVariables_dict[joueur1]
                ### === Configuration des visuels des décisions (tirer/se coucher)
        #tirer_btn = self.joueursVariables_dict[joueur1][3] #on récupère le boutton tirer du joueur en cours
        tirer_btn = self.joueursVariables_dict[joueur1]["tirer une carte btn"] #on récupère le boutton tirer du joueur en cours
        tirer_btn.configure(command = lambda: self.continuer(joueur1, "hit", options)  ) #on lui configure la commande continuer("hit")
        tirer_btn.grid(row= 3, column = 1)
        
        seCoucher_btn = self.joueursVariables_dict[joueur1]["se coucher btn"] #on récupère le boutton se coucher du joueur en cours
        #seCoucher_btn = self.joueursVariables_dict[joueur1][4] #on récupère le boutton se coucher du joueur en cours
        seCoucher_btn.configure(command = lambda: self.continuer(joueur1, "sleep", options)  ) #on lui configure la commande continuer("sleep")
        seCoucher_btn.grid(row = 4, column  =1)
        
        self.perf_counter(time.perf_counter(), t_lancement_partie, "lancement partie")
        self.inVerbose(["affichage du lancement de la partie à jour."])
    def affichage_détails_chaise(self):
        # === Fonction de l'affichage des détails pour le premier tour === 
            ## === Pour chaque joueur on définit la valeur de sa main
        for joueur, variables in self.joueursVariables_dict.items(): #Pour chaque joueur présent
            #valeur_main_label = variables[2]
            valeur_main_label = variables["valeur main label"]
                ### === Si le joueur à blackjack à l'issu du premier tour ===
            if joueur.est_couché: 
                valeur_main_label.configure(text=f"{21} | BLACKJACK",font=("Arial", 14))
                ### === Sinon ===
            else:
                    #### === on affiche la valeur de la main et la proba du joueur de bust
                valeur_main_label.configure(text=f"{joueur.main.valeur} | bust : {joueur.main.proba_bust}%")
            ## === On affiche les cartes des joueurs et du croupier
            #self.update_affichage_cartes(joueur, self.joueursVariables_dict[joueur][5])       
            
            self.update_affichage_cartes(joueur, self.joueursVariables_dict[joueur]["liste des cartes"])       

        self.update_affichage_cartes(self.bj.croupier, self.cartesCroupier_liste)
            ## === On affiche la proba de bust du croupier
        self.nomDuCroupier_label.configure(text = f"{self.bj.croupier} : {self.bj.croupier.main.valeur}")
        if self.proba_in_game:
            self.probaCroupier_label.configure(text=f"bust : {self.bj.croupier.main.proba_bust}%")
            ## === on update le nb carte du deck et de la fausse
        self.deck_counter.configure(text = f"Deck Info: \n {self.bj.deck}")
        self.fausse_info.configure(text = f"Fausse : {self.bj.deck.fausse}")
        self.inVerbose(["Affichage du premier tour à jour"])      
    def continuer(self, joueur, action, options):
        # === fonction qui gère les décisions au tour à tour
            ## === Renommage des variables pour plus de visibilité
        #cartes_joueur_labels = options[5] #les ctk labels de chaque carte de la main du joueur 
        #valeur_label = options[2] #les labels pour afficher la valeur de la main
        #tirer_btn = options[3]
        #seCoucher_btn = options[4]
        t_choix = time.perf_counter()
        
        cartes_joueur_labels = options["liste des cartes"] #les ctk labels de chaque carte de la main du joueur 
        valeur_label = options["valeur main label"] #les labels pour afficher la valeur de la main
        tirer_btn = options["tirer une carte btn"]
        seCoucher_btn = options["se coucher btn"]

        
            ## === Phase de décision du joueur - il tire sa carte ou se couche ===
        joueur.choix = action
        self.bj.tirer_ou_se_coucher(joueur, action)
            ## === Phase d'actualisation de la fenêtre ===
        if self.proba_in_game:
            probas.proba_bust(self.bj.liste_joueur_debout + [self.bj.croupier],self.bj)
            self.probaCroupier_label.configure(text = f"bust : {self.bj.croupier.main.proba_bust} %")#######
        valeur_label.configure(text = f"{joueur.main.valeur} | bust : {joueur.main.proba_bust}%")

        self.update_stats_deck()
        self.update_affichage_cartes(joueur, cartes_joueur_labels)
        self.à_shuffle()
            ## === Boucle de vérification de quel joueur est le suivant ===
                ### === Si le joueur se couche et qu'il reste des joueurs ===
        if joueur.est_couché and not(self.bj.liste_joueur_debout == []):
                    #### === On efface les options de jeu du joueur ===
            tirer_btn.grid_forget()
            seCoucher_btn.grid_forget()
                    #### === On change de joueur ===
            joueur_suivant = self.bj.liste_joueur_debout[0]
            options = self.joueursVariables_dict[joueur_suivant]
                    #### === On fait apparaître les options de jeu du joueur suivant
            #tirer_btn = self.joueursVariables_dict[joueur_suivant][3]
            tirer_btn = self.joueursVariables_dict[joueur_suivant]["tirer une carte btn"]
            #seCoucher_btn = self.joueursVariables_dict[joueur_suivant][4]
            seCoucher_btn = self.joueursVariables_dict[joueur_suivant]["se coucher btn"]       
                 
            tirer_btn.configure(command = lambda: self.continuer(joueur_suivant, "hit", options)  )
            seCoucher_btn.configure(command = lambda: self.continuer(joueur_suivant, "sleep", options)  )
            tirer_btn.grid(row= 3, column = 1)
            seCoucher_btn.grid(row= 4, column = 1)

        elif not(joueur.est_couché):
            pass
        else:
                ### === Si tout le monde est couché ===
                    #### === On efface les options de jeu du dernier joueur ===
            tirer_btn.grid_forget()
            seCoucher_btn.grid_forget()
                    #### === Le croupier tire ses cartes
            self.bj.décision_croupier()
                        ##### === On actualise la situation du croupier
            self.update_affichage_cartes(self.bj.croupier, self.cartesCroupier_liste)
            self.nomDuCroupier_label.configure(text=f"{self.bj.croupier} : {self.bj.croupier.main.valeur}") 
                    #### === On affiche le résultat pour chaque joueur (Gagné/Perdu)
            
            for chaise, assis in self.ChaisesPrisesPar_Dict.items():
                if assis:
                    chaise.configure(fg_color = "red" if assis.main.result =="perdu" else "green" if assis.main.result == "gagné" else "yellow")
                    self.joueursVariables_dict[assis]["valeur main label"].configure(text=f"{assis.main.valeur} {"✅" if assis.main.result=="gagné" else "❌" if assis.main.result == "perdu" else ""} {assis.main.result}",font=("Arial", 14))
            
                    #### === On clear les mains de tout le monde ===
            self.bj.ramasser_main()
            for joueur in self.bj.joueurs:
                self.joueursVariables_dict[joueur]['bankroll label'].configure(text = f"bankroll : {joueur.compte.montant} €")
                self.joueursVariables_dict[joueur]["bet label"].configure(text = 'mise : 0 €')
                    #### === On refait apparaître le boutton lancer === 
            self.lancer_btn.grid(row = 3, column = 2)

            ## === On actualise les compteurs de deck et fausse
        self.deck_counter.configure(text = f"Deck Info: \n {self.bj.deck}")
        self.fausse_info.configure(text = f"Fausse : {self.bj.deck.fausse}")
        self.perf_counter(time.perf_counter(), t_choix, "action (tirer/se coucher/décision croupier)")
        

    @property
    def get_list_of_joueur(self):
        return self.bj.joueurs
        
    def show_home(self):
        self.clear_main()
        ctk.CTkLabel(self.tableDeBlackjack_frame, text="Page d'accueil", font=ctk.CTkFont(size=18)).grid(pady=20)

    def clear_main(self):
        """Détruit tous les widgets du tableDeBlackjack_frame avant d'afficher un nouvel écran"""
        for widget in self.tableDeBlackjack_frame.winfo_children():
            widget.destroy()


