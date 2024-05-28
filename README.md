# DISRPT/latest 
## Introduction
**A Multilingual, multi-domain, Cross-framework Discourse Collection**  
Repository of the latest data for the multilingual DISRPT benchmark.  

Data in this particular sub-repository of the DISRPT benchmark matches the following paper:  
[TODO add link} Braud, C., Zeldes, A., Rivière, L., Liu, Y.J., Muller, P., Sileo, D., Aoyama, T., (2024), DISRPT: A Multilingual, Multi-domain, Cross-framework Benchmark for Discourse Processing, LREC.  

**Shared Tasks on DIScourse Relation Parsing and Treebanking**  
**Discourse Unit Segmentation**, **Connective Detection**, and **Discourse Relation Classification** :  

Objective is to provide training, development, and test datasets from all available languages and treebanks in the RST, SDRT, PDTB and dependency formalisms, using a uniform format.  
Because different corpora, languages and frameworks use different guidelines, the shared task is meant to promote design of flexible methods for dealing with various guidelines, and help to push forward the discussion of standards for computational approaches to discourse relations. We include data for evaluation with and without gold syntax, or otherwise using provided automatic parses for comparison to gold syntax data.  
In the following repositories one can find related papers references.

https://github.com/disrpt/sharedtask2023  
https://github.com/disrpt/sharedtask2021  
https://github.com/disrpt/sharedtask2019  
 
## Types of DATA
The tasks are oriented towards finding the locus and type of discourse relations in texts, rather than predicting complete trees or graphs. For frameworks that segment text into non-overlapping spans covering each entire documents (RST and SDRT), the segmentation task corresponds to finding the **starting point of each discourse unit**. For PDTB-style datasets, the unit-identification task is to identify the **spans of discourse connectives** that explicitly identify the existence of a discourse relation. These tasks use the files ending in `.tok` and `.conllu` for the **plain** text and **parsed** scenarios respectively.  

For relation classification, two discourse unit spans are given in text order together with the direction of the relation and context, using both plain text data and stand-off token index pointers to the treebanked files. Information is included for each corpus in the `.rels` file, with token indices pointing to the `.tok` file, though parse information may also be used for the task. The column to be predicted is the final label column; the penultimate `orig_label` column gives the original label from the source corpus, which may be different, for reference purposes only. This column may not be used. The relation direction column may be used for prediction and does not need to be predicted by systems (essentially, systems are labeling a kind of ready, unlabeled but directed dependency graph).  

Note that some datasets contain **discontinuous** discourse units, which sometimes nest the second unit in a discourse relation. In such cases, the unit beginning first in the text is considered `unit1` and gaps in the discourse unit are given as `<*>` in the inline text representation. Token index spans point to the exact coverage of the unit either way, which in case of discontinuous units will contain multiple token spans.  

**Multiword Expression: Syntactical Text vs. Natural (Raw) Text in .RELS**  
Some corpora use CoNLL-U Multiword Tokens with hyphen IDs for complex word forms (e.g. 1-2 don't ... 1 do ... 2 n't).  
Not every language has this contraction possibility. For those that can, and for which tools exist, 
we provide in RELS files both what we call `syntactical text` (extended forms) and `natural or raw text` (contracted forms). 
When it is not available, we just duplicate the available text, to avoid empty fields. Below is a recap of columns content: 

`doc`: *reference of document*  
`unit1_toks`: *tokens IDs span of unit1 (= first unit/argument of syntagmatic order)*  
`unit2_toks`: *tokens IDs span of unit2 (= second unit/argument of syntagmatic order)*  
`unit1_txt`: *syntactical text of unit1* (not available for : deu, eus, fra, nld, rus, spa, tha, zho)  
`unit2_txt`: *syntactical text of unit2* (not available for : deu, eus, fra, nld, rus, spa, tha, zho)  
`u1_raw`: *raw/natural text of unit1* (not available for : por{crpc,tedm})  
`u2_raw`: *raw/natural text of unit2* (not available for : por{crpc,tedm})  
`s1_toks`: *tokens IDs span of the sentence that contains unit1*  
`s2_toks`: *tokens IDs span of the sentence that contains unit2*  
`unit1_sent`: *syntactical text of sentence that contains unit1*  
`unit2_sent`: *syntactical text of sentence that contains unit2*  
`dir`: *directionality of relation adapted to units*  
`rel_type`: *type of relation* (available only for PDTB framework)  
`orig_label`: *original label(s)*  
`label`: *DISRPT selected label to predict: first one/english truncated one/misspelled corrected one...*  

