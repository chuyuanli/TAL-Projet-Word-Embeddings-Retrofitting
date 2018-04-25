#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""
-------------------------------------------------------------------------
| Algo pour calculer les nouveaux vecteurs en utilisant le thesaurus.   |
| par defaut, hyper-parametre α = 1, sum(β) = 1                         |
-------------------------------------------------------------------------

Thesaurus(union de PPDB xl et WordNet) est represente par un dictionnaire:
{word1: [neigh1, neigh2...],
 word2: [neigh3, neight4..],
 ...
}

WordVecs est un dictionnaire de vecteurs avec key = mot a retroffiter, valeur = vecteurs originaux
e.g: wordVec['dog'] = [2. 2.6 3.2 3.8 4.4 5. ... ], taille de vecteur D = 300

NewWordVecs est un dictionnaire de vecteurs de meme taille que WordVecs apres retrofitting
e.g: newWordVec['dog'] = [2.5 3. 3.2 3.8 4.6 5. ... ], D = 300

"""

import argparse
import gzip
import math
import numpy
import re
import sys
import collections
import re

from collections import defaultdict
from copy import deepcopy


################ PARTIE RETROFITTING ##################

isNumber = re.compile(r'\d+.*')

def norm_word(word):
  if isNumber.search(word.lower()):
    return '---num---'
  elif re.sub(r'\W+', '', word) == '':
    return '---punc---'
  else:
    return word.lower()



def read_word_vecs(filename):
  """
  lire tous les mots et leurs vecteurs et stocker dans un dict_w2v
  """
  wordVectors = {}
  if filename.endswith('.gz'): 
    fileObject = gzip.open(filename, 'r')
    print("zip")
  else: 
    fileObject = open(filename, encoding = "ISO-8859-1")
    print("w2v file is openning...")

  count_bruit = 0
  for line in fileObject:
    line = line.strip().lower()
    word = line.split()[0]
    wordVectors[word] = numpy.zeros(len(line.split())-1, dtype=float)
    for index, vecVal in enumerate(line.split()[1:]):
      #print(vecVal)
      #input()
      if '\x00' in vecVal: 
        vecVal = vecVal.replace('\x00','0.0')
      # regex to find the 'qualified' vectors, ignore wrong type of vectors such as: '_vis\x00', '²0.0'
      real_vec = re.match(r"^[-+]?\d*\.\d+$", vecVal) 
      if real_vec:
        wordVectors[word][index] = float(vecVal)
      else:
        count_bruit += 1
        continue

        # if vecVal.replace('.','',1).isdigit(): # wrong type of vectors such as: '_vis\x00', '²0.0'
        #   wordVectors[word][index] = float(vecVal)
        # else:
        #   count_bruit += 1
        #   continue
  
  print("Lines ignored = " + str(count_bruit)) 
  sys.stderr.write("Vectors read from: "+filename+" \n")

  return wordVectors

  
''' Read thesaurus word relations and store in a dictionary '''
def read_thesaurus(filename, wordVecs, dict_thesaurus):
  for line in open(filename, 'r'):
    words = line.lower().strip().split() #a list of neighbor words
    word1 = norm_word(words[0])
    if word1 not in dict_thesaurus.keys():
      dict_thesaurus[word1] = set([norm_word(word) for word in words[1:]])
    else:
      for neigh in words[1:]:
        dict_thesaurus[word1].add(neigh)

  sys.stderr.write("thesaurus read from: "+filename+"\n")
  return dict_thesaurus


''' Retrofit word vectors to a thesaurus '''
def retrofit(wordVecs, thesaurus, numIters, alpha=1, sumBeta=1.0):
  newWordVecs = deepcopy(wordVecs)
  # print(len(newWordVecs))
  wvVocab = set(newWordVecs.keys())
  loopVocab = wvVocab.intersection(set(thesaurus.keys())) # a set 
  # for word in loopVocab:
  #   outfile.write(word+'\n')

  print("Words to be retrofitted = %d / %d" %(len(loopVocab), len(wvVocab)))

  for it in range(numIters):
    count = 0
    # outfile = open('retrofitted_words.txt','w')

    # loop through every node also in ontology (else just use data estimate)
    for word in loopVocab:
      wordNeighbours = set(thesaurus[word]).intersection(wvVocab)
      numNeighbours = len(wordNeighbours)
      #no neighbours, pass - use original data
      if numNeighbours == 0:
        continue
      else:
        # check which are the words actually retrofitted
        # outfile.write(word+"\n")
        count += 1
        # loop over neighbours and add to neighbor vectors (sum of weight = 1)
        newVec = wordVecs[word] * alpha
        beta = sumBeta / numNeighbours
        for a_neigh in wordNeighbours:
          newVec += newWordVecs[a_neigh] * beta
        newWordVecs[word] = newVec / (alpha + sumBeta)

  print("Actual retrofitted words = %d" % (count))
  print("New vectors done!")
  return newWordVecs


''' Write word vectors to file '''
def print_word_vecs(wordVectors, outFileName):
  sys.stderr.write('\nWriting down the vectors in \''+outFileName+'\'...\n')
  outFile = open(outFileName, 'w')  
  for (word, values) in wordVectors.items():
    outFile.write(word+' ')
    for val in wordVectors[word]:
      outFile.write('%.4f' %(val)+' ')
    outFile.write('\n')      
  outFile.close()



#################### PARTIE MAIN ######################

if __name__=='__main__':

  usage = """ RETROFIT WORD-EMBEDDINGS WORD2VEC

  """+sys.argv[0]+"""[options] W2V_FILE PPDB_FILE OUTPUT_FILE

  W2V est le fichier qui contient 115k mots a retrofitted
  PPDB est le theseaurus qui donne les mots voisins (en general, PPDB donne le meilleur resultat)
  OUTPUT est le fichier ou s'ecrit les nouveaux vecteurs apres retrofitting

  - prog [options] fichiers WORDNET ET FRAMENET
          => prendre en compte les mots voisins dans d'autres sources theseaurus

  - prog [options] integer NUMITER
          => hyoerparametre numbre de retrofitting, en pratique le resultat converge a 10 iterations

  - prog [options] integer ALPHA, float BETA
          => les 2 hyperparametres qui controlent les poids relatifs entre q(i) chapeau et q(ij)

