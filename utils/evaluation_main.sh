# main script to run evaluation


export GOLD_DIR=/home/lriviere/disrpt_lau/latest/data # mettre en argument
export PRED_DIR=/home/lriviere/disrpt_lau/latest/data # mettre en argument
export EVAL_DIR=/home/lriviere/disrpt_lau/lrec24/disrpt/scripts/eval_test # mettre en argument
export PART="test" #"dev" # mettre en argument
# TODO mettre en argument les options pour chaque cas.....




# DISRPT TASK-1: EDUS SEGMENTATION ###################################################
# RST, SDRT, DEP datasets.

for dataset in deu.rst.pcc #eng.dep.covdtb eng.dep.scidtb eng.rst.gum eng.rst.rstdt eng.sdrt.stac eus.rst.ert fas.rst.prstc fra.sdrt.annodis ita.pdtb.luna nld.rst.nldt p or.rst.cstn rus.rst.rrt spa.rst.rststb spa.rst.sctb zho.dep.scidtb zho.rst.gcdt zho.rst.sctb 

do
    export DATASET_NAME=${dataset}

    file_output=$EVAL_DIR"/"$DATASET_NAME"_"$PART".tok_eval"
    echo "Processing $file_output..."
    output=$(python disrpt_eval_2024.py -g $GOLD_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".tok" -p $PRED_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".tok" -t S) 
    #-s 
    echo "$output" > $file_output

    file_output=$EVAL_DIR"/"$DATASET_NAME"_"$PART".conllu_eval" 
    echo "Processing $file_output..."
    output=$(python disrpt_eval_2024.py -g $GOLD_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".conllu" -p $PRED_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".conllu" -t S) 
    #-s -nb
    echo "$output" > $file_output
done



# DISRPT TASK-2: CONNECTIVES IDENTIFICATION ###################################################
# PDTB datasets

for dataset in eng.pdtb.gum #eng.pdtb.pdtb eng.pdtb.tedm ita.pdtb.luna por.pdtb.crpc por.pdtb.tedm tha.pdtb.tdtb tur.pdtb.tdb tur.pdtb.tedm zho.pdtb.cdtb

do
    export DATASET_NAME=${dataset}

    file_output=$EVAL_DIR"/"$DATASET_NAME"_"$PART".tok_eval" 
    echo "Processing $file_output..."
    output=$(python disrpt_eval_2024.py -g $GOLD_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".tok" -p $PRED_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".tok" -t C) 
    #-s
    echo "$output" > $file_output

    file_output=$EVAL_DIR"/"$DATASET_NAME"_"$PART".conllu_eval" 
    echo "Processing $file_output..."
    output=$(python disrpt_eval_2024.py -g $GOLD_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".conllu" -p $PRED_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".conllu" -t C) 
    #-s
    echo "$output" > $file_output
done



# DISRPT TASK-3: RELATIONS CLASSIFICATION ###################################################
# All datasets

for dataset in deu.rst.pcc #eng.dep.covdtb eng.dep.scidtb eng.pdtb.gum eng.pdtb.pdtb eng.pdtb.tedm eng.rst.gum eng.rst.rstdt eng.sdrt.stac eus.rst.ert fas.rst.prstc fra.sdrt.annodis ita.pdtb.luna nld.rst.nldt por.pdtb.crpc por.pdtb.tedm por.rst.cstn rus.rst.rrt spa.rst.rststb spa.rst.sctb tha.pdtb.tdtb tur.pdtb.tdb tur.pdtb.tedm zho.dep.scidtb zho.pdtb.cdtb zho.rst.gcdt zho.rst.sctb 

do 
    export DATASET_NAME=${dataset}

    file_output=$EVAL_DIR"/"$DATASET_NAME"_"$PART".rels_eval" 
    echo "Processing $file_output..."
    output=$(python disrpt_eval_2024.py -g $GOLD_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".rels" -p $PRED_DIR"/"$DATASET_NAME"/"$DATASET_NAME"_"$PART".rels" -t R) 
    #-s -rt
    echo "$output" > $file_output
done

