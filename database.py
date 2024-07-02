"""
database.py

Ce module gère les opérations de base de données pour l'application de langue "Cahier de textes portable".
Il utilise SQLite pour créer et gérer une base de données locale, stockant les informations sur les langues,
les points grammaticaux et les titres de documents.

Fonctions principales :

1. Initialisation et gestion de la base de données :
   - init_database : Initialise la base de données, crée les tables nécessaires et insère les données par défaut.
   - db_operation : Fonction utilitaire pour exécuter des opérations sur la base de données avec gestion des erreurs.

2. Gestion des points grammaticaux :
   - add_grammar_point : Ajoute un point grammatical à la base de données pour une langue donnée.
   - get_grammar_points : Récupère tous les points grammaticaux pour une langue donnée.
   - remove_grammar_point : Supprime un point grammatical de la base de données.

3. Gestion des titres de documents :
   - load_titles : Récupère tous les titres de documents de la base de données.
   - save_title : Enregistre un nouveau titre dans la base de données.
   - delete_title : Supprime un titre de la base de données.

Ce module est conçu pour être importé et utilisé par d'autres composants de l'application,
fournissant une interface entre l'application et la base de données SQLite.

La base de données contient trois tables principales :
- 'languages' : stocke les langues disponibles
- 'grammar_points' : stocke les points grammaticaux associés à chaque langue
- 'titles' : stocke les titres des documents

Note : La fonction get_grammar_points renvoie une liste par défaut de points grammaticaux
si aucun n'est trouvé dans la base de données pour la langue spécifiée.
"""


import sqlite3

def init_database():
    conn = sqlite3.connect('language_app.db')
    c = conn.cursor()

    try:
        # Création des tables
        c.execute('''CREATE TABLE IF NOT EXISTS languages
                     (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS grammar_points
                     (id INTEGER PRIMARY KEY, language_id INTEGER,
                     point TEXT NOT NULL,
                     FOREIGN KEY (language_id) REFERENCES languages(id))''')

       # Insertion des langues par défaut
        languages = ['Espagnol', 'Italien', 'Anglais', 'Allemand']
        for lang in languages:
            c.execute("INSERT OR IGNORE INTO languages (name) VALUES (?)", (lang,))

       
        # Nouvelle table pour les titres
        c.execute('''CREATE TABLE IF NOT EXISTS titles
                     (id INTEGER PRIMARY KEY, title TEXT UNIQUE NOT NULL)''')



        # Initialisation des points grammaticaux pour l'espagnol
        c.execute("SELECT id FROM languages WHERE name='Espagnol'")
        espagnol_id = c.fetchone()[0]

        points_grammaticaux = [
            "La phrase affirmative", "La phrase exclamative", "La phrase interrogative", "La phrase négative", "Les chiffres",
        "Le verbe être : ser ou estar", "Avoir : tener et haber", "Il y a : hay, está et hace", "L'apocope",
        "L'alphabet et les règles d'orthographes", "L'accent et la ponctuation", "L'accentuation", "Le genre des noms",
        "Le genre des adjectifs", "Le pluriel des noms", "Les noms composés", "L'article défini", "L'article indéfini",
        "L'article neutre : lo", "L'enclise", "Les auxiliaires : haber, ser et estar", "Exprimer l'accord et le désaccord",
        "Exprimer l'obligation (personnelle et impersonnelle)", "Exprimer l'habitude : soler", "Exprimer la quantité",
        "Exprimer l'insistance", "Exprimer le souhait et le regret", "Exprimer les goûts (avec gustar)", "Exprimer l'hypothèse",
        "Les tournures affectives", "L'impératif affirmatif", "L'impératif négatif", "La concordance des temps",
        "Les conjonctions (de coordination et de subordination)", "La date et l'heure", "Les comparatifs (de supériorité, infériorité et égalité)",
        "Les superlatifs", "Le style indirect", "Le sujet indéfini 'on'", "Les adjectifs indéfinis (Alguno, Ninguno, Cada, Mismo…)",
        "Les adjectifs démonstratifs", "Les adjectifs possessifs", "Les adjectifs qualificatifs", "Les adverbes d'affirmation, de négation et de doute",
        "Les adverbes de lieu", "Les adverbes de manière", "Les adverbes de quantité", "Les adverbes de temps",
        "Diphtongues et modifications orthographiques sur les consonnes et voyelles", "Diphtongaison et modifications orthographiques",
        "Les nombres cardinaux", "Les nombres ordinaux et les calculs", "Les prépositions", "Les pronoms démonstratifs",
        "Les pronoms indéfinis", "Les pronoms interrogatifs", "Les pronoms personnels compléments", "Les pronoms personnels sujets",
        "Les pronoms possessifs", "Les pronoms réfléchis", "Les pronoms relatifs", "Préfixes et suffixes en espagnol",
        "Qué ou cuál?", "Por ou para ?", "Les diminutifs", "Bien, bueno ou buen ?", "Por qué, porque, por que et porqué : quelle différence ?",
        "Tú ou Usted (tutoiement et vouvoiement)", "También ou Tampoco ?", "Pedir ou Preguntar ?", "Tomar, llevar ou Traer",
        "La substantivation de l'infinitif (el+ infinitif)", "L'expression de la simultanéité (mientras, gérondif, al+ infinitif)",
        "L'aspect de l'action", "Ser ou estar?", "L'obligation personnelle et l'obligation impersonnelle", "Le présent de l'indicatif (verbes réguliers)",
        "Le présent de l'indicatif (verbes en -acer, -ecer, -ocer, -ucir)", "Le présent de l'indicatif (verbes en -go)",
        "Le présent de l'indicatif : verbes à diphtongue", "Le présent de l'indicatif : verbes à affaiblissement",
        "Le présent de l'indicatif : verbes irréguliers", "Les verbes pronominaux", "Le gérondif", "L'impératif affirmatif",
        "L'impératif négatif", "Le participe passé", "La forme progressive", "La tournure affective : gustar", "Le futur simple",
        "Le futur proche", "Le conditionnel", "Le passé composé", "Le plus que parfait", "L'imparfait de l'indicatif",
        "Le passé simple", "Le passé simple : formation", "Alternance du passé simple et de l'imparfait", "Le subjonctif présent : formation",
        "Le subjonctif après les verbes de volonté et de souhait", "Le subjonctif après : para que", "Le subjonctif après les verbes de pensée à la forme négative",
        "Le subjonctif après les verbes d'émotion", "Le subjonctif après : ser + adjectif + que", "Le subjonctif après : ojalá que",
        "Le subjonctif après : es una pena que et es una lástima que", "Le subjonctif après les verbes d'interdiction et de permission",
        "Le subjonctif après les verbes de prière", "Le subjonctif après les verbes de conseil", "Le subjonctif après : Cuando + éventualité future",
        "Le subjonctif après : puede que ou es posible que ou similaires", "Le subjonctif après le verbe Esperar", "Le subjonctif imparfait pour exprimer l'hypothèse",
        "Le subjonctif imparfait après : como si", "L'expression de l'hypothèse", "La préposition A devant COD", "La préposition A après les verbes de mouvement",
        "La préposition EN", "La préposition DE", "La traduction de « on »", "Les traductions de \"devenir\"", "Les prépositions",
        "Les comparatifs et les superlatifs", "Les comparatifs.", "Le comparatif d'égalité.", "Le comparatif de supériorité.",
        "Le comparatif d'infériorité.", "Les superlatifs..", "Le superlatif relatif.", "Le superlatif absolu.", "La voix passive.",
        "La traduction de \"dont\""
        ]

        for point in points_grammaticaux:
            c.execute("INSERT OR IGNORE INTO grammar_points (language_id, point) VALUES (?, ?)", (espagnol_id, point))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Une erreur est survenue : {e}")
        conn.rollback()
    finally:
        conn.close()

