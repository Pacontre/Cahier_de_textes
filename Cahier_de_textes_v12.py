"""
main.py

Ce fichier est le point d'entrée principal de l'application Cahier de textes portable.

Il crée une application graphique avec une fenêtre d'accueil et une interface principale. 
L'application utilise :
- tkinter pour la création de l'interface graphique
- ttkbootstrap pour le style de l'interface
- SQLite pour la gestion de la base de données

Fonctionnalités principales :
1. Initialisation de la base de données
2. Affichage d'une fenêtre d'accueil pour la sélection de la langue
3. Création de l'interface principale avec plusieurs onglets

En cas d'erreur pendant l'exécution, le traceback complet est imprimé pour faciliter le débogage.

Pour lancer l'application, exécutez simplement ce fichier : python main.py
"""

# Imports
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from database import init_database
from gui import afficher_accueil, create_styled_gui
import traceback 


axes_du_programme = [
    "Identités et échanges", "Espace privé et espace public", "Art et pouvoir",
    "Citoyenneté et mondes virtuels", "Fictions et réalités", "Innovations scientifiques et responsabilité",
    "Diversité et inclusion", "Territoire et mémoire", "Vivre entre générations",
    "Les univers professionnels le monde du travail", "Le village le quartier la ville",
    "Représentation de soi et rapport à autrui", "Sports et société", "La création et le rapport aux arts",
    "Sauver la planète penser les futurs possibles", "Le passé dans le présent"
]

def main():
    print("Début de la fonction main")
    try:
        root = tk.Tk()
        print("Fenêtre Tk créée")
        
        style = Style(theme='cosmo')
        print("Style appliqué")
        
        root.title("Cahier de textes portable")
        root.geometry("1000x800")
        print("Fenêtre configurée")

        init_database()
        print("Base de données initialisée")

        language_var = afficher_accueil(root)
        print("Fenêtre d'accueil affichée")
        
        root.wait_window(root.children['!toplevel'])
        print("Attente de la fermeture de la fenêtre d'accueil terminée")
        
        main_frame, widgets = create_styled_gui(root, language_var, axes_du_programme)
        print("Interface principale créée")

        # Supprimez cette ligne ou commentez-la
        # ttk.Button(main_frame, text="Fermer l'application", command=root.quit).grid(row=11, column=0, columnspan=2, pady=10, sticky="ew")

        print("Juste avant mainloop")
        root.mainloop()
        print("Boucle principale terminée")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        print("Traceback complet:")
        traceback.print_exc()
    

if __name__ == "__main__":
    print("Script principal démarré")
    main()
    print("Script principal terminé")