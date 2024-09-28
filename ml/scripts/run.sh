#/bin/bash

set -e
set +x


ROOT_DIR=$(dirname "$(readlink -f "$0")")/../
source $ROOT_DIR/venv/bin/activate

DATA_DIR=$ROOT_DIR/../data

DEBUG=${DEBUG:-false}
PREDICT=${PREDICT:-false}

FULL_DATA_CSV_FILE=$DATA_DIR/train_dataset_tag_video/baseline/train_data_categories.csv

# we use filtered target to get more accurate classes
# TAXONOMY_FILE=$DATA_DIR/train_dataset_tag_video/baseline/IAB_tags.csv

# create new taxonomy
TAXONOMY_FILE=$DATA_DIR/data_prep/filtered_taxonomy.csv
python3 $ROOT_DIR/scripts/data_prep/create_new_taxonomy.py \
    --train_csv_path $FULL_DATA_CSV_FILE \
    --save_new_taxonomy_path $TAXONOMY_FILE \
    --class_drop_threshold 0.05 \
    --class_min_samples 2

# split full data
python3 $ROOT_DIR/scripts/split.py \
    --input_file $FULL_DATA_CSV_FILE \
    --output_dir $DATA_DIR/split \
    --fraction 0.85 \
    --seed 1337


TRAIN_DATA_CSV_FILE=$DATA_DIR/split/train.csv
PREDICT_DATA_CSV_FILE=$DATA_DIR/split/val.csv

# PIPELINE_NAME="submit"
# PIPELINE_NAME="baseline"
PIPELINE_NAME="llm_hierarcial"

SUBMITION_FILE=${SUBMITION_FILE:-$DATA_DIR/submits/$PIPELINE_NAME/submission_$(date +"%Y-%m-%d_%H-%M-%S").csv}

if [ "$PIPELINE_NAME" == "baseline" ]; then
    PYTHONPATH=$ROOT_DIR python3 $ROOT_DIR/scripts/pipelines/baseline.py \
        --submission_file $SUBMITION_FILE \
        --file_path_train $PREDICT_DATA_CSV_FILE \
        --file_path_iab $TAXONOMY_FILE \
        --generate-random
fi

if [ "$PIPELINE_NAME" == "llm_hierarcial" ]; then
    PYTHONPATH=$ROOT_DIR python3 $ROOT_DIR/scripts/pipelines/llm_hierarcial.py \
        --submission_file $SUBMITION_FILE \
        --file_path_train $TRAIN_DATA_CSV_FILE \
        --file_path_predict $PREDICT_DATA_CSV_FILE \
        --file_path_iab $TAXONOMY_FILE \
        --hf-model-name unsloth/Llama-3.2-1B-Instruct \
        --model-type openrouter \
        $([ "$DEBUG" == true ] && echo --debug) \
        $([ "$PREDICT" == true ] && echo --predict-all) \
    ;
fi


if [ -f "$SUBMITION_FILE" ]; then
    # save submission file structure
    GROUD_TRUTH_FILE=$PREDICT_DATA_CSV_FILE

    python3 $ROOT_DIR/scripts/eval.py \
        --submission $SUBMITION_FILE \
        --ground-truth $GROUD_TRUTH_FILE
else
    echo "Submission file does not exist. Exiting."
    exit 1
fi