# latest
Latest data for the multilingual DISRPT discourse benchmark


# DiscHub: DISRPT Latest
# Multilingual and Cross-framework Discourse Collection

Repository from DISRPT Shared Task for  
Discourse Unit Segmentation, Connective Detection, and Discourse Relation Classification  
-> link vers paper LREC 2024

## Introduction
 -> copier readme des ST avec les liens vers les repo, les papers etc

## Types of DATA, types of annotations
lang.framework.name
dep/sdrt/rst/pdtb
tok/conllu/relstre 

## Evaluation 
description de nos script d'eval avec les option type/rel, description des labels tok et conll et option de scores all/intra-sentential

## Statistics : cp celles des repos ST

## Description ds data / changelogs :
décrire précisement les OOD, les mwe+mwt/mwe/mwt, les raw_text/duplicate

## Corpora
nb of corpora, add definition of a corpus vs dataset sim. cf. paper
<!--
 Regarding the number of datasets, we will make clearer the distinction between corpora (=one annotation project) and what is called here a dataset (=a combination of one language, one corpus, one framework). This distinction explains why the benchmark covers 24 corpora but 28 datasets (e.g. the TED Multilingual Discourse Bank (TED-MDB) is one original corpus, but covers several languages that are each regarded as a separate dataset for testing systems). 
-->
24 corpora dont 4 corpora "multi" : gum {2:rst, pdtb}, tedm {3:eng, por, tur}, sctb {2:spa, zho} 
28 datasets
### Corpora Partitions
The majority of datasets (23/28) are divided into 3 parts: training set, development set and test set.
Four datasets are divided into 2 parts only (development and test sets): eng.dep.covdtb and {eng,por,tur}.pdtb.tedm.
One dataset is only one part (test set): eng.rst.gentle.

### Multi-Word Expression: Syntactical Text vs. Raw Text
def d'un MWE avec ex
dans les rels : par defautl syntactial text 
ajout de la colonne rw textqd c'était possible, sinon duplicate pour pas laisser des colonnes vides
tableau recap pour chaque dataset : langue avec MWE ? process des MWE ? avec ou sans forme contrctées ? raw txt / duplicate