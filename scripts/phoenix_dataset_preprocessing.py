#!/usr/bin/env python3

import os
import argparse
import itertools
import pandas as pd

import tensorflow as tf
import tensorflow_datasets as tfds
import sign_language_datasets.datasets
from sign_language_datasets.datasets.config import SignDatasetConfig

from typing import Iterator, Optional, Dict, Union, List


# Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Process and transform a CSV file.")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file.")
    parser.add_argument("pose_directory", type=str, help="Path to the pose files.")
    parser.add_argument("output_file", type=str, help="Path to the output CSV file.")
    parser.add_argument("--encoder_prompt", type=str, default="__dgs__", help="encoder prompt string.")
    parser.add_argument("--decoder_prompt", type=str, default="__de__", help="decoder prompt string.")

    parser.add_argument("--tfds-data-dir", type=str, default=None,
                        help="TFDS data folder to cache downloads.", required=False)
    return parser.parse_args()


def load_dataset(data_dir: Optional[str] = None):
    """
    :param data_dir:
    :return:
    """

    config = SignDatasetConfig(name="rwth_phoenix2014_t",
                               version="3.0.0",
                               include_video=False,
                               process_video=False,
                               fps=25,
                               include_pose="holistic")

    rwth_phoenix2014_t = tfds.load('rwth_phoenix2014_t', builder_kwargs=dict(config=config), data_dir=data_dir)

    return rwth_phoenix2014_t


Example = Dict[str, str]


def generate_examples(dataset: tf.data.Dataset,
                      split_name: str) -> Iterator[Example]:
    """
    :param dataset:
    :param split_name: "train", "validation" or "test"
    :return:
    """

    for datum in dataset[split_name]:

        datum_id = datum["id"].numpy().decode('utf-8')

        text = datum['text'].numpy().decode('utf-8')

        data_buffer = open("file.pose", "wb")

        datum['pose']['data'].numpy()
        datum['pose']['conf'].numpy()

        fps = int(datum['pose']['fps'].numpy())

        for sentence_id, sentence in enumerate(sentences):



            video_info = {"filepath": video_filepath, "fps": fps,
                          "start_frame": start_frame, "end_frame": end_frame}

            example = {"split_name": split_name,
                       "file_id": datum_id,
                       "participant": participant,
                       "sentence_id": str(sentence_id).zfill(5),
                       "gloss_sequence": gloss_sequence,
                       "german_sentence": german_sentence,
                       "video_info": video_info}

            yield example


# Placeholder functions for constructing new fields
def leave_blank(row):
    return ""


def set_as_0(row):
    return 0


def construct_encoder_prompt(row, encoder_prompt):
    return encoder_prompt


def construct_decoder_prompt(row, decoder_prompt):
    return decoder_prompt


def map_column_to_new_field(original_column, new_column_name, data):
    if original_column in data.columns:
        data[new_column_name] = data[original_column]
    else:
        data[new_column_name] = ""  # Fill with empty if column does not exist


def main():
    # Parse arguments
    args = parse_arguments()

    if os.path.exists(args.output_file):
        print(f"Output file '{args.output_file}' already exists. The script will not overwrite it.")
        exit(0)

    # Read the input CSV file
    data = pd.read_csv(args.input_file, delimiter="\t")

    # Create new columns using the placeholder functions
    data['signal'] = data.apply(leave_blank, axis=1)
    data['signal_start'] = data.apply(set_as_0, axis=1)
    data['signal_end'] = data.apply(set_as_0, axis=1)
    data['encoder_prompt'] = data.apply(lambda row: construct_encoder_prompt(row, args.encoder_prompt), axis=1)
    data['decoder_prompt'] = data.apply(lambda row: construct_decoder_prompt(row, args.decoder_prompt), axis=1)
    data['output'] = data.apply(leave_blank, axis=1)

    # Example of mapping original columns to new ones
    map_column_to_new_field('SENTENCE_NAME', 'signal', data)
    map_column_to_new_field('SENTENCE', 'output', data)

    data['signal'] = data['signal'].apply(lambda x: f"{args.pose_directory}/{x}.pose")

    # Select the desired columns for the new dataset
    output_columns = [
        'signal',
        'signal_start',
        'signal_end',
        'encoder_prompt',
        'decoder_prompt',
        'output'
    ]

    # Save the transformed dataset to a new file, determining format by extension
    if args.output_file.endswith('.tsv'):
        data[output_columns].to_csv(args.output_file, sep='\t', index=False)
    else:
        data[output_columns].to_csv(args.output_file, index=False)

    print(f"Transformed dataset saved to {args.output_file}")


if __name__ == "__main__":
    main()