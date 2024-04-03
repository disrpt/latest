# main script to run evaluation


export GOLD_DIR=/home/lriviere/disrpt_lau/latest/data
export PRED_DIR=/home/lriviere/disrpt_lau/my_cool_predictions/data
export EVAL_DIR=/home/lriviere/disrpt_lau/evaluation_results/
export PART="test" #"dev" 




# DISRPT TASK-1: EDUS SEGMENTATION ###################################################
# RST, SDRT, DEP datasets.

for dataset in deu.rst.pcc eng.dep.covdtb eng.dep.scidtb eng.rst.gum eng.rst.rstdt eng.sdrt.stac eus.rst.ert fas.rst.prstc fra.sdrt.annodis ita.pdtb.luna nld.rst.nldt p or.rst.cstn rus.rst.rrt spa.rst.rststb spa.rst.sctb zho.dep.scidtb zho.rst.gcdt zho.rst.sctb 

do
    export DATASET_NAME=${dataset}

    python disrpt_eval_2024.py -g $GOLD_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".tok" -p $PRED_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".tok" -t S > $EVAL_DIR"/"$DATASET_NAME"_"$PART".tok_eval" #-s 

    python disrpt_eval_2024.py -g $GOLD_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".conllu" -p $PRED_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".conllu" -t S > $EVAL_DIR"/"$DATASET_NAME"_"$PART".conllu_eval" #-s -nb
done



# DISRPT TASK-2: CONNECTIVES IDENTIFICATION ###################################################
# PDTB

for dataset in eng.pdtb.gum eng.pdtb.pdtb eng.pdtb.tedm ita.pdtb.luna por.pdtb.crpc por.pdtb.tedm tha.pdtb.tdtb tur.pdtb.tdb tur.pdtb.tedm zho.pdtb.cdtb

do
    export DATASET_NAME=${dataset}

    python disrpt_eval_2024.py -g $GOLD_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".tok" -p $PRED_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".tok" -t C > $EVAL_DIR"/"$DATASET_NAME"_"$PART".tok_eval" #-s

    python disrpt_eval_2024.py -g $GOLD_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".conllu" -p $PRED_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".conllu" -t C > $EVAL_DIR"/"$DATASET_NAME"_"$PART".conllu_eval" #-s
done



# DISRPT TASK-2: RELATIONS CLASSIFICATION ###################################################
# All datasets

for dataset in deu.rst.pcc eng.dep.covdtb eng.dep.scidtb eng.pdtb.gum eng.pdtb.pdtb eng.pdtb.tedm eng.rst.gum eng.rst.rstdt eng.sdrt.stac eus.rst.ert fas.rst.prstc fra.sdrt.annodis ita.pdtb.luna nld.rst.nldt por.pdtb.crpc por.pdtb.tedm por.rst.cstn rus.rst.rrt spa.rst.rststb spa.rst.sctb tha.pdtb.tdtb tur.pdtb.tdb tur.pdtb.tedm zho.dep.scidtb zho.pdtb.cdtb zho.rst.gcdt zho.rst.sctb 

do 
    export DATASET_NAME=${dataset}

    python disrpt_eval_2024.py -g $GOLD_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".rels" -p $PRED_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".rels" -t R > $EVAL_DIR"/"$DATASET_NAME"_"$PART".rels_eval" #-s -rt
done

