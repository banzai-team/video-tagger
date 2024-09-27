import pandas as pd
import argparse
import ast
import numpy as np


def iou_metric(ground_truth, predictions):
    iou =  len(set.intersection(set(ground_truth), set(predictions)))
    iou = iou/(len(set(ground_truth).union(set(predictions))))
    return iou

def split_tags(tag_list):
    final_tag_list = []
    for tag in tag_list:
        tags = tag.split(": ")
        if len(tags) == 3:
            final_tag_list.append(tags[0])
            final_tag_list.append(tags[0] + ": " + tags[1])
            final_tag_list.append(tags[0]+ ": " + tags[1] + ": " + tags[2])
        elif len(tags) == 2:
            final_tag_list.append(tags[0])
            final_tag_list.append(tags[0] + ": " + tags[1])
        elif len(tags) == 1:
            final_tag_list.append(tags[0])
        else:
            print("NOT IMPLEMENTED!!!!", tag)
    return final_tag_list


def find_iou_for_sample_submission(pred_submission, true_submission):
    ground_truth_df = true_submission
    ground_truth_df["tags"] = ground_truth_df["tags"].apply(lambda l: str(l).split(', '))
    ground_truth_df["tags_split"] = ground_truth_df["tags"].apply(lambda l: split_tags(l))

    predictions_df = pred_submission
    predictions_df["predicted_tags"] = predictions_df["predicted_tags"].apply(ast.literal_eval)
    predictions_df["predicted_tags_split"] = predictions_df["predicted_tags"].apply(lambda l: split_tags(l))
    iou=0
    counter = 0
    for i, row in ground_truth_df.iterrows():
        predicted_tags = predictions_df[predictions_df["video_id"]==row["video_id"]]["predicted_tags_split"].values[0]
        iou_temp=iou_metric(row['tags_split'], predicted_tags)
        iou+=iou_temp
        counter+=1

    return iou/counter


def main(args):
    sample_submission = pd.read_csv(args.submission)
    ground_truth = pd.read_csv(args.ground_truth)
    assert 'predicted_tags' in sample_submission
    assert 'predicted_tags' not in ground_truth

    try:
        pred_submission = sample_submission #pd.read_csv(pred_path, sep = ',')
    except Exception:
        assert False, 'Ошибка при загрузке решения участника'
    try:
        true_submission = ground_truth #pd.read_csv(true_path, sep = ',')
    except Exception:
        assert False, 'Ошибка при загрузке эталонного решения'


    final_score = find_iou_for_sample_submission(pred_submission, true_submission)
    print("FINAL_SCORE", final_score)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Evaluation script')
    parser.add_argument('--submission', type=str, help='Path to submission file')
    parser.add_argument('--ground-truth', type=str, help='Path to ground truth file')
    args = parser.parse_args()
    main(args)