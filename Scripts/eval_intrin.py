#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import collections
from collections import defaultdict
import numpy as np
import math
import re
import pprint
import scipy.stats
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


################ PARTIE EVALUATION INTRINSEQUE ##################

def read_ws353(file):
	dict_ws353 = defaultdict(float)

	with open(file, 'r') as file_ws353:
		for line in file_ws353:
			mot1, mot2, socreH = line.strip().split("\t")
			mot_pair = (mot1.lower(), mot2.lower())
			dict_ws353[mot_pair] = float(socreH)

	#print(dict_ws353)
	print("dict_ws353 ready.")
	return dict_ws353


def get_word_vecs(filename, dict_ws353):
	"""
	lire un fichier w2v et retourner un dict de mot avec leurs vecteurs
	dict_ws353 pour indiquer quels sont les mots dont on cherche les vecteurs
	"""
	wordVectors = {}
	# variable ws353List stocke tous les mots de ws353, dictinct mot = 437
	ws353List = set()
	for (m1, m2) in dict_ws353.keys():
		ws353List.add(m1)
		ws353List.add(m2)

	fileObject = open(filename, encoding = "ISO-8859-1")
	print("w2v file is openning. Searching for words in ws353...")

	count_bruit = 0
	for line in fileObject:
		line = line.strip().lower()
		word = line.split()[0]
		if word in ws353List: # prend seulement les mots dans ws353
			wordVectors[word] = np.zeros(len(line.split())-1, dtype=float)
			for index, vecVal in enumerate(line.split()[1:]):
				if '\x00' in vecVal: 
					vecVal = vecVal.replace('\x00','0.0')

				# regex to find the 'qualified' vectors, ignore wrong type of vectors such as: '_vis\x00', '²0.0'
				real_vec = re.match(r"^[-+]?\d*\.\d+$", vecVal) 
				if real_vec:
				  wordVectors[word][index] = float(vecVal)
				else:
				  count_bruit += 1
				  continue
		      
		    #normalize vectors
			wordVectors[word] /= math.sqrt((wordVectors[word]**2).sum() + 1e-6)
	  
	# print("Lines ignored = " + str(count_bruit)) 
	print("Vectors read from: "+filename+" \n")
	return wordVectors


def score_cosinus(w2v, ws353):
	"""
	prendre les mots paires et calculer leur similarite cosinus selon le fichier w2v
	retourner un dict avec la cle paire de mot et valeur score cos
	"""
	score_cos = {}
	count = 0		

	for (mot1, mot2) in ws353.keys(): #calculer le score cosinus que pour les mots retrofitted
		# if mot1 in checkList and mot2 in checkList:
		if mot1 in w2v.keys() and mot2 in w2v.keys():
			count += 1
			# les vecteurs sont deja normalises, donc multiplier directement les vecteurs de 2 mots, et puis sommer
			score = (w2v[mot1] * w2v[mot2]).sum()
			score_cos[(mot1, mot2)] = score

	# pprint.pprint(score_cos)
	print("Calculer la similarite cosinus de %d paires de mots. \n" % (count))
	return score_cos


def Spearman(dict_ws353, dict_w2v, new_w2v):
	"""
	Evaluation intrinseque en calculant la correlation Spearman entre les paires de mots dans ws353
	X: array_like, score ws353 note par humain 
	Y: array_like, score calcule par ancien w2v
	Y2: array_like, score calcule par w2v retrofitted
	retourner:
	- r: float, spearman correlation
	- p: float, empirical p-value
	"""
	# initialiser X et Y pour stocker les score humain et cosinus
	X, Y= list(), list()

	for mot_paire in dict_ws353.keys():
		if mot_paire in dict_w2v.keys():
			X.append(dict_ws353[mot_paire])
			Y.append(dict_w2v[mot_paire])

	# transformer X et Y en numpy arrays
	X, Y= np.asarray(X, dtype=float), np.asarray(Y, dtype=float)
	# verifier la taille de X et Y soit equivalente
	if len(X) != len(Y):
		raise ValueError("X and Y are not of equal size!")
	# calculer correlation Spearman et p value
	r, p_value = scipy.stats.spearmanr(X, Y)
	print("r = "+str(r)+" p = "+str(p_value) + "\n")

	if not new_w2v:
		plot_scatter_spearman(X, Y, False)
	else:
		plot_scatter_spearman(X, Y, True)


def plot_scatter_spearman(X, Y, new_w2v):
	"""
	plot bivariate scatterplots
	refer to source online:
	http://lilithelina.tumblr.com/post/135265946959/data-analysis-pearson-correlation-python
	"""
	# creer un dataframe pour stocker X et Y
	sub_data = pd.DataFrame(
    {
     'ws353': X,
     'w2v': Y,
    })

	# plot la correlation entre X and Y, sauvegarder l'image
	fig = plt.figure(figsize=(10,5))
	sns.regplot(x="ws353", y="w2v", fit_reg=True, data=sub_data);
	plt.xlabel('Score WS353');
	if not new_w2v:
		plt.ylabel('Score W2V original');
		plt.title('Scatterplot for the Spearman correlation between ws353 and w2v original');
		plt.savefig("ws353_oldw2v_v2.png")
	else:
		plt.ylabel('Score W2V retrofitted');
		plt.title('Scatterplot for the Spearman correlation between ws353 and w2v retrofitted');
		plt.savefig("ws353_neww2v_ppdb_wn.png")



#################### PARTIE MAIN ######################

# checkFile = "/Users/lichuyuan/Desktop/TALProjet/retrofitted_words_ppdb.txt"

file = ""
dict_ws353 = read_ws353(file)

old_w2v = get_word_vecs("/Users/lichuyuan/Desktop/TALProjet/w2v_135k.txt", dict_ws353)
old_score = score_cosinus(old_w2v, dict_ws353)
print("--- Spearman rank correlation entre ws353 et w2v original ----")
Spearman(dict_ws353, old_score, False)

new_w2v = get_word_vecs(wv_file, dict_ws353)
new_score = score_cosinus(new_w2v, dict_ws353)
print("--- Spearman rank correlation entre ws353 et w2v retrofitted (PPDB) ----")
Spearman(dict_ws353, new_score, True)














