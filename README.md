# DISRPT/latest 
## Introduction
### A Multilingual, multi-domain, Cross-framework Discourse Collection
Repository of the latest data for the multilingual DISRPT benchmark.  

Data in this particular sub-repository of the DISRPT benchmark matches the following paper:  
[TODO add link} Braud, C., Zeldes, A., Rivière, L., Liu, Y.J., Muller, P., Sileo, D., Aoyama, T., (2024), DISRPT: A Multilingual, Multi-domain, Cross-framework Benchmark for Discourse Processing, LREC.  

### Shared Tasks on DIScourse Relation Parsing and Treebanking
**Discourse Unit Segmentation**, **Connective Detection**, and **Discourse Relation Classification** :  

Objective is to provide training, development, and test datasets from all available languages and treebanks in the RST, SDRT, PDTB and dependency formalisms, using a uniform format.  
Because different corpora, languages and frameworks use different guidelines, the shared task is meant to promote design of flexible methods for dealing with various guidelines, and help to push forward the discussion of standards for computational approaches to discourse relations. We include data for evaluation with and without gold syntax, or otherwise using provided automatic parses for comparison to gold syntax data.  

https://github.com/disrpt/sharedtask2023  
https://github.com/disrpt/sharedtask2021  
https://github.com/disrpt/sharedtask2019  
 
## Types of DATA, types of annotations
lang.framework.name
dep/sdrt/rst/pdtb
tok/conllu/relstre 

décrire précisement les OOD, les mwe+mwt/mwe/mwt, les raw_text/duplicate

## Statistics : cp celles des repos ST => ben non, cf paper ou générer des nouvelles stats

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

### Tasks

### Multi-Word Expression: Syntactical Text vs. Raw Text
def d'un MWE avec ex
dans les rels : par defautl syntactial text 
ajout de la colonne rw textqd c'était possible, sinon duplicate pour pas laisser des colonnes vides
tableau recap pour chaque dataset : langue avec MWE ? process des MWE ? avec ou sans forme contrctées ? raw txt / duplicate


## Directories
The shared task repository currently comprises the following directories:

* `data` - individual corpora from various languages and frameworks.
    * Folders are given names in the scheme `LANG.FRAMEWORK.CORPUS`, e.g. `eng.rst.gum` is the directory for the GUM corpus, which is in English and annotated in the framework of Rhetorical Structure Theory (RST).
    * Note that some corpora (eng.rst.rstdt, eng.pdtb.pdtb, tur.pdtb.tdb, zho.pdtb.cdtb) do not contain text or have some documents without text (eng.rst.gum) and text therefore needs to be reconstructed using `utils/process_underscores.py`.
* `utils` - scripts for validating, evaluating and generating data formats. The official scorer for the 3 tasks is `disrpt_eval.py`. See `usage` section for details.

See the README files in individual data directories for more details on each dataset.


## Usage
### Reconstruction of underscored data






### Evaluation
* `disrpt_eval_2024.py` - evaluation of 1 predictions file against 1 gold file.
    * Usage: `python disrpt_eval_2024.py [-h] -g GOLDFILE -p PREDFILE -t {S,C,R} [-s] [-nb] [-rt]`
    * Arguments required: 
        * -g/--goldfile GOLDFILE ................. Path to gold file
        * -p/--predfile PREDFILE ................. Path to predicitons file
        * -t/--task {S,C,R} ...................... Task to evaluate. S = "Discourse Unit Segmentation", C = "Connectives Identification", R = "Relations Classification"
    * Options:
        * -s/--string_input ...................... If inputs are strings instead of file path
        * -nb/--no_boudary_edu ................... Does not count EDU that starts at beginning of sentence, relevant for task S and format CONLLU only
        * -rt/--rel_type ......................... Evaluate relation type instead of label, relavant for task R only
    * Output:
        * Results are print directly as STDout.



* `evaluation_main.sh` - evaluation of all predictions files organized in same directories structure than gold files: ...data/LANG.FRAMEWORK.CORPUS/LANG.FRAMEWORK.CORPUS_DIV.EXTENSION
    * Usage: `bash evaluation_main.sh -g GOLDDIR -p PREDDIR -o OUTDIR [-d] [-b] [-y] [-s]`
    * Arguments required:
        * -g/--gold_dir GOLDDIR ................... Path to parent gold directory (...latest/data).
        * -p/--pred_dir PREDDIR ................... Path to parent predictions directory (.../data).
        * -o/--out_eval_dir OUTDIR ................ Path to output directory to print results files.
    * Options:
        * -d/--division_set ....................... Datasets division to evaluate to 'dev. Default='test' (DIV).
        * -b/--no_boudary_edu ..................... Option for TASK-1/.conllu. Evaluate only intra-sentential EDUs.
        * -y/--rel_type ........................... Option for TASK-3. Evaluate TYPES instead of LABELS (cf.PDTB) plus metrics for each type.
        * -s, --string_input ...................... Whether inputs are strings instead of file names.
    * Output:
        * For each file evaluated, results are print into a file following this name convention : .../OUTDIR/LANG.FRAMEWORK.CORPUS_DIV.EXTENSION_eval


## TODO: ajouter tous les readme ?