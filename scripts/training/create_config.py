#!/usr/bin/env python3

import argparse
import logging


YAML_CONFIG_TEMPLATE = """# Configuration file for training with the multimodalhugs framework.
# This file contains settings for the model, common experiment parameters,
# training hyperparameters, and dataset/data loading options.

model:
  # Model-specific settings:
  type: "multimodal_embedder"
  multimodal_mapper_type: "linear"                # Type of Multimodal Mapper (e.g., "linear" or "adapter").
  multimodal_mapper_layer_norm_before: true       # Whether to apply Layer Normalization before the Multimodal Mapper.
  multimodal_mapper_dropout: 0.1                  # Dropout probability for the Multimodal Mapper to prevent overfitting.
  backbone_type: {backbone_type}                  # Identifier for the pretrained backbone (e.g., "m2m_100").
  pretrained_backbone: {pretrained_backbone}      # Weights or checkpoint identifier for the pretrained backbone.
  feat_dim: 534                                   # Dimension of the Feature Extractor output. If features are extracted off-line, the dimentionality of features.

training:
  run_name: {run_name}                             # The name or identifier of the model configuration.
  early_stopping_patience: 10                      # Stop after there was no improvement after this many validation steps.
  do_train: True                                   # Whether to run training.
  do_eval: True                                    # Whether to run evaluation on the validation set.
  predict_with_generate: true                      # Use generate to compute generative metrics.
  save_strategy: "steps"                           # Checkpoint save strategy during training.
  eval_strategy: "steps"                           # Evaluation strategy ("steps" or "epoch").
  eval_steps: 128                                  # Number of training steps between evaluations.
  logging_steps: 128                               # Interval (in steps) at which training metrics are logged.
  save_steps: 128                                  # Interval (in steps) at which model checkpoints are saved.
  per_device_train_batch_size: {batch_size}                   # Batch size per device during training.
  per_device_eval_batch_size: {batch_size}                    # Batch size per device for evaluation.
  label_smoothing_factor: {label_smoothing_factor}
  gradient_accumulation_steps: {gradient_accumulation_steps}                   # Number of steps to accumulate gradients before weight updates.
  learning_rate: {learning_rate}                   # Initial learning rate for the optimizer.
  load_best_model_at_end: True                     # Load the best model found during training at the end.
  dataloader_num_workers: 2                        # Number of subprocesses to use for data loading; higher values speed up data loading but increase memory usage.
  dataloader_prefetch_factor: 2                    # Number of batches loaded in advance by each worker; total prefetched batches = num_workers * prefetch_factor.
  metric_name: sacrebleu, chrf                     # Name of the metric to use (any metric supported by evaluate.load()). If you want to use multiple metrics, structure the variable like: metric_name: '<metric_name_1>,<metric_name_2>,...'
  metric_for_best_model: 'sacrebleu'               # Metric used to determine the best model.
  greater_is_better: true
  num_train_epochs: 1                              # Number of full passes through the training dataset.
  max_steps: {max_steps}                           # Maximum number of training steps, e.g. 500000 (overrides num_train_epochs if set).
  warmup_steps: {warmup_steps}                     # Number of warmup steps to gradually increase the learning rate.
  save_total_limit: 10                             # Maximum number of checkpoints to retain (older ones are deleted).
  seed: 3435                                       # Random seed for reproducibility.
  fp16: True                                       # Enable mixed-precision (FP16) training for faster computation.
  # See the list of allowed arguments in https://huggingface.co/docs/transformers/v4.49.0/en/main_classes/trainer#transformers.Seq2SeqTrainingArguments

data:
  # Dataset and preprocessing settings:
  train_metadata_file: {train_metadata_file}                            # Path to the training metadata file (e.g., TSV format).
  validation_metadata_file: {validation_metadata_file}                  # Path to the validation metadata file.
  test_metadata_file: {test_metadata_file}                              # Path to the test metadata file.
  shuffle: True                                                                                                                 # Shuffle the dataset samples during loading.
  max_frames: 300                                                                                                               # Maximum number of frames to consider in video samples; samples exceeding this are filtered.

processor:
  reduce_holistic_poses: {reduce_holistic_poses}   # reduce the face mesh points of Mediapipe holistic poses (leading to fewer dimensions overall)
  text_tokenizer_path: {text_tokenizer_path}       # Path or identifier for the pretrained text tokenizer (e.g., "facebook/m2m100_418M").
  new_vocabulary: {new_vocabulary}                 # Comma-separated list of new tokens that will be added to the tokenizer. It can also be a Path to the file containing the new tokens that will be added to the tokenizer.
"""


