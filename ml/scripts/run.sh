#/bin/bash

set -e
set +x


ROOT_DIR=$(dirname "$(readlink -f "$0")")/../
source $ROOT_DIR/venv/bin/activate

DATA_DIR=$ROOT_DIR/../data
# TRAIN_DATA_CSV_FILE=$DATA_DIR/train_dataset_tag_video/baseline/train_data_categories.csv
# python3 $ROOT_DIR/scripts/split.py --input_file $TRAIN_DATA_CSV_FILE --output_dir $DATA_DIR/split --fraction 0.85 --seed 1337

TRAIN_DATA_CSV_FILE=$DATA_DIR/split/val.csv

TAXONOMY_FILE=$DATA_DIR/train_dataset_tag_video/baseline/IAB_tags.csv

# PIPELINE_NAME="baseline"
PIPELINE_NAME="llm_hierarcial"
SUBMITION_FILE=$DATA_DIR/submits/$PIPELINE_NAME/submission_$(date +"%Y-%m-%d_%H-%M-%S").csv

if [ "$PIPELINE_NAME" == "baseline" ]; then
    PYTHONPATH=$ROOT_DIR python3 $ROOT_DIR/scripts/pipelines/baseline.py \
        --submission_file $SUBMITION_FILE \
        --file_path_train $TRAIN_DATA_CSV_FILE \
        --file_path_iab $TAXONOMY_FILE \
        --generate-random
fi

if [ "$PIPELINE_NAME" == "llm_hierarcial" ]; then
    PYTHONPATH=$ROOT_DIR python3 $ROOT_DIR/scripts/pipelines/llm_hierarcial.py \
        --submission_file $SUBMITION_FILE \
        --file_path_train $TRAIN_DATA_CSV_FILE \
        --file_path_iab $TAXONOMY_FILE \
        --hf-model-name unsloth/Llama-3.2-1B-Instruct \
        --predict-all
fi

# # save submission file structure
# GROUD_TRUTH_FILE=$TRAIN_DATA_CSV_FILE

# python3 $ROOT_DIR/scripts/eval.py \
#     --submission $SUBMITION_FILE \
#     --ground-truth $GROUD_TRUTH_FILE