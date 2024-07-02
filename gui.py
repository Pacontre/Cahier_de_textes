"""
gui.py

Ce script est un module de l'application graphique "Cahier de textes portable". 
Il gère l'interface utilisateur, la gestion des données et la logique de l'application.

Le script utilise tkinter pour la création de l'interface utilisateur, ainsi que des 
modules personnalisés pour la gestion de la base de données et d'autres fonctionnalités.

Fonctions principales :
- update_objectifs_grammaticaux : Met à jour la liste des objectifs grammaticaux selon la langue.
- init_global_variables : Initialise les variables globales de l'application.
- afficher_accueil : Crée et affiche la fenêtre d'accueil.
- create_styled_gui : Crée l'interface utilisateur principale.
- create_scrollable_frame : Crée un cadre défilable pour les widgets.
- Diverses fonctions 'create_*' : Créent différentes sections de l'interface principale.
- copier_travail_a_faire : Copie le texte du travail à faire dans le presse-papiers.
- Fonctions de mise à jour (update_*, remove_from_*) : Gèrent les listes de titres et 
  de points grammaticaux dans l'interface et la base de données.

Le script se termine par la fonction 'main', point d'entrée qui initialise l'interface 
et gère les erreurs potentielles.

Ce module est conçu pour être importé et utilisé par le script principal de l'application.
"""


import tkinter as tk
from tkinter import ttk
from database import load_titles, get_grammar_points, add_grammar_point
from utils import ajouter_titre, supprimer_titre, ajouter_point_grammatical, supprimer_point_grammatical, generer_texte_final, copier_texte
from PIL import Image, ImageTk
import sys
import os

# Déclaration des variables globales
titles_listbox = None
titre_entry = None
grammar_listbox = None
objectifs_dropdown = None
update_objectifs_grammaticaux_func = None

# Autres variables globales
all_titles = []
all_grammar_points = []
titre_widgets = []
objectif_widgets = []



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def update_objectifs_grammaticaux(language_var, objectifs_dropdown, all_objectifs):
    language = language_var.get()
    all_objectifs[:] = get_grammar_points(language)
    objectifs_dropdown['values'] = all_objectifs

def init_global_variables():
    global all_titles, all_grammar_points, titre_widgets, objectif_widgets
    all_titles = load_titles()
    all_grammar_points = get_grammar_points("Espagnol")  # Assurez-vous que la langue par défaut est correcte
    titre_widgets.clear()
    objectif_widgets.clear()

from PIL import Image, ImageTk

def filter_titles(entry, listbox=None):
    typed = entry.get().lower()
    all_titles = load_titles()
    filtered = [title for title in all_titles if typed in title.lower()]
    
    if isinstance(entry, ttk.Combobox):
        entry['values'] = filtered
    
    if listbox:
        listbox.delete(0, tk.END)
        for title in filtered:
            listbox.insert(tk.END, title)

def remove_blue_background(image):
    image = image.convert("RGBA")
    data = image.getdata()
    new_data = []
    for item in data:
        # Change all blue (or close to blue) pixels to transparent
        if item[2] > 200 and item[0] < 100 and item[1] < 100:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    image.putdata(new_data)
    return image