def fill_template(args: argparse.Namespace) -> str:
    """

    :param args:
    :return:
    """
    if args.dry_run:
        max_steps = 10
    else:
        max_steps = 500000

    if args.new_vocabulary is not None:
        new_vocabulary_path = f"{args.config_dir}/new_vocabulary.txt"

        logging.debug(f"Writing new vocabulary to: '{new_vocabulary_path}'")

        with open(new_vocabulary_path, "w") as outhandle:
            outhandle.write("\n".join(args.new_vocabulary))
        args.new_vocabulary = new_vocabulary_path

    return YAML_CONFIG_TEMPLATE.format(
        run_name=args.run_name,
        train_metadata_file=args.train_metadata_file,
        validation_metadata_file=args.validation_metadata_file,
        test_metadata_file=args.test_metadata_file,
        backbone_type=args.backbone_type,
        pretrained_backbone=args.pretrained_backbone,
        reduce_holistic_poses=args.reduce_holistic_poses,
        max_steps=max_steps,
        text_tokenizer_path=args.text_tokenizer_path,
        new_vocabulary=args.new_vocabulary,
        learning_rate=args.learning_rate,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        warmup_steps=args.warmup_steps,
        batch_size=args.batch_size,
        label_smoothing_factor=args.label_smoothing_factor
    )

# Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Create YAML config file.")
    parser.add_argument("--run-name", type=str, help="The name or identifier of the model configuration.")
    parser.add_argument("--config-dir", type=str,
                        help="Path where the output config (and possibly new vocabulary file) "
                             "should be saved.")
    parser.add_argument("--train-metadata-file", type=str, help="Train TSV metadata file path.")
    parser.add_argument("--validation-metadata-file", type=str, help="Validation TSV metadata file path.")
    parser.add_argument("--test-metadata-file", type=str, help="Test TSV metadata file path.")

    parser.add_argument("--text-tokenizer-path", type=str, help="Text tokenizer identifier (default: facebook/m2m100_418M).",
                        default="facebook/m2m100_418M", required = False)
    parser.add_argument("--new-vocabulary", type=str, nargs="+", help="Strings to be added to tokenizer (default: None).",
                        default=None, required=False)

    parser.add_argument("--backbone-type", type=str, help="Identifier for the pretrained backbone (default: m2m_100).",
                        default="m2m_100", required=False)
    parser.add_argument("--pretrained-backbone", type=str, help="Weights or checkpoint identifier for the pretrained "
                                                                "backbone. (default: facebook/m2m100_418M).",
                        default="facebook/m2m100_418M", required=False)

    parser.add_argument("--reduce-holistic-poses", action="store_true", default=False,
                        help="Reduce holistic poses (default: False).", required=False)

    parser.add_argument("--learning-rate", type=float, help="The initial learning rate for AdamW optimizer (default: 5e-05).",
                        default=5e-05, required=False)
    parser.add_argument("--gradient-accumulation-steps", type=int, help=" Number of updates steps to accumulate the gradients for, before performing a backward/update pass.",
                        default=1, required=False)
    parser.add_argument("--warmup-steps", type=int, help="Number of steps used for a linear warmup from 0 to learning_rate. ",
                        default=0, required=False)
    parser.add_argument("--batch-size", type=int,
                        help="The batch size per GPU/XPU/TPU/MPS/NPU core/CPU for training / evaluation.",
                        default=8, required=False)
    parser.add_argument("--label-smoothing-factor", type=float,
                        help="The label smoothing factor to use. Zero means no label smoothing.",
                        default=0.0, required=False)

    parser.add_argument("--dry-run", action="store_true", default=False,
                        help="Train for a small number of steps.", required=False)
    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_arguments()

    logging.basicConfig(level=logging.DEBUG)
    logging.debug(args)

    filled_template = fill_template(args)

    config_path = f"{args.config_dir}/config_{args.run_name}.yaml"

    logging.debug(f"Writing config to: '{config_path}'")

    with open(config_path, "w") as outhandle:
        outhandle.write(filled_template)


if __name__ == "__main__":
    main()