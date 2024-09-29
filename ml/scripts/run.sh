#/bin/bash

set -e
set -x


# submit file needed to be passed
# PIPELINE_NAME="submit"
# PIPELINE_NAME="baseline"
PIPELINE_NAME="llm_hierarcial"

DATA_PREP=${DATA_PREP:-false}
EVAL=${EVAL:-true}
DEBUG=${DEBUG:-false}
PREDICT_ALL=${PREDICT_ALL:-false}
USE_S2T=${USE_S2T:-false}


# need big gpu
# MODEL_TYPE="hf"
HF_MODEL_NAME=unsloth/Llama-3.2-1B-Instruct

# easy testing
MODEL_TYPE="openrouter" # vllm variant too
OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-none}  # vllm variant too
OPENAPI_API_KEY=$OPENROUTER_API_KEY

OPENROUTER_BASE_URL=${OPENROUTER_BASE_URL:-https://openrouter.ai/api/v1/}  # vllm variant too
OPENROUTER_MODEL_NAME=${OPENROUTER_MODEL_NAME:-meta-llama/llama-3.1-70b-instruct}

ROOT_DIR=$(dirname "$(readlink -f "$0")")/../
DATA_DIR=$ROOT_DIR/../data

FULL_DATA_CSV_FILE=${FULL_DATA_CSV_FILE:-$DATA_DIR/train_dataset_tag_video/baseline/train_data_categories.csv}
# same set
TRAIN_VIDEOS_DIR=${VIDEOS_DIR:-$DATA_DIR/train_dataset_tag_video/videos}
PREDICT_VIDEOS_DIR=${VIDEOS_DIR:-$DATA_DIR/train_dataset_tag_video/videos}
VIDEOS_PREP_DIR=${VIDEOS_PREP_DIR:-$DATA_DIR/data_prep/}

# we use filtered target to get more accurate classes
# TAXONOMY_FILE=$DATA_DIR/train_dataset_tag_video/baseline/IAB_tags.csv
TRAIN_DATA_CSV_FILE=${TRAIN_DATA_CSV_FILE:-$DATA_DIR/split/train.csv}
PREDICT_DATA_CSV_FILE=${PREDICT_DATA_CSV_FILE:-$DATA_DIR/split/val.csv}
SUBMITION_DIR=${SUBMITION_DIR:-$DATA_DIR/submits/$PIPELINE_NAME}
SUBMITION_FILE=$SUBMITION_DIR/submission_$(date +"%Y-%m-%d_%H-%M-%S").csv


source $ROOT_DIR/venv/bin/activate
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


if [ "${DATA_PREP}" == "true" ]; then
    # could be long
    echo "data prep s2t"
    if [ ! -d "$VIDEOS_PREP_DIR/s2t/" ]; then
        mkdir -p $VIDEOS_PREP_DIR/s2t/
        python3 $ROOT_DIR/scripts/extract_text_from_video.py \
            --input_path $VIDEOS_DIR \
            --texts_output_path $VIDEOS_PREP_DIR/s2t/ \
            --max_minutes 5
    fi

    echo "data prep video_desc"
    if [ ! -d "$VIDEOS_PREP_DIR/video_desc/" ]; then
        mkdir -p $VIDEOS_PREP_DIR/video_desc/
        python3 $ROOT_DIR/scripts/process_video.py \
            --input $TRAIN_VIDEOS_DIR \
            --output_dir $VIDEOS_PREP_DIR/video_desc/

        python3 $ROOT_DIR/scripts/process_video.py \
            --input $PREDICT_VIDEOS_DIR \
            --output_dir $VIDEOS_PREP_DIR/video_desc/
    fi
fi

# test pipe
if [ "$PIPELINE_NAME" == "baseline" ]; then
    python3 $ROOT_DIR/scripts/pipelines/baseline.py \
        --submission_file $SUBMITION_FILE \
        --file_path_train $PREDICT_DATA_CSV_FILE \
        --file_path_iab $TAXONOMY_FILE
fi

if [ "$PIPELINE_NAME" == "llm_hierarcial" ]; then
    PYTHONPATH=$ROOT_DIR python3 $ROOT_DIR/scripts/pipelines/llm_hierarcial.py \
        --submission_file $SUBMITION_FILE \
        --file_path_train $TRAIN_DATA_CSV_FILE \
        --file_path_predict $PREDICT_DATA_CSV_FILE \
        --file_path_iab $TAXONOMY_FILE \
        --hf-model-name $HF_MODEL_NAME \
        --openrouter-model-name $OPENROUTER_MODEL_NAME \
        --model-type $MODEL_TYPE \
        --train_video_desc_dir $VIDEOS_PREP_DIR/video_desc/ \
        --predict_video_desc_dir $VIDEOS_PREP_DIR/video_desc/ \
        $([ "${USE_S2T}" == "true" ] && echo --predict_s2t_dir $VIDEOS_PREP_DIR/s2t/) \
        $([ "${DEBUG}" == "true" ] && echo --debug) \
        $([ "${PREDICT_ALL}" == "true" ] && echo --predict-all) \
    ;
    # todo:
fi



if [ "${EVAL}" == "true" ] && [ -f "$SUBMITION_FILE" ]; then
    # save submission file structure
    GROUD_TRUTH_FILE=$PREDICT_DATA_CSV_FILE

    python3 $ROOT_DIR/scripts/eval.py \
        --submission $SUBMITION_FILE \
        --ground-truth $GROUD_TRUTH_FILE
else
    echo "Submission file does not exist. Exiting."
    exit 1
fi
