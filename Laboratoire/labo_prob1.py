# coding=utf-8
###
###  Code pour explorer le premier exercice du laboratoire - S2 APP5i
###  Le traitement des arguments a ©tÃ© inclus:
###     Tous les arguments requis sont prÃ©sents et accessibles dans args
###     Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
###
###  FrÃ©dÃ©ric Mailhot, 28 fÃ©vrier 2018
###  FrÃ©dÃ©ric Mailhot, 28 fÃ©vrier 2020


import math
import argparse
import glob
import sys
import os

from pythonds.graphs import Graph

def addBucket(d,bucket,word):
    if bucket in d:
        d[bucket].append(word)
    else:
        d[bucket] = [word]
###
### Code tirÃ© de la section 7.8 du livre de rÃ©fÃ©rence
### Ã€ adapter pour l'exercice:
###   - ajouter un arc entre des mots qui ne sont pas de la mÃªme longueur mais qui ne diffÃ¨rent que par une lettre
###   - permettre des arcs entre des mots qui diffÃ¨rent par 2, 3, ... lettres (indiquÃ© sur la ligne de commande)
def buildGraph(wordFile):
    d = {}
    g = Graph()
    wfile = open(wordFile,'r')
    # create buckets of words that differ by one letter
    for line in wfile:
        word = line[:-1]
        for i in range(len(word)):
            bucket = word[:i] + '_' + word[i+1:]
            addBucket(d,bucket,word)
            ### Ajout des distances de 2 lettres
            word_remain = word[i+1:]
            for j in range(len(word_remain)):
                bucket = word[:i] + '_' + word_remain[:j] + '_' + word_remain[j+1:]

    # add vertices and edges for words in the same bucket
    for bucket in d.keys():
        for word1 in d[bucket]:
            for word2 in d[bucket]:
                if word1 != word2:
                    g.addEdge(word1,word2)
    return g

###  Vous devriez ajouter du code pour accÃ©der au mot de dÃ©part (fourni sur la ligne de commande)
###  et ensuite parcourir le graphe jusqu'Ã  une distance D (fournie sur la ligne de commande) du mot d'origine

def set_unvisited(g):
    g= Graph
    for vertex in g.getVertices():
        g.getVertex(vertex).set_color("white")

def print_path(vertex,dist):
    vertex= Vertex
    if dist == 0:
        return
    vertex.set_color("black")
    print(vertex.get_key())
    neighbor_list = vertex.get_neighbors()
    for neighbor_vertex in neighbor_list:
        if neighbor_vertex.get_color() == "white":
            print_path(neighbor_vertex,int(dist)-1)
            return



### Main: lecture des paramÃ¨tres et appel des mÃ©thodes appropriÃ©es
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='S2-APP5i Labo1:Exercice1.py')
    parser.add_argument('-f', required=True, help='Fichier contenant la liste de mots')
    parser.add_argument('-m', required=True, help='Mot de dÃ©part')
    parser.add_argument('-d', required=True, help='Distance du mot de dÃ©part')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    args = parser.parse_args()

### Si mode verbose, reflÃ©ter les valeurs des paramÃ¨tres passÃ©s sur la ligne de commande
    if args.v :
        print("Mode verbose:")
        print("Fichier de mots utilisÃ©: " + args.f)
        print("Mot de dÃ©part: " + args.m)
        print("Distance du mot de dÃ©part: " + args.d)



### Ã€ partir d'ici, vous devriez inclure les appels requis pour la crÃ©ation du graphe, puis son utilisation
    g = buildGraph(args.f)
    start_vertex = g.getVertex(args.m)
    set_unvisited(g)
    print_path(start_vertex,args.d)