def afficher_accueil(root):
    print("Début de la fonction afficher_accueil")
    try:
        root.withdraw()
        print("Fenêtre principale masquée")

        accueil = tk.Toplevel(root)
        accueil.title("Cahier de textes portable - Accueil")
        accueil.geometry("600x500")
        accueil.configure(bg="#F5F5F5")
        print("Fenêtre d'accueil créée")

        label_bienvenue = ttk.Label(accueil, text="CAHIER DE TEXTES", font=("Helvetica Neue", 36, "bold"), background="#F5F5F5")
        label_bienvenue.pack(pady=(50, 30))
        print("Label de bienvenue ajouté")

        ttk.Label(accueil, text="Sélectionnez votre langue :", font=("Helvetica Neue", 16), background="#F5F5F5").pack(pady=(20, 30))
        print("Label de sélection de langue ajouté")

        language_var = tk.StringVar(value="Espagnol")
        languages = [('Espagnol', 'spain.png'), ('Italien', 'italy.png'), ('Anglais', 'uk.png'), ('Allemand', 'germany.png')]
        
        flags_frame = ttk.Frame(accueil)
        flags_frame.pack()

        def on_flag_click(lang, canvas):
            language_var.set(lang)
            for c in flag_canvases:
                c.config(bg="#F5F5F5")
            canvas.config(bg="#E8E8E8")

        flag_canvases = []
        for lang, flag_file in languages:
            img = Image.open(resource_path(f"images/{flag_file}"))
            img = img.resize((60, 40), Image.LANCZOS)
            flag_img = ImageTk.PhotoImage(img)
            
            canvas = tk.Canvas(flags_frame, width=70, height=70, bg="#F5F5F5", highlightthickness=1, highlightbackground="#D3D3D3")
            canvas.pack(side=tk.LEFT, padx=10)
            canvas.create_image(35, 20, image=flag_img, anchor=tk.CENTER)
            canvas.create_text(35, 60, text=lang, font=("Helvetica Neue", 12))
            canvas.image = flag_img
            canvas.bind("<Button-1>", lambda e, l=lang, c=canvas: on_flag_click(l, c))
            flag_canvases.append(canvas)

        print("Drapeaux ajoutés")

        ttk.Label(accueil, text="Bienvenue!", font=("Helvetica Neue", 14), background="#F5F5F5").pack(pady=(30, 20))

        style = ttk.Style()
        style.configure('Suivant.TButton', font=('Helvetica Neue', 12), foreground='white', background='#2E86C1')
        bouton_suivant = ttk.Button(accueil, text="Commencer", command=lambda: [accueil.destroy(), root.deiconify()], style='Suivant.TButton')
        bouton_suivant.pack(pady=(20, 0))
        print("Bouton Commencer ajouté")

        return language_var
    except Exception as e:
        print(f"Erreur dans afficher_accueil : {e}")
        return tk.StringVar(value="Espagnol")  # Valeur par défaut en cas d'erreur

def create_styled_gui(root, language_var, axes_du_programme):
    global titre_widgets, all_titles
    titre_widgets = []
    all_titles = load_titles()

    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    setup_styles()
    notebook = create_notebook(main_frame)
    principal_tab = create_principal_tab(notebook, language_var, axes_du_programme)
    widgets, last_row = create_widgets(principal_tab, language_var, axes_du_programme)

    widgets['reset_button']['command'] = lambda: reset_form(widgets)

    create_other_tabs(notebook, widgets)

    close_button = ttk.Button(main_frame, text="Fermer l'application", command=root.quit)
    close_button.pack(pady=10)

    return main_frame, widgets

def setup_styles():
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 12))
    style.configure("TCheckbutton", font=("Helvetica", 12), background="white")
    style.configure("TEntry", font=("Helvetica", 12))
    style.configure("TCombobox", font=("Helvetica", 12))

def create_notebook(parent):
    notebook = ttk.Notebook(parent)
    notebook.pack(fill=tk.BOTH, expand=True)
    return notebook

def create_principal_tab(notebook, language_var, axes_du_programme):
    principal_tab = ttk.Frame(notebook)
    notebook.add(principal_tab, text="Principal")

    for i in range(13):
        principal_tab.grid_rowconfigure(i, weight=1)
    principal_tab.grid_columnconfigure(1, weight=1)

    return principal_tab

def reset_form(widgets):
    # Réinitialiser tous les widgets
    widgets['titre_entry'].set('')
    widgets['nature_dropdown'].set('')
    widgets['comprehension_ecrit'].set(False)
    widgets['comprehension_oral'].set(False)
    widgets['expression_ecrite'].set(False)
    widgets['expression_orale'].set(False)
    widgets['axe_dropdown'].set('')
    widgets['objectifs_entry'].delete(0, tk.END)
    widgets['objectifs_dropdown'].set('')
    widgets['listbox_objectifs'].delete(0, tk.END)
    widgets['champ_lexical_entry'].delete(0, tk.END)
    widgets['trace_entry'].delete(0, tk.END)
    widgets['texte_final_text'].delete('1.0', tk.END)