def db_operation(operation):
    conn = sqlite3.connect('language_app.db')
    c = conn.cursor()
    try:
        result = operation(c)
        conn.commit()
        return result
    except sqlite3.Error as e:
        print(f"Une erreur est survenue : {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def add_grammar_point(language, point):
    conn = sqlite3.connect('language_app.db')
    c = conn.cursor()
    try:
        c.execute("SELECT id FROM languages WHERE name=?", (language,))
        lang_id = c.fetchone()[0]
        c.execute("INSERT INTO grammar_points (language_id, point) VALUES (?, ?)", (lang_id, point))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Une erreur est survenue : {e}")
        conn.rollback()
    finally:
        conn.close()


def get_grammar_points(language):
    conn = sqlite3.connect('language_app.db')
    c = conn.cursor()
    try:
        c.execute("""SELECT point FROM grammar_points
                     JOIN languages ON grammar_points.language_id = languages.id
                     WHERE languages.name=?""", (language,))
        points = [row[0] for row in c.fetchall()]
        if not points:
            # Liste par défaut si aucun point n'est trouvé
            points = [
                "Le présent de l'indicatif", "Le passé composé", "L'imparfait",
                "Le futur simple", "Le conditionnel présent", "Le subjonctif présent",
                "Les articles définis et indéfinis", "Les adjectifs qualificatifs",
                "Les pronoms personnels", "La négation", "L'interrogation"
            ]
        return points
    except sqlite3.Error as e:
        print(f"Une erreur est survenue : {e}")
        return []
    finally:
        conn.close()

def remove_grammar_point(language, point):
    conn = sqlite3.connect('language_app.db')
    c = conn.cursor()
    try:
        c.execute("""DELETE FROM grammar_points 
                     WHERE language_id = (SELECT id FROM languages WHERE name=?) 
                     AND point=?""", (language, point))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Une erreur est survenue : {e}")
        conn.rollback()
    finally:
        conn.close()

def load_titles():
    conn = sqlite3.connect('language_app.db')
    c = conn.cursor()
    try:
        c.execute("SELECT title FROM titles")
        titles = [row[0] for row in c.fetchall()]
        return titles
    except sqlite3.Error as e:
        print(f"Une erreur est survenue : {e}")
        return []
    finally:
        conn.close()

def save_title(title):
    db_operation(lambda c: c.execute("INSERT OR IGNORE INTO titles (title) VALUES (?)", (title,)))

def delete_title(title):
    conn = sqlite3.connect('language_app.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM titles WHERE title=?", (title,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Une erreur est survenue : {e}")
        conn.rollback()
    finally:
        conn.close()

