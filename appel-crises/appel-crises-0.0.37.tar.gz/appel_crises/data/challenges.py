from typing import Dict, List, Tuple

# ONLY APPEND to this list, or it might break ongoing challenges
CHALLENGES: List[Tuple[str, Tuple[str]]] = [
    ("Combien a-t-on de doigts dans une main ?", ("5", "cinq")),
    ("1 + 1 ?", ("2",)),
    ("Combien avons-nous de narines ?", ("2",)),
    ("Combien de côtés a un triangle ?", ("3",)),
    ("Combien sont les 101 Dalmatiens ? (Pas de piège)", ("101",)),
    ("Quelle est la couleur du cheval blanc ?", ("blanc",)),
    ("Quelle est l'inverse du noir ?", ("blanc", "le blanc")),
    (
        "Quel est le prénom d'un canard et du président actuel des Etats-Unis ?",
        ("Donald",),
    ),
    ("Quel est le nom de famille de Marie Dupont ?", ("dupont",)),
    ("Quel est le premier mois de l'année ?", ("janvier",)),
    ("De quelle couleur sont les Simpson ?", ("jaune",)),
    (
        "Qui est arrivé en DERNIER, (la poule ou l'œuf de tyrannosaure ?",
        ("la poule", "poule"),
    ),
    ("Quel est le premier jour de la semaine ?", ("lundi", "le lundi")),
    (
        "De quoi sont faites les boules de neige ? (pas de déterminant!)",
        ("neige", "de neige"),
    ),
    (
        "Quel fruit a le même nom que la couleur de cheveux de Donald Trump ?",
        ("orange",),
    ),
    ("Quelle est la capitale de la France ?", ("paris",)),
    ("Je parle, (tu parles, (il parle, (nous ... ?", ("parlons", "nous parlons")),
    (
        "Pierre et Paul sont dans un bateau, (Pierre tombe à l'eau, (qui reste-t-il ?",
        ("paul",),
    ),
    (
        "Quel est l'ingrédient principal de la compote de pomme ? (pas de pluriel!)",
        ("pomme",),
    ),
    (
        "Quel doigt de la main n'est pas dans le même sens que les autres ?",
        ("pouce", "le pouce"),
    ),
    ("Ceci est un appel commun à la ?", ("reconstruction", "la reconstruction")),
    ("De quoi sont faits les châteaux de sable ?", ("sable", "de sable")),
    ("Quel super-héros ressemble à une araignée ?", ("spiderman",)),
    ("Quel est ton Disney préféré ? (la réponse est : tous)", ("tous",)),
    ("Le pissenlit est-il UNE FLEUR  ou UN PORTE-AVIONS ?", ("une fleur", "fleur")),
    ("Quel animal fait meuh ?", ("vache", "la vache", "une vache")),
    ("Qui est le héros des livres Harry Potter ?", ("Harry Potter",)),
    ("Qui est l'héroïne du film Marry Poppins ?", ("Marry Poppins",)),
    ("De quelle couleur est le ciel quand il fait beau ?", ("bleu",)),
    (
        "A quoi sert une aiguille à coudre ? (juste le verbe!)",
        ("coudre", "à coudre", "a coudre"),
    ),
    (
        "A quoi sert un fer à souder ? (juste le verbe!)",
        ("souder", "à souder", "souder"),
    ),
    (
        "A quoi sert un fer à repasser ? (juste le verbe!)",
        ("repasser", "à repasser", "a repasser"),
    ),
    (
        "Quel instrument célèbre possède de nombreuses de touches blanches et noires ?",
        ("piano",),
    ),
    ("Citez un légume orange et pointu que les lapins aiment beaucoup", ("carotte",)),
    ("Citez un fruit jaune et long que les singes aiment beaucoup", ("banane",)),
    ("Quel outil sert à scier ?", ("scie", "une scie", "la scie")),
    ("Quel outil sert à visser ?", ("tournevis", "le tournevis", "un tournevis")),
    (
        "Lequel de ces animaux a un long bec : le CHIEN ou le CANARD ?",
        ("canard", "le canard"),
    ),
    ("Comment s'appelle le pays où vivent le plus de Chinois ?", ("chine", "la chine")),
    (
        "Quel couvert de table ressemble à une petite fourche ?",
        ("fourchette", "la fourchette", "une fourchette"),
    ),
    (
        "D'après quel écrivain est nommée la rue Victor Hugo à Béziers ?",
        ("victor hugo", "hugo"),
    ),
    (
        "Quel fruit jaune-orangé à la peau rugueuse est appelé ananas en italien ?",
        ("ananas", "l'ananas"),
    ),
    ("Complétez : \"l'habit ne fait pas le … \"", ("moine", "le moine")),
    ("Combien de pattes a un chat ? (normalement)", ("4", "quatre")),
    ("Quel sac met-on sur son dos ?", ("sac à dos", "un sac à dos", "un sac a dos")),
    ("Qu'essore-t-on dans un panier à salade ?", ("salade", "une salade")),
    ("Complétez avec un nom de charcuterie: \"oh hisse, (la …\"", ("saucisse",)),
    ("Quel est le pluriel de \"pingouin\" ?", ("pingouins",)),
    ("Quel est le pluriel de \"alouette\" ?", ("hérissons",)),
    ("Quel est le pluriel de \"brique\" ?", ("briques",)),
]

CHALLENGES_WITH_ID = [
    (ix, question, answers) for ix, (question, answers) in enumerate(CHALLENGES)
]

ANSWERS: Dict[int, List[str]] = {
    id_: [a.lower().strip() for a in answers]
    for id_, (_, answers) in enumerate(CHALLENGES)
}
