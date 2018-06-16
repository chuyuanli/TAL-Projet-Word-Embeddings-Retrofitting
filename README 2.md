# TAL-Projet-Word-Embeddings-Retrofitting
TAL M1 annual project: refine word embeddings with semantic ressources (retrofitting proposed by Faruqui)

## What is about? 
This report is based on the paper of [Faruqui et al, 2014](http://www.manaalfaruqui.com/papers/naacl15-retrofitting.pdf) to improve the word embeddings with the algorithm of retrofitting. It is used to post-process word vectors to incorporate knowledge from semantic lexicons (thesaurus). As shown in these word vectors are generally better in performance on semantic tasks than the original word vectors.

## Requirements
1. Python2.7 or 3.6
2. Libraries to install:
	- numpy
	- sklearn
	- scipy.stats
	- matplotlib.pyplot
	- seaborn
	- pandas
3. Data
	- Word Vectors file(skip-gram vectors trained by Google)
	- Thesaurus file(ppdb, framenet or wordnet)

## Before running the program
1. Prepare a reporsitory and put all the scripts in it:
	- retrofit.py
	- eval_intrin.py
	- eval_extrin1.py
	- eval_extrin2.py
	- eval_visualisation.py
	- lanceur.sh 
2. In the same reporsitory, put all the files required (how to get these files will be further explained in the dossier):
	- w2v_orig.txt
	- ppdb-xl.txt (and/or framenet.txt, and/or wordnet.txt)
	- ws353.txt
	- a sub-reporsitory **named txt_sentoken** which contains 1000 neg and pos film reviews respectivly

The first two files are used for retrofitting, and the last two are for evaluation.

## Running the program
### Use lanceur.sh (highly recommended)
We have prepared a bash file which will trigger all the python scripts one by one. The codes have been taken care of, users only need to change the file paths in their computer accrodingly.
- Change the first 6 paths which indicate w2v file, thesaurus files and evaluation files, you can also change the file names. For example: `w2v_orig='yourPathToTheRepository/w2v_135k.txt'`
- Change the path name of the 4 ftrain ftest files, but leave the file names as they are: `ftrain_orig='yourPathToTheRepository/output_train_nonRetf'`
- Indicate the output file name here `'output_w2v='WriteYourOutputFileNameHere'`

A trace recording file (trace.txt) will be generated automatically while each script is running. It indicates which step you are in, and show some test results. For example, you will see the trace below in the phrase of intrinsic evaluation:
```
[PROCESSUS EVALUATION INTRINSEQUE]
--- Spearman rank correlation entre ws353 et w2v original ----
r = 0.37043960280629223 p = 7.381041913132579e-13
--- Spearman rank correlation entre ws353 et w2v retrofitted (PPDB) ----
r = 0.46034181696333953 p = 8.216530152440082e-20
```

A complete run of all the scipts will go through 4 processes and will take around 5 minutes. The following files or graphes would be generated (if the thesaurus is ppdb):
- Retrofitted word vectors: `output_wv135k_ppdb.txt`
- Spearman's correlation graphes: `ws353_oldw2v.png` and `ws353_neww2v_ppdb.png`
- 4 svmlight files named like `output_train_retf` (load automatically for extrinsic evaluation)
- 2-dimensional PCA graph: `PCA projection.png`

### Run .py file
It is also possible to run the python scripts separatly:
`python3 retrofit.py w2v_orig.txt thesaurus.txt output_w2v.txt -n num_iter -a alpha -b sumBeta`
`python3 retrofit.py w2v_135k.txt ppdb-xl.txt output_wv135k_ppdb -n 10 -a 1 -b 1.0`

Where, 'n' is an integer which specifies the number of iterations for which the optimization is to be performed. Usually n = 10 gives reasonable results. 
'a' and 'b' are hyper-parameters to indicate the weights for two parts in the algorithm (cf dossier).

Other .py files are similar, follow the instructions and feed the corresponding files as arguments will be fine.

**Main reference**
```
@InProceedings{faruqui:2014:NIPS-DLRLW,
  author    = {Faruqui, Manaal and Dodge, Jesse and Jauhar, Sujay K.  and  Dyer, Chris and Hovy, Eduard and Smith, Noah A.},
  title     = {Retrofitting Word Vectors to Semantic Lexicons},
  booktitle = {Proceedings of NAACL},
  year      = {2015},
}
```

Should you have any questions, feel free to contact us =)
lisa27chuyuan@gmail.com








