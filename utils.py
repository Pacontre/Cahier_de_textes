"""
utils.py

Ce module contient des fonctions utilitaires pour l'application "Cahier de textes portable".
Il gère diverses tâches liées à l'interface utilisateur et à la manipulation des données.

Fonctions principales :

1. Gestion des titres et suggestions :
   - update_title_suggestions : Met à jour les suggestions de titres dans une liste déroulante.
   - ajouter_titre : Ajoute un nouveau titre à la liste et à la base de données.
   - supprimer_titre : Supprime un titre sélectionné de la liste et de la base de données.
   - update_titre_listboxes : Met à jour les listes de titres dans l'interface graphique.

2. Gestion des objectifs grammaticaux :
   - recherche_objectifs : Filtre les objectifs grammaticaux selon l'entrée utilisateur.
   - valider_objectif : Ajoute un nouvel objectif à la liste et à la base de données.
   - update_objectifs_dropdown : Met à jour la liste déroulante des objectifs selon la langue.
   - ajouter_point_grammatical : Ajoute un nouveau point grammatical à la liste et à la base de données.
   - supprimer_point_grammatical : Supprime un point grammatical sélectionné.

3. Manipulation de texte :
   - generer_texte_final : Génère un texte final à partir des entrées utilisateur.
   - copier_texte : Copie le texte d'un widget dans le presse-papiers.
   - generer_trace_ecrite : Génère une trace écrite à partir du travail à faire.
   - copier_travail_a_faire : Copie le texte du travail à faire dans le presse-papiers.

4. Autres utilitaires :
   - nettoyer_liste : Efface tous les éléments d'une liste.
   - on_window_resize : Gère le redimensionnement de la fenêtre (actuellement vide).

Ce module est conçu pour être importé et utilisé par les autres composants de l'application,
notamment pour la gestion de l'interface utilisateur et l'interaction avec la base de données.
"""

import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from database import remove_grammar_point, delete_title, save_title, load_titles, add_grammar_point, get_grammar_points

titre_widgets = []
objectif_widgets = []

def update_title_suggestions(titre_entry, titles):
    def inner_update(*args):
        typed = titre_entry.get().lower()
        if typed:
            suggestions = [title for title in titles if typed in title.lower()]
            titre_entry['values'] = suggestions
    return inner_update

def recherche_objectifs(event, dropdown, entry, language_var):
    typed = entry.get().lower()
    all_points = get_grammar_points(language_var.get())
    
    if typed:
        matching_points = [point for point in all_points if typed in point.lower()]
        dropdown['values'] = matching_points
    else:
        dropdown['values'] = all_points
    
    # Si aucun point ne correspond, laissez la possibilité d'ajouter un nouveau point
    if not dropdown['values'] and typed:
        dropdown['values'] = [f"Ajouter : {typed}"]

def valider_objectif(entry, listbox, dropdown, language_var):
    objectif = entry.get()
    if objectif.startswith("Ajouter : "):
        objectif = objectif[9:]  # Enlever le préfixe "Ajouter : "
    
    if objectif and objectif not in listbox.get(0, tk.END):
        listbox.insert(tk.END, objectif)
        if objectif not in get_grammar_points(language_var.get()):
            add_grammar_point(language_var.get(), objectif)
    
    entry.delete(0, tk.END)
    dropdown.set('')  # Réinitialiser le dropdown
    recherche_objectifs(None, dropdown, entry, language_var)  # Mettre à jour le dropdown

def nettoyer_liste(listbox):
    listbox.delete(0, tk.END)

def generer_texte_final(texte_final_text, widgets):
    nouveau_titre = widgets['titre_entry'].get()
    if nouveau_titre:
        save_title(nouveau_titre)
        if nouveau_titre:
            update_titre_listboxes(nouveau_titre)

    competences = []
    if widgets['comprehension_ecrit'].get():
        competences.append("Compréhension de l'écrit")
    if widgets['comprehension_oral'].get():
        competences.append("Compréhension de l'oral")
    if widgets['expression_ecrite'].get():
        competences.append("Expression écrite")
    if widgets['expression_orale'].get():
        competences.append("Expression orale")

    objectifs_valides = list(widgets['listbox_objectifs'].get(0, tk.END))

    texte_final = (
        f"Titre du/des document(s) : {widgets['titre_entry'].get()}\n"
        f"Nature du/des document(s) : {widgets['nature_dropdown'].get()}\n"
        f"Compétence travaillée : {', '.join(competences)}\n"
        f"Axe du programme : {widgets['axe_dropdown'].get()}\n"
        f"Objectifs grammaticaux : {', '.join(objectifs_valides)}\n"
        f"Champ lexical travaillé : {widgets['champ_lexical_entry'].get()}\n"
        f"Trace écrite : {widgets['trace_entry'].get()}"
    )
    texte_final_text.delete("1.0", tk.END)
    texte_final_text.insert(tk.END, texte_final)

def copier_texte(texte_final_text):
    texte = texte_final_text.get('1.0', tk.END)
    texte_final_text.clipboard_clear()
    texte_final_text.clipboard_append(texte)
    texte_final_text.update() 