def create_widgets(principal_tab, language_var, axes_du_programme):
    widgets = {}
    row = 0

    create_header(principal_tab, language_var, row)
    row += 2

    widgets.update(create_document_info(principal_tab, row))
    row += 2

    widgets.update(create_competences(principal_tab, row))
    row += 2

    widgets.update(create_axe_programme(principal_tab, axes_du_programme, row))
    row += 1

    widgets.update(create_objectifs_grammaticaux(principal_tab, language_var, row))
    row += 3

    widgets.update(create_champ_lexical(principal_tab, row))
    row += 1

    widgets.update(create_trace_ecrite(principal_tab, row))
    row += 1

    widgets.update(create_texte_final(principal_tab, row, widgets))
    row += 2

    # Ajout du bouton Reset
    reset_button = ttk.Button(principal_tab, text="Reset", command=lambda: reset_form(widgets))
    reset_button.grid(row=row, column=0, columnspan=2, pady=10)
    widgets['reset_button'] = reset_button

    return widgets, row

def create_header(parent, language_var, row):
    ttk.Label(parent, text="Cahier de textes", font=("Helvetica", 24, "bold")).grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
    ttk.Label(parent, text="Langue sélectionnée :").grid(row=row+1, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(parent, textvariable=language_var).grid(row=row+1, column=1, sticky="w", padx=5, pady=5)

def create_document_info(parent, row):
    global titre_widgets, all_titles
    
    parent.grid_columnconfigure(1, weight=1)

    ttk.Label(parent, text="Titre du/des document(s) :", font=("Helvetica", 12)).grid(
        column=0, row=row, sticky="w", pady=10, padx=(0, 10))
    titre_entry = ttk.Combobox(parent, font=("Helvetica", 12), values=all_titles)
    titre_entry.grid(column=1, row=row, sticky="ew", pady=10, padx=(0, 10))
    
    titre_widgets.append(titre_entry)

    def on_titre_added(event):
        nouveau_titre = titre_entry.get().strip()
        if nouveau_titre and nouveau_titre not in all_titles:
            save_title(nouveau_titre)
            all_titles.append(nouveau_titre)
            update_titre_listboxes(nouveau_titre)
    
    titre_entry.bind('<Return>', on_titre_added)
    titre_entry.bind('<KeyRelease>', lambda event: filter_titles(titre_entry))

    ttk.Label(parent, text="Nature du/des document(s) :", font=("Helvetica", 12)).grid(
        column=0, row=row+1, sticky="w", pady=10, padx=(0, 10))
    nature_dropdown = ttk.Combobox(parent, values=["Texte", "Document sonore", "Vidéo", "Document iconographique", "Double page"], font=("Helvetica", 12))
    nature_dropdown.grid(column=1, row=row+1, sticky="ew", pady=10, padx=(0, 10))

    return {'titre_entry': titre_entry, 'nature_dropdown': nature_dropdown}



def create_other_tabs(notebook, widgets):
    travail_a_faire_tab = ttk.Frame(notebook)
    notebook.add(travail_a_faire_tab, text="Travail à faire")
    widgets.update(create_travail_a_faire_tab(travail_a_faire_tab))

    bibliotheque_tab = ttk.Frame(notebook)
    notebook.add(bibliotheque_tab, text="Bibliothèque")
    bibliotheque_widgets = create_bibliotheque_tab(bibliotheque_tab)
    widgets.update(bibliotheque_widgets)
    titre_widgets.append(bibliotheque_widgets['titles_listbox'])


def filter_titles(entry):
    typed = entry.get().lower()
    filtered = [title for title in all_titles if typed in title.lower()]
    entry['values'] = filtered



def create_competences(parent, row):
    ttk.Label(parent, text="Compétence travaillée :", font=("Helvetica", 12)).grid(row=row, column=0, sticky="w", padx=5, pady=5)
    
    competence_frame = ttk.Frame(parent)
    competence_frame.grid(row=row, column=1, sticky="w", padx=5, pady=5)
    
    comprehension_ecrit = tk.BooleanVar()
    comprehension_oral = tk.BooleanVar()
    expression_ecrite = tk.BooleanVar()
    expression_orale = tk.BooleanVar()
    
    ttk.Checkbutton(competence_frame, text="Compréhension de l'écrit", variable=comprehension_ecrit).grid(row=0, column=0, sticky="w")
    ttk.Checkbutton(competence_frame, text="Compréhension de l'oral", variable=comprehension_oral).grid(row=0, column=1, sticky="w", padx=(20, 0))
    ttk.Checkbutton(competence_frame, text="Expression écrite", variable=expression_ecrite).grid(row=1, column=0, sticky="w")
    ttk.Checkbutton(competence_frame, text="Expression orale", variable=expression_orale).grid(row=1, column=1, sticky="w", padx=(20, 0))

    return {
        'comprehension_ecrit': comprehension_ecrit,
        'comprehension_oral': comprehension_oral,
        'expression_ecrite': expression_ecrite,
        'expression_orale': expression_orale
    }

def create_axe_programme(parent, axes_du_programme, row):
    parent.grid_columnconfigure(1, weight=1)
    ttk.Label(parent, text="Axe du programme :", font=("Helvetica", 12)).grid(
        column=0, row=row, sticky="w", pady=10, padx=(0, 10))
    axe_dropdown = ttk.Combobox(parent, values=axes_du_programme, font=("Helvetica", 12))
    axe_dropdown.grid(column=1, row=row, sticky="ew", pady=10, padx=(0, 10))
    return {'axe_dropdown': axe_dropdown}

def create_objectifs_grammaticaux(parent, language_var, row):
    global update_objectifs_grammaticaux_func
    
    parent.grid_columnconfigure(1, weight=1)

    ttk.Label(parent, text="Objectifs grammaticaux :", font=("Helvetica", 12)).grid(
        column=0, row=row, sticky="nw", pady=10, padx=(0, 10))
    
    objectifs_frame = ttk.Frame(parent)
    objectifs_frame.grid(column=1, row=row, sticky="ew", pady=10, padx=(0, 10))
    objectifs_frame.grid_columnconfigure(0, weight=1)
    
    objectifs_entry = ttk.Entry(objectifs_frame, font=("Helvetica", 12))
    objectifs_entry.grid(row=0, column=0, sticky="ew")
    
    objectifs_dropdown = ttk.Combobox(objectifs_frame, font=("Helvetica", 12))
    objectifs_dropdown.grid(row=0, column=1, sticky="ew", padx=(5, 0))
    objectif_widgets.append(objectifs_dropdown)
    
    listbox_objectifs = tk.Listbox(parent, selectmode=tk.MULTIPLE, height=5, font=("Helvetica", 12))
    listbox_objectifs.grid(column=1, row=row+1, sticky="nsew", pady=5, padx=(0, 10))
    parent.grid_rowconfigure(row+1, weight=1)

    all_objectifs = []
    objectifs_var = tk.StringVar()

    def local_update_objectifs_grammaticaux(*args):
        update_objectifs_grammaticaux(language_var, objectifs_dropdown, all_objectifs)

    update_objectifs_grammaticaux_func = local_update_objectifs_grammaticaux

    def filter_objectifs(*args):
        typed = objectifs_entry.get().lower()
        if typed:
            filtered = [obj for obj in all_objectifs if typed in obj.lower()]
            objectifs_dropdown['values'] = filtered
        else:
            objectifs_dropdown['values'] = all_objectifs

    objectifs_entry.bind('<KeyRelease>', filter_objectifs)
    objectifs_dropdown.bind('<<ComboboxSelected>>', lambda e: objectifs_entry.delete(0, tk.END) or objectifs_entry.insert(0, objectifs_dropdown.get()))

    def valider_objectif():
        objectif = objectifs_entry.get() or objectifs_dropdown.get()
        if objectif:
            if objectif not in listbox_objectifs.get(0, tk.END):
                listbox_objectifs.insert(tk.END, objectif)
                add_grammar_point(language_var.get(), objectif)
            objectifs_entry.delete(0, tk.END)
            objectifs_dropdown.set('')

    def effacer_objectif():
        selected = listbox_objectifs.curselection()
        for index in reversed(selected):
            listbox_objectifs.delete(index)

    button_frame = ttk.Frame(parent)
    button_frame.grid(column=1, row=row+2, sticky="e", pady=5, padx=(0, 10))

    ttk.Button(button_frame, text="Valider", command=valider_objectif).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(button_frame, text="Effacer", command=effacer_objectif).pack(side=tk.LEFT)

    local_update_objectifs_grammaticaux()
    language_var.trace_add("write", local_update_objectifs_grammaticaux)

    return {
        'objectifs_entry': objectifs_entry, 
        'objectifs_dropdown': objectifs_dropdown, 
        'listbox_objectifs': listbox_objectifs,
        'update_func': local_update_objectifs_grammaticaux
    }



def create_champ_lexical(parent, row):
    parent.grid_columnconfigure(1, weight=1)
    ttk.Label(parent, text="Champ lexical travaillé :", font=("Helvetica", 12)).grid(
        column=0, row=row, sticky="w", pady=10, padx=(0, 10))
    champ_lexical_entry = ttk.Entry(parent, font=("Helvetica", 12))
    champ_lexical_entry.grid(column=1, row=row, sticky="ew", pady=10, padx=(0, 10))
    return {'champ_lexical_entry': champ_lexical_entry}

def create_trace_ecrite(parent, row):
    parent.grid_columnconfigure(1, weight=1)
    ttk.Label(parent, text="Trace écrite :", font=("Helvetica", 12)).grid(
        column=0, row=row, sticky="w", pady=10, padx=(0, 10))
    trace_entry = ttk.Entry(parent, font=("Helvetica", 12))
    trace_entry.grid(column=1, row=row, sticky="ew", pady=10, padx=(0, 10))
    return {'trace_entry': trace_entry}


def create_document_info(parent, row):
    global update_objectifs_grammaticaux_func, titre_widgets
    
    parent.grid_columnconfigure(1, weight=1)

    ttk.Label(parent, text="Titre du/des document(s) :", font=("Helvetica", 12)).grid(
        column=0, row=row, sticky="w", pady=10, padx=(0, 10))
    titre_entry = ttk.Combobox(parent, font=("Helvetica", 12), values=load_titles())
    titre_entry.grid(column=1, row=row, sticky="ew", pady=10, padx=(0, 10))
    
    titre_widgets.append(titre_entry)

    def on_titre_added(event):
        nouveau_titre = titre_entry.get().strip()
        if nouveau_titre and nouveau_titre not in titre_entry['values']:
            save_title(nouveau_titre)
            values = list(titre_entry['values'])
            values.append(nouveau_titre)
            titre_entry['values'] = tuple(values)
            for widget in titre_widgets:
                if widget != titre_entry:
                    widget['values'] = titre_entry['values']
    
    titre_entry.bind('<Return>', on_titre_added)

    def filter_titles(*args):
        typed = titre_entry.get().lower()
        if typed:
            filtered = [title for title in load_titles() if typed in title.lower()]
            titre_entry['values'] = filtered
        else:
            titre_entry['values'] = load_titles()

    titre_entry.bind('<KeyRelease>', filter_titles)

    ttk.Label(parent, text="Nature du/des document(s) :", font=("Helvetica", 12)).grid(
        column=0, row=row+1, sticky="w", pady=10, padx=(0, 10))
    nature_dropdown = ttk.Combobox(parent, values=["Texte", "Document sonore", "Vidéo", "Document iconographique", "Double page"], font=("Helvetica", 12))
    nature_dropdown.grid(column=1, row=row+1, sticky="ew", pady=10, padx=(0, 10))

    def on_titre_selected(event):
        selected_titre = titre_entry.get()
        if update_objectifs_grammaticaux_func:
            update_objectifs_grammaticaux_func()

    titre_entry.bind('<<ComboboxSelected>>', on_titre_selected)

    return {'titre_entry': titre_entry, 'nature_dropdown': nature_dropdown}

# Dans gui.py
def create_texte_final(parent, row, widgets):
    frame = ttk.Frame(parent)
    frame.grid(row=row, column=0, columnspan=2, sticky="nsew", pady=10)
    parent.grid_rowconfigure(row, weight=1)

    ttk.Label(frame, text="Texte final :", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w")
    texte_final_text = tk.Text(frame, height=10, font=("Helvetica", 12), wrap=tk.WORD)
    texte_final_text.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=5)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    button_frame = ttk.Frame(frame)
    button_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

    generer_button = ttk.Button(button_frame, text="Générer Texte Final", command=lambda: generer_texte_final(texte_final_text, widgets))
    generer_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
    
    ttk.Button(button_frame, text="Copier", command=lambda: copier_texte(texte_final_text)).grid(row=0, column=1, sticky="ew", padx=(5, 0))

    return {'texte_final_text': texte_final_text, 'generer_button': generer_button}


def create_travail_a_faire_tab(parent):
    frame = ttk.Frame(parent, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Travail à faire :", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0, 5))
    
    travail_a_faire_text = tk.Text(frame, height=10, font=("Helvetica", 12), wrap=tk.WORD)
    travail_a_faire_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    ttk.Button(frame, text="Copier le travail à faire", command=lambda: copier_travail_a_faire(travail_a_faire_text)).pack(side=tk.LEFT)

    return {'travail_a_faire_text': travail_a_faire_text}

from tkinter import messagebox

def copier_travail_a_faire(travail_a_faire_text):
    travail = travail_a_faire_text.get("1.0", tk.END).strip()
    if travail:
        try:
            travail_a_faire_text.clipboard_clear()
            travail_a_faire_text.clipboard_append(travail)
            travail_a_faire_text.update()  # Nécessaire pour que le texte reste dans le presse-papiers
            messagebox.showinfo("Copié", "Le travail à faire a été copié dans le presse-papiers.")
        except tk.TclError:
            messagebox.showerror("Erreur", "Impossible de copier dans le presse-papiers. Veuillez réessayer.")
    else:
        messagebox.showwarning("Attention", "Aucun travail à faire n'a été saisi.")

def create_bibliotheque_tab(parent):
    global all_titles, all_grammar_points, titre_widgets, objectif_widgets
    frame = ttk.Frame(parent, padding="10")
    frame.grid(row=0, column=0, sticky="nsew")
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    frame.grid_columnconfigure(0, weight=1)

    # Titres de documents
    ttk.Label(frame, text="Titres de documents", font=("Helvetica", 14, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
    
    titles_frame = ttk.Frame(frame)
    titles_frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))
    titles_frame.grid_columnconfigure(0, weight=1)
    
    titles_entry = ttk.Entry(titles_frame, font=("Helvetica", 12))
    titles_entry.grid(row=0, column=0, sticky="ew")
    
    ttk.Button(titles_frame, text="Ajouter", command=lambda: ajouter_titre(titles_entry, titles_listbox, all_titles)).grid(row=0, column=1, padx=5)
    ttk.Button(titles_frame, text="Supprimer", command=lambda: supprimer_titre(titles_listbox, all_titles)).grid(row=0, column=2)

    titles_listbox = tk.Listbox(frame, height=5, font=("Helvetica", 12))
    titles_listbox.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
    frame.grid_rowconfigure(2, weight=1)
    
    all_titles = load_titles()
    titles_listbox.insert(tk.END, *all_titles)

    titre_widgets.append(titles_listbox)

    def filter_titles(*args):
        search_term = titles_entry.get().lower()
        titles_listbox.delete(0, tk.END)
        for title in all_titles:
            if search_term in title.lower():
                titles_listbox.insert(tk.END, title)

    titles_entry.bind('<KeyRelease>', lambda event: filter_titles(titles_entry, titles_listbox))

    # Ajout du bouton Rafraîchir pour les titres
    def refresh_titles():
        all_titles = load_titles()
        titles_listbox.delete(0, tk.END)
        titles_listbox.insert(tk.END, *all_titles)
        for widget in titre_widgets:
            if isinstance(widget, ttk.Combobox):
                widget['values'] = all_titles

    ttk.Button(frame, text="Rafraîchir les titres", command=refresh_titles).grid(row=3, column=0, sticky="w", pady=(0, 10))

    # Points grammaticaux
    ttk.Label(frame, text="Points grammaticaux", font=("Helvetica", 14, "bold")).grid(row=4, column=0, sticky="w", pady=(20, 5))
    
    grammar_frame = ttk.Frame(frame)
    grammar_frame.grid(row=5, column=0, sticky="ew", pady=(0, 5))
    grammar_frame.grid_columnconfigure(0, weight=1)
    
    grammar_entry = ttk.Entry(grammar_frame, font=("Helvetica", 12))
    grammar_entry.grid(row=0, column=0, sticky="ew")
    
    ttk.Button(grammar_frame, text="Ajouter", command=lambda: ajouter_point_grammatical(grammar_entry, grammar_listbox, all_grammar_points)).grid(row=0, column=1, padx=5)
    ttk.Button(grammar_frame, text="Supprimer", command=lambda: supprimer_point_grammatical(grammar_listbox, all_grammar_points)).grid(row=0, column=2)

    grammar_listbox = tk.Listbox(frame, height=5, font=("Helvetica", 12))
    grammar_listbox.grid(row=6, column=0, sticky="nsew", pady=(0, 10))
    frame.grid_rowconfigure(6, weight=1)
    
    all_grammar_points = get_grammar_points("Espagnol")  # Assurez-vous que la langue est correcte
    grammar_listbox.insert(tk.END, *all_grammar_points)

    objectif_widgets.append(grammar_listbox)

    def filter_grammar_points(*args):
        search_term = grammar_entry.get().lower()
        grammar_listbox.delete(0, tk.END)
        for point in all_grammar_points:
            if search_term in point.lower():
                grammar_listbox.insert(tk.END, point)

    grammar_entry.bind('<KeyRelease>', filter_grammar_points)

    # Ajout du bouton Rafraîchir pour les points grammaticaux
    def refresh_grammar_points():
        all_grammar_points = get_grammar_points("Espagnol")
        grammar_listbox.delete(0, tk.END)
        grammar_listbox.insert(tk.END, *all_grammar_points)
        for widget in objectif_widgets:
            if isinstance(widget, ttk.Combobox):
                widget['values'] = all_grammar_points

    ttk.Button(frame, text="Rafraîchir les points grammaticaux", command=refresh_grammar_points).grid(row=7, column=0, sticky="w", pady=(0, 10))

    return {'titles_entry': titles_entry, 'titles_listbox': titles_listbox, 
            'grammar_entry': grammar_entry, 'grammar_listbox': grammar_listbox}


def update_titre_listboxes(new_titre):
    global all_titles, titre_widgets
    
    if new_titre and new_titre not in all_titles:
        all_titles.append(new_titre)
        all_titles.sort()  # Trier la liste des titres
        
        for widget in titre_widgets:
            if isinstance(widget, tk.Listbox):
                widget.delete(0, tk.END)
                for titre in all_titles:
                    widget.insert(tk.END, titre)
            elif isinstance(widget, ttk.Combobox):
                values = list(widget['values'])
                if new_titre not in values:
                    values.append(new_titre)
                    values.sort()
                    widget['values'] = tuple(values)

    return all_titles  # Retourner la liste mise à jour

def update_grammar_listboxes(new_point):
    global all_grammar_points, grammar_listbox, objectifs_dropdown
    
    if new_point and new_point not in all_grammar_points:
        all_grammar_points.append(new_point)
    
        if grammar_listbox:
            grammar_listbox.insert(tk.END, new_point)
    
        if objectifs_dropdown:
            values = list(objectifs_dropdown['values'])
            values.append(new_point)
            objectifs_dropdown['values'] = tuple(set(values))  # Utiliser un set pour éliminer les doublons
    
        # Trier la liste des points grammaticaux
        all_grammar_points.sort()
        
        # Mettre à jour l'ordre dans la listbox si elle existe
        if grammar_listbox:
            grammar_listbox.delete(0, tk.END)
            for point in all_grammar_points:
                grammar_listbox.insert(tk.END, point)

    return all_grammar_points  # Retourner la liste mise à jour

def remove_from_titre_listboxes(titre):
    global all_titles, titles_listbox, titre_entry
    
    if titre in all_titles:
        all_titles.remove(titre)
    
        if titles_listbox:
            try:
                index = titles_listbox.get(0, tk.END).index(titre)
                titles_listbox.delete(index)
            except ValueError:
                print(f"Le titre '{titre}' n'a pas été trouvé dans la listbox.")
    
        if titre_entry:
            values = list(titre_entry['values'])
            if titre in values:
                values.remove(titre)
                titre_entry['values'] = tuple(values)  # Convertir en tuple pour la cohérence
    
        # Optionnel : mettre à jour l'ordre dans la listbox
        if titles_listbox:
            titles_listbox.delete(0, tk.END)
            for t in all_titles:
                titles_listbox.insert(tk.END, t)

    return all_titles  # Retourner la liste mise à jour

def remove_from_grammar_listboxes(point):
    global all_grammar_points, grammar_listbox, objectifs_dropdown
    
    if point in all_grammar_points:
        all_grammar_points.remove(point)
    
        if grammar_listbox:
            try:
                index = grammar_listbox.get(0, tk.END).index(point)
                grammar_listbox.delete(index)
            except ValueError:
                print(f"Le point grammatical '{point}' n'a pas été trouvé dans la listbox.")
    
        if objectifs_dropdown:
            values = list(objectifs_dropdown['values'])
            if point in values:
                values.remove(point)
                objectifs_dropdown['values'] = tuple(values)  # Convertir en tuple pour la cohérence
    
        # Optionnel : mettre à jour l'ordre dans la listbox
        if grammar_listbox:
            grammar_listbox.delete(0, tk.END)
            for p in all_grammar_points:
                grammar_listbox.insert(tk.END, p)

    return all_grammar_points  # Retourner la liste mise à jour