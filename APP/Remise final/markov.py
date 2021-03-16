# coding=utf-8
###
###  Gabarit pour l'application de traitement des frequences de mots dans les oeuvres d'auteurs divers
###  Le traitement des arguments a ete inclus:
###     Tous les arguments requis sont presents et accessibles dans args
###     Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
###
###  Frederic Mailhot, 26 fevrier 2018
###    Revise 16 avril 2018
###    Revise 7 janvier 2020

###  Parametres utilises, leur fonction et code a generer
###
###  -d X  Deja traite dans le gabarit:  la variable rep_auth contiendra le chemin complet vers le repertoire d'auteurs
###       La liste d'auteurs est extraite de ce repertoire, et est comprise dans la variable authors
###
###  -P X Si utilise, indique au systeme d'utiliser la ponctuation.  Ce qui est considÃ©re comme un signe de ponctuation
###       est defini dans la liste PONC
###       Si -P EST utilise, cela indique qu'on dÃ©sire conserver la ponctuation (chaque signe est alors considere
###       comme un mot.  Par defaut, la ponctuation devrait etre retiree
###
###  -m X mode d'analyse:  -m 1 indique de faire les calculs avec des unigrammes, -m 2 avec des bigrammes.
###
###  -a X Auteur (unique a traiter).  Utile en combinaison avec -g, -G, pour la generation d'un texte aleatoire
###       avec les caracteristiques de l'auteur indique
###
###  -G   Indique qu'on veut generer un texte (voir -a ci-haut), le nombre de mots Ã  generer doit Ãªtre indique
###
###  -g   Indique qu'on veut generer un texte (voir -a ci-haut), le nom du fichier en sortie est indique
###
###  -F X Indique qu'on desire connaitre le rang d'un certain mot pour un certain auteur.  L'auteur doit etre
###       donnÃ© avec le parametre -a, et un mot doit suivre -F:   par exemple:   -a Verne -F Cyrus
###
###  -v   Deja traite dans le gabarit:  mode "verbose",  va imprimer les valeurs donnÃ©es en parametre
###
###
###  Le systeme doit toujours traiter l'ensemble des oeuvres de l'ensemble des auteurs.  Selon la presence et la valeur
###  des autres parametres, le systeme produira differentes sorties:
###
###  avec -a, -g, -G:  generation d'un texte aleatoire avec les caracteristiques de l'auteur identifie
###  avec -a, -F:  imprimer la frequence d'un mot d'un certain auteur.  Format de sortie:  "auteur:  mot  frequence"
###                la frequence doit Ãªtre un nombre reel entre 0 et 1, qui represente la probabilite de ce mot
###                pour cet auteur
###  avec -f:  indiquer l'auteur le plus probable du texte identifie par le nom de fichier qui suit -f
###            Format de sortie:  "nom du fichier: auteur"
###  avec ou sans -P:  indique que les calculs doivent etre faits avec ou sans ponctuation
###  avec -v:  mode verbose, imprimera l'ensemble des valeurs des paramÃ¨tres (fait deja partie du gabarit)
# -d D:\Simon\Desktop\Repo\S2_APP5\APP\TextesPourEtudiants -m 2 -g allo -G 10

#
# Ce code à été réalisé par Benjamin Gélinas(gelb2602) et Simon Leroux(lers0601)
# le 17 mars 2021
# Tutorat T3 et T2 respectivement
#

import math
import argparse
import glob
import sys
import os
import numpy
from pathlib import Path
from random import randint
from random import choice

### Ajouter ici les signes de ponctuation Ã  retirer
PONC = ["!", '"', "'", ")", "(", ",", ".", ";", ":", "?", "-", "_"]


###  Vous devriez inclure vos classes et mÃ©thodes ici, qui seront appellÃ©es Ã  partir du main
def dico_maker(texte, dico):
    dictionnairetemp = dico
    if not args.P:
        for i in range(len(PONC)):
            texte = texte.replace(PONC[i], " ")
    texte = texte.lower().split()
    gram = []
    if args.m == 1:
        for i in range(len(texte)):
            word = texte[i]
            if len(word) > 2:
                gram.append(word)
    else:
        i = 0
        while len(texte[i]) < 3:
            i += 1
        while i < len(texte):
            j = i
            if i + 1 != len(texte):
                while j + 1 != len(texte) and len(texte[j + 1]) < 3:
                    j += 1
                if j + 1 != len(texte):
                    gram.append((texte[i], texte[j + 1]))
            i = j
            i += 1
    for i in range(len(gram)):
        mot = gram[i]
        if mot not in dictionnairetemp:
            dictionnairetemp[mot] = 0
        dictionnairetemp[mot] += 1
    return dictionnairetemp


def sort(dictionnaires):
    return sorted(list(dictionnaires.items()), key=lambda x: x[1], reverse=True)


