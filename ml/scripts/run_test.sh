#!/bin/bash
set -e
set -x


SCRIPTS_DIR=$(dirname "$(readlink -f "$0")")
ROOT_DIR=${SCRIPTS_DIR}/../
DATA_DIR=${ROOT_DIR}/../data

PIPELINE_NAME="llm_hierarcial"


# FULL_DATA_CSV_FILE=${FULL_DATA_CSV_FILE:-$DATA_DIR/train_dataset_tag_video/baseline/train_data_categories.csv}
# VIDEOS_DIR=${VIDEOS_DIR:-$DATA_DIR/train_dataset_tag_video/videos}
# VIDEOS_PREP_DIR=${VIDEOS_PREP_DIR:-$DATA_DIR/data_prep/train_dataset_tag_video/videos}
DATA_PREP=true \
EVAL=false \
DEBUG=false \
PREDICT_ALL=true \
FULL_DATA_CSV_FILE=$DATA_DIR/train_dataset_tag_video/baseline/train_data_categories.csv \
PREDICT_VIDEOS_DIR=$DATA_DIR/test_tag_video/videos \
TRAIN_VIDEOS_DIR=$DATA_DIR/train_dataset_tag_video/videos \
TRAIN_DATA_CSV_FILE=$DATA_DIR/train_dataset_tag_video/baseline/train_data_categories.csv \
PREDICT_DATA_CSV_FILE=$DATA_DIR/test_tag_video/sample_submission.csv \
SUBMITION_DIR=$DATA_DIR/test_submits/$PIPELINE_NAME \
    bash $SCRIPTS_DIR/run.sh