def on_window_resize(event):
    # Implémentez ici la logique de redimensionnement si nécessaire
    pass

def update_objectifs_dropdown(language_var, objectifs_dropdown, listbox_objectifs):
    points = get_grammar_points(language_var.get())
    objectifs_dropdown['values'] = points
    listbox_objectifs.delete(0, tk.END)
    for point in points:
        listbox_objectifs.insert(tk.END, point)

def generer_trace_ecrite(travail_a_faire_entry, trace_ecrite_text):
    travail = travail_a_faire_entry.get()
    trace = f"Travail à faire : {travail}\n\nTrace écrite générée ici."
    trace_ecrite_text.delete("1.0", tk.END)
    trace_ecrite_text.insert(tk.END, trace)

def ajouter_titre(entry, listbox, all_titles):
    global titre_widgets
    nouveau_titre = entry.get().strip()
    if nouveau_titre and nouveau_titre not in all_titles:
        save_title(nouveau_titre)
        all_titles.append(nouveau_titre)
        listbox.insert(tk.END, nouveau_titre)
        entry.delete(0, tk.END)
        
        # Mettre à jour toutes les Combobox et Listbox de titres
        for widget in titre_widgets:
            if isinstance(widget, ttk.Combobox):
                values = list(widget['values'])
                if nouveau_titre not in values:
                    values.append(nouveau_titre)
                    widget['values'] = tuple(values)
            elif isinstance(widget, tk.Listbox):
                if nouveau_titre not in widget.get(0, tk.END):
                    widget.insert(tk.END, nouveau_titre)
    elif nouveau_titre in all_titles:
        messagebox.showwarning("Attention", "Ce titre existe déjà.")
    else:
        messagebox.showwarning("Attention", "Veuillez entrer un titre.")


def supprimer_titre(listbox, all_titles):
    global titre_widgets
    selection = listbox.curselection()
    if selection:
        titre = listbox.get(selection[0])
        confirm = messagebox.askyesno("Confirmer la suppression", f"Êtes-vous sûr de vouloir supprimer le titre '{titre}' ?")
        if confirm:
            listbox.delete(selection[0])
            delete_title(titre)
            all_titles.remove(titre)
            
            # Mettre à jour toutes les Combobox et Listbox de titres
            for widget in titre_widgets:
                if isinstance(widget, ttk.Combobox):
                    values = list(widget['values'])
                    if titre in values:
                        values.remove(titre)
                        widget['values'] = tuple(values)
                elif isinstance(widget, tk.Listbox):
                    items = list(widget.get(0, tk.END))
                    if titre in items:
                        index = items.index(titre)
                        widget.delete(index)
            
            messagebox.showinfo("Suppression réussie", f"Le titre '{titre}' a été supprimé.")
    else:
        messagebox.showwarning("Attention", "Veuillez sélectionner un titre à supprimer.")

def update_titre_listboxes(new_titre):
    global titre_widgets
    all_titles = load_titles()
    
    if new_titre and new_titre not in all_titles:
        all_titles.append(new_titre)
        all_titles.sort()
        
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

    save_title(new_titre)  # Assurez-vous que cette fonction existe dans votre module de base de données
    return all_titles

def ajouter_point_grammatical(entry, listbox, all_grammar_points):
    nouveau_point = entry.get().strip()
    if nouveau_point and nouveau_point not in all_grammar_points:
        add_grammar_point("Espagnol", nouveau_point)
        all_grammar_points.append(nouveau_point)
        listbox.insert(tk.END, nouveau_point)
        entry.delete(0, tk.END)
        
        # Mettre à jour toutes les Combobox d'objectifs grammaticaux
        for widget in objectif_widgets:
            values = list(widget['values'])
            values.append(nouveau_point)
            widget['values'] = values
    elif nouveau_point in all_grammar_points:
        messagebox.showwarning("Attention", "Ce point grammatical existe déjà.")
    else:
        messagebox.showwarning("Attention", "Veuillez entrer un point grammatical.")

def supprimer_point_grammatical(listbox, all_grammar_points):
    selection = listbox.curselection()
    if selection:
        point = listbox.get(selection[0])
        confirm = messagebox.askyesno("Confirmer la suppression", f"Êtes-vous sûr de vouloir supprimer le point grammatical '{point}' ?")
        if confirm:
            listbox.delete(selection[0])
            remove_grammar_point("Espagnol", point)  # Assurez-vous que la langue est correcte
            messagebox.showinfo("Suppression réussie", f"Le point grammatical '{point}' a été supprimé.")
    else:
        messagebox.showwarning("Attention", "Veuillez sélectionner un point grammatical à supprimer.")

def copier_travail_a_faire(travail_a_faire_text):
    travail = travail_a_faire_text.get("1.0", tk.END).strip()
    if travail:
        travail_a_faire_text.clipboard_clear()
        travail_a_faire_text.clipboard_append(travail)
        travail_a_faire_text.update()  # Nécessaire pour que le texte reste dans le presse-papiers
        messagebox.showinfo("Copié", "Le travail à faire a été copié dans le presse-papiers.")
    else:
        messagebox.showwarning("Attention", "Aucun travail à faire n'a été saisi.")