def calculDefrequence(rangeauteur, liste, i):
    freq = [[] for nombre in rangeauteur]
    for auteur in rangeauteur:
        for motEnCommun in range(len(liste[auteur])):
            freq[auteur].append(liste[auteur][motEnCommun][i])
        freq[auteur] = sum(freq[auteur])
    return freq


def ChaineDeMarkov(listeDeDicos):
    liste = [[] for auteur in range(len(listeDeDico))]
    for auteur in range(len(listeDeDicos)):
        chaineDeMarkov = []
        for bigramme in range(len(listeDeDicos[auteur])):
            motComparer, freq = listeDeDicos[auteur][bigramme]
            motComparer, suivant = motComparer
            if mot[auteur] == motComparer:
                chaineDeMarkov.append((suivant, freq))
        liste[auteur] += chaineDeMarkov
    return liste


### Main: lecture des paramÃ¨tres et appel des mÃ©thodes appropriÃ©es
###
###       argparse permet de lire les paramÃ¨tres sur la ligne de commande
###             Certains paramÃ¨tres sont obligatoires ("required=True")
###             Ces paramÃ¨tres doivent Ãªtres fournis Ã  python lorsque l'application est exÃ©cutÃ©e
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='markov_cip1_cip2.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', required=True, type=int, choices=range(1, 3),
                        help='Mode (1 ou 2) - unigrammes ou digrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    parser.add_argument('-A', action='store_true', help='Tout les auteurs')
    args = parser.parse_args()

    ### Lecture du rÃ©pertoire des auteurs, obtenir la liste des auteurs
    ### Note:  args.d est obligatoire
    ### auteurs devrait comprendre la liste des rÃ©pertoires d'auteurs, peu importe le systÃ¨me d'exploitation
    cwd = os.getcwd()
    if os.path.isabs(args.d):
        rep_aut = args.d
    else:
        rep_aut = os.path.join(cwd, args.d)

    rep_aut = os.path.normpath(rep_aut)
    authors = os.listdir(rep_aut)

    ### Enlever les signes de ponctuation (ou non) - DÃ©finis dans la liste PONC
    if args.P:
        remove_ponc = True
    else:
        remove_ponc = False

    ### Si mode verbose, reflÃ©ter les valeurs des paramÃ¨tres passÃ©s sur la ligne de commande
    if args.v:
        print("Mode verbose:")
        print("Calcul avec les auteurs du repertoire: " + args.d)
        if args.f:
            print("Fichier inconnu a,"
                  " etudier: " + args.f)

        print("Calcul avec des " + str(args.m) + "-grammes")
        if args.F:
            print(str(args.F) + "e mot (ou digramme) le plus frequent sera calcule")

        if args.a:
            print("Auteur etudie: " + args.a)

        if args.P:
            print("Retirer les signes de ponctuation suivants: {0}".format(" ".join(str(i) for i in PONC)))

        if args.G:
            print("Generation d'un texte de " + str(args.G) + " mots")

        if args.g:
            print("Nom de base du fichier de texte genere: " + args.g)

        print("Repertoire des auteurs: " + rep_aut)
        print("Liste des auteurs: ")
        for a in authors:
            aut = a.split("/")
            print("    " + aut[-1])
    ### Ã€ partir d'ici, vous devriez inclure les appels Ã  votre code

    listeDeDico = []
    if args.a:
        lsdir = os.listdir(rep_aut + '/' + args.a)
        dictionnaire = {}
        for j in range(len(lsdir)):
            f = open(rep_aut + '/' + args.a + '/' + lsdir[j], "r", encoding="utf8")
            texte = f.read().lower()
            dictionnaire = dico_maker(texte, dictionnaire)
            f.close()
        listeDeDico.append(sort(dictionnaire))
        if args.F:
            print(listeDeDico[0][args.F - 1])
    else:
        for i in range(len(authors)):
            lsdir = os.listdir(rep_aut + '/' + authors[i])
            dictionnaire = {}
            for j in range(len(lsdir)):
                f = open(rep_aut + '/' + authors[i] + '/' + lsdir[j], "r", encoding="utf8")
                texte = f.read().lower()
                dictionnaire = dico_maker(texte, dictionnaire)
                f.close()
            listeDeDico.append(sort(dictionnaire))
        if args.F:
            for authors in range(len(listeDeDico)):
                print(listeDeDico[authors][args.F - 1])

    # Bloc de code pour la comparaison avec un texte inconnu
    if args.f:
        # Declaration des variables
        listeTexteInconnu = []
        dictionnaireInconnu = {}
        longeurduDico=range(len(listeDeDico))
        listeDeProbabilite = [[] for auteur in longeurduDico]
        FreqAuteur = [[] for nombre in longeurduDico]
        FreqAuteurInconnu = [[] for nombre in longeurduDico]
        sommeCarre = [[] for nombre in longeurduDico]
        listeDeMotCommun = [[] for auteur in longeurduDico]

        f = open(args.f, encoding="utf8")
        texte = f.read().lower()
        dictionnaireInconnu = dico_maker(texte, dictionnaireInconnu)
        f.close()

        # Le bout de code suivant passe a traver tout les textes de tout les auteurs dans la liste de mot ordonne et
        # si le mot est dans le dictionnaire du texte inconnu le rajoute dans une liste de mot commun. La liste de
        # mot commun contient en ordre:
        #                               0.Le gram en commun
        #                               1.La frequence dans le texte inconnu
        #                               2.La frequence dans le texte de l'auteur
        for auteur in longeurduDico:
            for motconnu in listeDeDico[auteur]:
                if args.m == 2:
                    if motconnu[0] in dictionnaireInconnu:
                        listeDeMotCommun[auteur].append((motconnu[0], dictionnaireInconnu[motconnu[0]], motconnu[1]))
                else:
                    if motconnu[0] in dictionnaireInconnu:
                        listeDeMotCommun[auteur].append((motconnu[0], dictionnaireInconnu[motconnu[0]], motconnu[1]))

        # Calcul de la frequence pour chaque auteur
        FreqAuteur = calculDefrequence(longeurduDico, listeDeMotCommun, 2)

        # Calcul de la frequence pour l'inconnu
        FreqAuteurInconnu = calculDefrequence(longeurduDico, listeDeMotCommun, 1)

        # Normalisation des frequences. Dans ce bout de code,
        # on crée un tableau avec comme informations:
        #                                               0. Fréquence normalisé du texte inconnu
        #                                               1. Fréquence normalisé du texte pour l'auteur
        for auteur in longeurduDico:
            for nombre in range(len(listeDeMotCommun[auteur])):
                listeDeProbabilite[auteur].append((listeDeMotCommun[auteur][nombre][1] / FreqAuteurInconnu[auteur],
                                                   listeDeMotCommun[auteur][nombre][2] / FreqAuteur[auteur]))

        # Calcul de la ressemblance avec l'auteur(La racine carré de la somme de toutes les différence entre la
        # fréquence normalisé de l'auteur et la fréquence normalisé de l'inconnu au carré)
        for auteur in longeurduDico:
            for nombre in range(len(listeDeProbabilite[auteur])):
                sommeCarre[auteur].append(pow(
                    (listeDeProbabilite[auteur][nombre][0] - listeDeProbabilite[auteur][nombre][1]), 2))
            sommeCarre[auteur] = sum(sommeCarre[auteur])
            sommeCarre[auteur] = math.sqrt(sommeCarre[auteur])

        # affichage
        if args.a:
            print(args.a + ": ", "%.4f" % sommeCarre[auteur])
        else:
            for auteur in range(len(listeDeDico)):
                print(authors[auteur] + ": ", "%.4f" % sommeCarre[auteur])

    # Bloc de code qui génere un texte
    if args.g and args.G:

        listeDeMarkov = [[] for auteur in range(len(listeDeDico))]
        mot = ["les" for auteur in range(len(listeDeDico))]
        listeDeTexte = [["les"] for auteur in range(len(listeDeDico))]
        nombreTotal = [1 for i in range(len(listeDeDico))]

        for nombreDeMots in range(args.G):  # Pour le faire le nombre de mot demandé
            # Crée une liste de chaines de markov pour tout les auteurs demmandées(donc la prochaine couche)
            listeDeSuivantelu = []
            listeDeMarkov = ChaineDeMarkov(listeDeDico)

            for auteur in range(len(listeDeMarkov)):
                tot = 0
                probabilite = []
                motsuivant = [listeDeMarkov[auteur][i][0] for i in range(len(listeDeMarkov[auteur]))]
                for i in range(len(listeDeMarkov[auteur])):
                    tot += listeDeMarkov[auteur][i][1]
                for i in range(len(listeDeMarkov[auteur])):
                    probabilite.append(listeDeMarkov[auteur][i][1] / tot)
                listeDeSuivantelu.append(numpy.random.choice(motsuivant, p=probabilite))
            for auteur in range(len(listeDeMarkov)):
                listeDeTexte[auteur].append(listeDeSuivantelu[auteur])
                mot[auteur] = listeDeSuivantelu[auteur]
            listeDeSuivantelu.clear()

        if args.a:
            with open(args.g, "w+") as doc:
                for auteur in range(len(listeDeTexte)):
                    print(args.a + ":", file=doc)
                    for mot in range(len(listeDeTexte[auteur])):
                        print(listeDeTexte[auteur][mot], file=doc, end=" ")
                    print("\n", file=doc, end=" ")
        else:
            with open(args.g, "w+") as doc:
                for auteur in range(len(listeDeTexte)):
                    print(authors[auteur] + ":", file=doc)
                    for mot in range(len(listeDeTexte[auteur])):
                        print(listeDeTexte[auteur][mot], file=doc, end=" ")
                    print("\n", file=doc, end=" ")
