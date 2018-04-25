# TAL-Projet-Word-Embeddings-Retrofitting
TAL M1 annual project: refine word embeddings with semantic ressources (retrofitting proposed by Faruqui)


### What is retrofitting? ###
This is an algorithme proposed by Faruqui et al. 2015 which aims at refining word embeddings by semantic ressources to get better performance in tasks such as lexical similarity and sentimental analysis. 

The new vectors is supposed to be close to:
	- the original vectors 
	- its semantic neighbors (hyponyms, hyeronyms, etc)


### Sources ###
- Word Vectors: Google word2vec tool (Mikolov et al., 2013a), we take the pretrained 300-dimension 3 million words
https://code.google.com/archive/p/word2vec/
- Thesaurus: 
	- PPDB parahrase database: xl package, available here:
	http://paraphrase.org/#/download
	- WordNet: human-constructed semantic lexicon of English words
	- FrameNet: lexical and predicate-argument semantics in English


### Workflow ###
- Faruqui has proposed available lexicon ressources here:
https://github.com/mfaruqui/retrofitting/tree/master/lexicons
- Need good format of w2v, transforme script in C++
- Go through algorithme, iterate 10 times (converge, need math prouve)
- New vectors test with ws353 and polarity sentiment analysis
	- intrinsic evaluation: ws353 best result with PPDB, followed by WordNet and a combination of these two, bad result with FrameNet
	- Extrinsic evaluation: film polarity review, to be done...


### Reference ###

@InProceedings{faruqui:2014:NIPS-DLRLW,
  author    = {Faruqui, Manaal and Dodge, Jesse and Jauhar, Sujay K.  and  Dyer, Chris and Hovy, Eduard and Smith, Noah A.},
  title     = {Retrofitting Word Vectors to Semantic Lexicons},
  booktitle = {Proceedings of NAACL},
  year      = {2015},
}
