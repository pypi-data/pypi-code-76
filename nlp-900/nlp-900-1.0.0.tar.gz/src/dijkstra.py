"""chemin le plus court"""
import io
import pkgutil

from src.utils import searchGareInSentence


def createGraph(file=None):
    """
    Transforme un csv en graphe pondéré.

    :param str file: le nom du fichier.
    :return: (Graphe pondéré, list des sommets)
    :rtype: (dict, list)
    """
    grapheGare = dict()
    sommet = list()
    data = pkgutil.get_data(__name__, file).decode()
    with io.StringIO(data) as file:
        for line in file:
            if "trip_id,trajet,duree" in line:
                continue
            lsplit = line.lower().replace("\n", "").split(",")
            gare = lsplit[1].split(" - ")
            startGare = searchGareInSentence(gare[0])
            finishGare = searchGareInSentence(gare[1])
            sommet.append(startGare)
            sommet.append(finishGare)
            if startGare in grapheGare.keys():
                grapheGare[startGare][finishGare] = int(lsplit[2])
            else:
                grapheGare[startGare] = dict()
                grapheGare[startGare][finishGare] = int(lsplit[2])
    file.close()
    return grapheGare, list(dict.fromkeys(sommet))


def shortTime(graphe, etape, finish, visites, d, father, start):
    """
    Calcule le temps le plus courts entre deux sommets.Renvoie le chemin et le temps.

    :param dict graphe: le graphe pondéré.
    :param str etape:
    :param str finish: étape de fin.
    :param visites:
    :param dict d: distance dict
    :param dict father: sommets père.
    :param str start: étape de début
    :return: La list des sommets et le temps
    :rtype: (list, int)
    """
    if etape == finish:
        return (
            shortFather(father, start, finish, []),
            d[finish] if finish in d.keys() else float("inf"),
        )
    if len(visites) == 0:
        d[etape] = 0
    for neighbour in graphe[etape]:
        if neighbour not in visites:
            if neighbour not in d.keys():
                dNeighbour = float("inf")
            else:
                dNeighbour = d[neighbour]
            if etape not in d.keys():
                continue
            newDist = d[etape] + graphe[etape][neighbour]
            if newDist < dNeighbour:
                d[neighbour] = newDist
                father[neighbour] = etape
    visites.append(etape)
    noVisite = {s: d.get(s, float("inf")) for s in graphe if s not in visites}
    if noVisite == {}:
        return [], float("inf")
    noeud_plus_proche = min(noVisite, key=noVisite.get)
    return shortTime(
        graphe,
        noeud_plus_proche,
        finish,
        visites,
        d,
        father,
        start,
    )


def shortFather(father, start, finish, etape):
    """
    Plus court chemin des pères.

    :param dict father: graphe père
    :param str start: étape de départ
    :param str finish: étape de fin
    :param list etape: list des etape
    :return: list des étapes.
    :rtype: list
    """
    if finish == start:
        return [start] + etape
    else:
        if finish not in father.keys():
            return []
        return shortFather(father, start, father[finish], [finish] + etape)


def dijkstra(graphe, debut, fin):
    """
    Algo de dijkstra.

    :param dict graphe: le graphe pondéré
    :param str debut: étape de début
    :param str fin: étape de fin
    :return: la list des étape, le temps
    :rtype: (list, int)
    """
    fin = fin.lower()
    debut = debut.lower()
    if debut not in graphe.keys():
        return [], float("inf")
    if fin in graphe[debut]:
        return [debut, fin], graphe[debut][fin]
    return shortTime(graphe, debut, fin.lower(), list(), dict(), dict(), debut)


def bestDijkstra(grapheGare, listStart, listArrived):
    """
    Itère sur la list de départ et d'arrivé pour trouver le meilleur chemin.

    :param dict grapheGare:
    :param list listStart: list de point de départ
    :param list listArrived: list de point d'arrivé
    :return: list du chemin, le temps
    :rtype: (list, int)
    """
    bestTime = float("inf")
    lGare = list()
    for start in listStart:
        for arrived in listArrived:
            l, time = dijkstra(grapheGare, start, arrived)
            if time < bestTime:
                bestTime = time
                lGare = l
    return lGare, bestTime
