prompt = """
J'ai envie de découvrir de nouvelles chansons. J'aime des chansons comme As it was d'Harry Styles 
ou The Chain de Fleetwoods Mac. Trouve moi 30 morceaux (titre, artiste, album) pour ma playlist.
Je veux des morceaux plutôt récents et d'artistes différents.
Le résultat doit être UNIQUEMENT un fichier json avec le format:
[
    {
        "titre": "Shape of You",
        "artiste": "Ed Sheeran",
        "album": "÷ (Divide)"
    },
    {
        "titre": "Blinding Lights",
        "artiste": "The Weeknd",
        "album": "After Hours"
    },
    ...
]

"""