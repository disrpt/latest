# eng.pdtb.gum

### The Georgetown University Multilayer (GUM) Corpus - PDTB-style annotations

To cite this corpus, please refer to the following article:

Zeldes, Amir (2017) "The GUM Corpus: Creating Multilayer Resources in the Classroom". 
Language Resources and Evaluation 51(3), 581–612.

```bibtex
@Article{Zeldes2017,
   author    = {Amir Zeldes},
   title     = {The {GUM} {C}orpus: Creating Multilayer Resources in the Classroom},
   journal   = {Language Resources and Evaluation},
   year      = {2017},
   volume    = {51},
   number    = {3},
   pages     = {581--612},
   doi       = {http://dx.doi.org/10.1007/s10579-016-9343-x}
 }
```

## Introduction

GUM is a growing corpus of English texts currently covering 16 text types, each coded using a code within document names:

- academic - Academic writing from Creative Commons sources
- bio - Biographies from Wikipedia
- conversation - Face-to-face conversations from the Santa Barbara Corpus
- court - Courtroom oral transcripts
- essay - Argumentative essays
- fiction - Fiction from Creative Commons sources
- interview - Interviews from Wikimedia
- letter - Private letters and other forms of paper-written (non-e-mail) correspondence
- news - News from Wikinews
- podcast - Podcast recording transcripts
- reddit - Online forum discussions from Reddit
- speech - Political speeches
- textbook - OpenStax open access textbooks
- vlog - YouTube Creative Commons vlogs
- voyage - Travel guides from Wikivoyage
- whow - How-to guides from wikiHow

The corpus is created as part of the course LING-4427 (Computational Corpus Linguistics) at Georgetown University. Data is annotated in the enhanced RST (eRST) formalism, described in [this paper](https://arxiv.org/abs/2403.13560). While eRST annotations are contained in the folder `data/eng.erst.gum/`, this folder contains PDTB-style connective annotations for the connective detection task.

For more details see: https://gucorpling.org/gum

## DISRPT 2023 Shared Task Information

For the DISRPT 2023 shared task on elementary discourse unit segmentation, 
only 11 open text genres were included with plain text, while the remaining twelfth genre, 
containing Reddit forum discussions, **must be reconstructed** using the script 
in `utils/process_underscore_2024.py` (see main repository README).  
Following the 2023 shared task, four more genres were added (court, essay, letter and 
podcast were not included in 2023).

The data follows the established `train`, `dev`, and `test` partitions used for other tasks 
(e.g. for the conll shared task on UD parsing), which can be found [here](https://github.com/amir-zeldes/gum/blob/master/splits.md). 

POS tags and syntactic parses are manually annotated gold data. 

### Notes on Connectives

GUM eRST guidelines follow PDTB guidelines for the identification of connectives with two small but important differences:

1. Since eRST recognizes some non-sentential fragments as discourse units, in accordance with the RST-DT EDU segmentation guidelines, some instances of adnominal prepositions (e.g. "because of", "despite" + NOUN) are considered connectives in the eng.pdtb.gum data, but would not be considered connectives in eng.pdtb.pdtb
2. While PDTB recognizes connective modifiers as part of the connective, eRST signaling annotation does not. As a result, the string "six months later" may be considered a connective in eng.pdtb.pdtb, but in eng.pdtb.gum only the word "later" will be annotated as a connective.

Also note that the `.conllu` data contains some reconstructed ellipsis tokens with 
decimal IDs (e.g. 12.1); these do not appear in the other formats and are ignored in token 
index spans.

More GUM guidelines can be found [here](https://wiki.gucorpling.org/gum/rst). 