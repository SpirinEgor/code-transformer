import pickle
from argparse import ArgumentParser
from asyncio import create_task, run, get_event_loop, get_running_loop
from concurrent.futures import ThreadPoolExecutor
from glob import glob
from os import mkdir, cpu_count
from os.path import join, split, exists
from shutil import rmtree
from typing import List

from tqdm import tqdm

from code_transformer.env import DATA_PATH_STAGE_2
from code_transformer.preprocessing.pipeline.stage2 import CTStage2Sample
from code_transformer.utils.io import load_zipped, save_zipped

HOLDOUT_NAMES = ["train", "valid", "test"]


async def unpack_file(data: List[CTStage2Sample], output_dir: str):
    if exists(output_dir):
        files = glob(join(output_dir, "datapoint-*.p.gzip"))
        if len(files) == len(data):
            return
        else:
            rmtree(output_dir)
    mkdir(output_dir)
    output_names = [join(output_dir, f"datapoint-{i}.p.gzip") for i in range(len(data))]
    pbar = tqdm(total=len(data), leave=False)

    def store(datapoint, output_path):
        save_zipped(datapoint, output_path)
        pbar.update(1)

    loop = get_running_loop()
    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        coros = [loop.run_in_executor(executor, store, d, op) for d, op in zip(data, output_names)]
        for coro in coros:
            await coro

    pbar.close()


async def load_zipped_async(filepath: str) -> List[CTStage2Sample]:
    return load_zipped(filepath)


async def unpack_holdout(holdout_dir: str):
    files = glob(join(holdout_dir, "dataset-*.p.gzip"))
    holdout_name = split(holdout_dir)[-1]
    data = load_zipped(files[0])

    task = None
    for i, file in tqdm(enumerate(files), total=len(files), desc=holdout_name):
        folder_name = split(file)[-1].split(".", 1)[0]
        folder_dir = join(holdout_dir, folder_name)

        if i != len(files) - 1:
            task = create_task(load_zipped_async(files[i + 1]))

        await unpack_file(data, folder_dir)
        if i != len(files) - 1:
            data = await task


def main(dataset_name: str):
    dataset_dir = join(DATA_PATH_STAGE_2, dataset_name)
    for holdout_name in HOLDOUT_NAMES:
        run(unpack_holdout(join(dataset_dir, holdout_name)))


if __name__ == "__main__":
    __arg_parser = ArgumentParser()
    __arg_parser.add_argument("--data", help="stage2 dataset name", required=True)

    __args = __arg_parser.parse_args()
    main(__args.data)
