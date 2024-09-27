#/bin/bash

set -e
set +x


ROOT_DIR=$(dirname "$(readlink -f "$0")")/../
source $ROOT_DIR/venv/bin/activate

DATA_DIR=$ROOT_DIR/..
TRAIN_DATA_CSV_FILE=$DATA_DIR/data/train_dataset_tag_video/baseline/train_data_categories.csv
TAXONOMY_FILE=$DATA_DIR/data/train_dataset_tag_video/baseline/IAB_tags.csv

PIPELINE_NAME="baseline"
SUBMITION_FILE=$DATA_DIR/data/submits/$PIPELINE_NAME/submission_$(date +"%Y-%m-%d_%H-%M-%S").csv

if [ "$PIPELINE_NAME" == "baseline" ]; then
    python3 $ROOT_DIR/scripts/pipelines/baseline.py \
        --submission_file $SUBMITION_FILE \
        --file_path_train $TRAIN_DATA_CSV_FILE \
        --file_path_iab $TAXONOMY_FILE \
        --generate-random
fi

# save submission file structure
GROUD_TRUTH_FILE=$TRAIN_DATA_CSV_FILE

python3 $ROOT_DIR/scripts/eval.py \
    --submission $SUBMITION_FILE \
    --ground-truth $GROUD_TRUTH_FILE