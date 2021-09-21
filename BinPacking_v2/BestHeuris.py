def bestHeuristique(famille, taille):
    if famille == "moyenne":
        return "Greedy1"
    else:
        return "Greedy3"


def bestAg(famille, taille):
    if famille == "difficile":
        return "AG Classique"
    else:
        return "AG Adaptatif"


def bestRS(famille, taille):
    return "Recuit simulé avec solution initiale avec Greedy"


def bestMeta(famille, taille):
    if famille == "facile":
        if taille == "petite" or taille == "grande":
            return "AG Adaptatif"
        else:
            return "RS avec solution initiale Greedy"
    if famille == "moyenne":
        return "RS avec solution initiale Greedy"
    if famille == "difficile":
        return "AG Classique"


def bestMethod(famille, taille):
    if famille == "facile":
        if taille == "petite":
            return "AG Adaptatif"
        else:
            return "Greedy3"
    if famille == "moyenne":
        return "Greedy1"
    if famille == "difficile":
        return "AG Classique"