*See paper for details.  


## Corpora
Namely, we distinct `corpora` (= one annotation project) and `dataset` (= a combination of one language, one corpus, one framework).  
There are 24 corpora, for 28 datasets : 
* "2" GUM: RST/PDTB
* "3" Tedm: eng, por, tur
* "2" Sctb: spa, zho

**Partitions**  
The majority of datasets (23/28) are divided into 3 parts: training set, development set and test set.
Four datasets are divided into 2 parts only (development and test sets): eng.dep.covdtb and {eng,por,tur}.pdtb.tedm.
One dataset is only one part (test set): eng.rst.gentle.


## Directories
The shared task repository currently comprises the following directories:

* `data` - individual corpora from various languages and frameworks.
    * Folders are given names in the scheme `LANG.FRAMEWORK.CORPUS`, e.g. `eng.rst.gum` is the directory for the GUM corpus, which is in English and annotated in the framework of Rhetorical Structure Theory (RST).
    * Note that some corpora (eng.rst.rstdt, eng.pdtb.pdtb, tur.pdtb.tdb, zho.pdtb.cdtb) do not contain text or have some documents without text (eng.rst.gum) and text therefore needs to be reconstructed using `utils/process_underscores.py`.
* `utils` - scripts for validating, evaluating and generating data formats. The official scorer for the 3 tasks is `disrpt_eval.py`. See `usage` section for details.

See the README files in individual data directories for more details on each dataset.


## Usage
### Reconstruction of underscored data
* `process_underscore_2024.py` - text reconstruction of datasets under specific licenses.
    * Usage from `utils/`: `python process_underscore_2024.py -c {CORPUS,all} -m add`
    * Arguments required:
        * -c/--corpus {CORPUS,all} .... *Name of the corpus in the shape `LANG.FRAMEWORK.CORPUS` or 'all'(default).*
        * -m/--mode {add,del} .... *Chose 'add'(default) to replace underscores by text.*




### Evaluation
* `disrpt_eval_2024.py` - evaluation of 1 predictions file against 1 gold file.
    * Usage from `utils/`: `python disrpt_eval_2024.py [-h] -g GOLDFILE -p PREDFILE -t {S,C,R} [-s] [-nb] [-rt]`
    * Arguments required: 
        * -g/--goldfile GOLDFILE .... *Path to gold file.*
        * -p/--predfile PREDFILE .... *Path to predictions file.*
        * -t/--task {S,C,R} .... *Task to evaluate. S = "Discourse Unit Segmentation", C = "Connectives Identification", R = "Relations Classification".*
    * Options:
        * -s/--string_input .... *If inputs are strings instead of file path.*
        * -nb/--no_boundary_edu .... *Does not count EDU that starts at beginning of sentence, relevant for task S and format CONLLU only.*
        * -rt/--rel_type .... *Evaluate relation type instead of label, relevant for task R only.*
    * Output:
        * Results are print directly as STDout.



* `evaluation_main.sh` - evaluation of all predictions files organized in same directories structure than gold files: ...data/LANG.FRAMEWORK.CORPUS/LANG.FRAMEWORK.CORPUS_DIV.EXTENSION
    * Usage from `utils/`: `bash evaluation_main.sh -g GOLDDIR -p PREDDIR -o OUTDIR [-d] [-b] [-y] [-s]`
    * Arguments required:
        * -g/--gold_dir GOLDDIR .... *Path to parent gold directory (...latest/data).*
        * -p/--pred_dir PREDDIR .... *Path to parent predictions directory (.../data).*
        * -o/--out_eval_dir OUTDIR .... Path to output directory to print results files.*
    * Options:
        * -d/--division_set .... *Datasets division to evaluate to 'dev. Default='test' (DIV).*
        * -b/--no_boundary_edu .... *Option for TASK-1/.conllu. Evaluate only intra-sentential EDUs.*
        * -y/--rel_type .... *Option for TASK-3. Evaluate TYPES instead of LABELS (cf.PDTB) plus metrics for each type.*
        * -s, --string_input .... *Whether inputs are strings instead of file names.*
    * Output:
        * For each file evaluated, results are print into a file following this name convention : .../OUTDIR/LANG.FRAMEWORK.CORPUS_DIV.EXTENSION_eval

