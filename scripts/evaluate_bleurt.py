from evaluate import load
import numpy as np

def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=str, required=True)
    parser.add_argument("--references", type=str, required=True)
    return parser.parse_args()

def main():
    args = parse_arguments()

    bleurt = load("bleurt", module_type="metric")

    predictions = open(args.predictions, "r").readlines()
    references = open(args.references, "r").readlines()

    results = bleurt.compute(predictions=predictions, references=references)

    average_score = np.mean(results)

    print(average_score)

if __name__ == "__main__":
    main()
