"""
Preprocessing adapted from code2seq (https://github.com/tech-srl/code2seq).
Can be used with any of the preprocessed datasets generated by preprocess-1.py
This takes a stage1 preprocessed dataset (which contains ASTs) and runs code2seq's preprocessing pipeline to obtain
the dataset format that can be directly fed into code2seq. This was used to obtain comparison results for code2seq on
the CSN dataset.
"""
import argparse
import itertools
import os

from joblib import parallel_backend, Parallel, delayed

from code_transformer.preprocessing.pipeline.code2seq import __collect_samples
from code_transformer.preprocessing.pipeline.stage1 import CTStage1Sample
from code_transformer.preprocessing.datamanager.preprocessed import CTBufferedDataManager
from code_transformer.utils.io import create_directories
from code_transformer.utils.log import get_logger
from code_transformer.utils.timing import Timing

parser = argparse.ArgumentParser()
parser.add_argument("language", type=str)
parser.add_argument("partition", type=str)
parser.add_argument("input_data_path", type=str)
parser.add_argument("output_data_path", type=str)
parser.add_argument("--max_path_length", type=int, default=8)
parser.add_argument("--max_path_width", type=int, default=2)
parser.add_argument("--use_method_name", type=bool, default=True)
parser.add_argument("--use_nums", type=bool, default=True)

logger = get_logger(__file__)
args = parser.parse_args()

input_data_path = args.input_data_path
output_data_path = args.output_data_path
language = args.language
partition = args.partition

NUM_PROCESSES = 15
LOG_EVERY = 10000
BATCH_SIZE = 10
RANDOM_SEED = 123

data_manager = CTBufferedDataManager(input_data_path, language, partition=partition)


def process_batch(batch, args):
    batch = [CTStage1Sample.from_compressed(sample) for sample in batch]
    processed_samples = []
    for sample in batch:
        for node in sample.ast.nodes.values():
            node.value = node.source_span.substring(sample.stripped_code_snippet)
        # Sometimes, method names contain extra garbage in Ruby, e.g., Github.Client::Say.say
        # We only want the last part of the function name in this case
        func_name = sample.func_name.split(".")[-1]
        processed_samples.extend(__collect_samples(sample.ast, args, language, func_name=func_name))
    return processed_samples


with parallel_backend("loky") as parallel_config:
    execute_parallel = Parallel(NUM_PROCESSES, verbose=0)
    batched_samples_generator = data_manager.read(BATCH_SIZE)

    samples = []
    while True:
        dataset_slice = itertools.islice(batched_samples_generator, int(LOG_EVERY / BATCH_SIZE))
        with Timing() as t:
            dataset = execute_parallel(delayed(process_batch)(batch, args) for batch in dataset_slice)

        if dataset:
            # dataset = [sample for batch in dataset for sample in batch]  # List[batches] -> List[samples]
            dataset = list(itertools.chain.from_iterable(dataset))
            logger.info(
                f"processing {len(dataset)} samples took {t[0]:0.2f} seconds ({t[0] / len(dataset):0.3f} seconds per "
                f"sample)"
            )
            samples.extend(dataset)
        else:
            break

    output_file = f"{output_data_path}/{language}/{partition}.txt"
    create_directories(output_file)
    with open(output_file, "w") as f:
        for line_index, line in enumerate(samples):
            f.write(line + ("" if line_index == len(samples) - 1 else "\n"))

data_manager.shutdown()
logger.info("PREPROCESS-1 DONE!")

os._exit(1)