"""

  parser = argparse.ArgumentParser()
  parser.add_argument("w2v", type=str, default=None, help="Input word vecs")
  parser.add_argument("ppdb", type=str, default=None, help="PPDB file name")
  parser.add_argument("output", type=str, help="Output word vecs")
  parser.add_argument("-t2", "--wordnet", type=str, default=None, help="wordnet file name")
  parser.add_argument("-t3", "--framenet", type=str, default=None, help="FrameNet file name")
  parser.add_argument("-n", "--numiter", type=int, default=10, help="Num iterations")
  parser.add_argument("-a", "--alpha", type=int, default=1, help="hyperparametre: poids de q(i) chapeau")
  parser.add_argument("-b", "--sumBeta", type=float, default=1.0, help="hyperparametre: sum du poids de q(ij)")
  args = parser.parse_args()

  wordVecs = read_word_vecs(args.w2v)
  thesaurus = read_thesaurus(args.ppdb, wordVecs, defaultdict(str))
  # si on veut combiner les thesaurus differents
  if args.wordnet:
    thesaurus = read_thesaurus(args.wordnet, wordVecs, thesaurus)
  if args.framenet:
    thesaurus = read_thesaurus(args.framenet, wordVecs, thesaurus)
  #print(len(thesaurus))
  outFileName = args.output
  
  print("\n******** BAREMES DE HYPER-PARAMETRES *********")
  numIter = int(args.numiter)
  print("Iteration time = "+str(numIter))
  alpha = int(args.alpha)
  beta = float(args.sumBeta)
  print("Alpha = %d, SUM Beta = %f" % (alpha, args.sumBeta))
  print("******** FIN DE BAREMES *********\n")
  
  # retrofit new vectors
  new_vecs = retrofit(wordVecs, thesaurus, numIter, alpha, beta)
  # print out the new vectors
  print_word_vecs(new_vecs, outFileName) 






