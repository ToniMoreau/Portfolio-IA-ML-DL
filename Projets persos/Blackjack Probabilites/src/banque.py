

class Compte:
    def __init__(self, montant, proprietaire):
        self.verbose = True
        self.montant = montant
        self.proprietaire = proprietaire
        
    def inVerbose(self, liste_message):
        if self.verbose:
            for msg in liste_message:
                print("[BANQUE]", msg)
    
    def virement(self, somme, destinataire):
        if self.montant >= somme:
            self.montant -= somme
            destinataire.compte.montant += somme
            self.inVerbose([f'Virement de {self.proprietaire} vers {destinataire}'])
            return True
        else:
            self.inVerbose([f'Montant insuffisant !'])
            return False
    