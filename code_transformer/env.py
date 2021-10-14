"""
Per default, we assume the following folder structure:
CODE_TRANSFORMER_DATA_PATH
 ├── raw
 │   ├── csn
 │   │   ├── python
 │   │   │   └── final
 │   │   │       └── ...
 │   │   :
 │   │   └── go
 │   ├── code2seq
 │   │   └── java-small
 │   └── code2seq-methods
 │       └── java-small
 ├── stage1
 └── stage2
     ├── python
     │   ├── train
     │   ├── valid
     │   ├── test
     │   └── vocabularies.p.gzip
     ├── java-small
     :
     └── python,javascript,go,ruby


CODE_TRANSFORMER_BINARY_PATH
 ├── java-parser-1.0-SNAPSHOT.jar
 ├── JavaMethodExtractor-1.0.0-SNAPSHOT.jar
 └── semantic

CODE_TRANSFORMER_MODELS_PATH
 ├── ct_lm
 ├── ct_code_summarization
 │   ├── CT-1
 │   │   ├── config.json
 │   │   ├── model_10000.p
 │   │   :
 │   │   └── model_450000.p
 │   :
 │   └── CT-24
 ├── great_code_summarization
 └── xl_net_code_summarization
"""

from environs import Env, EnvError
from pathlib import Path

from code_transformer.utils.log import get_logger

DEFAULT_DATA_DIR = "../data/code-transformer"
DEFAULT_MODEL_DIR = "checkpoints"
DEFAULT_LOG_DIR = "logs"

env = Env(expand_vars=True)
env_file_path = Path(f"{Path.home()}/.config/code_transformer/.env")
if env_file_path.exists():
    env.read_env(env_file_path, recurse=False)


def _safe_env_read(*args):
    try:
        return env(*args)
    except EnvError as e:
        logger = get_logger(__name__)
        logger.error(e)
        return None


with env.prefixed("CODE_TRANSFORMER_"):

    _DATA_PATH = env("DATA_PATH", DEFAULT_DATA_DIR)
    _BINARY_PATH = _safe_env_read("BINARY_PATH")
    MODELS_SAVE_PATH = env("MODELS_PATH", DEFAULT_MODEL_DIR)
    LOGS_PATH = env("LOGS_PATH", DEFAULT_LOG_DIR)

    CSN_RAW_DATA_PATH = env("CSN_RAW_DATA_PATH", f"{_DATA_PATH}/raw/csn")
    CODE2SEQ_RAW_DATA_PATH = env("CODE2SEQ_RAW_DATA_PATH", f"{_DATA_PATH}/raw/code2seq")
    CODE2SEQ_EXTRACTED_METHODS_DATA_PATH = env(
        "CODE2SEQ_EXTRACTED_METHODS_DATA_PATH", f"{_DATA_PATH}/raw/code2seq-methods"
    )

    DATA_PATH_STAGE_1 = env("DATA_PATH_STAGE_1", f"{_DATA_PATH}/stage1")
    DATA_PATH_STAGE_2 = env("DATA_PATH_STAGE_2", f"{_DATA_PATH}/stage2")

    JAVA_EXECUTABLE = env("JAVA_EXECUTABLE", "java")
    JAVA_PARSER_EXECUTABLE = env("JAVA_PARSER_EXECUTABLE", f"{_BINARY_PATH}/java-parser-1.0-SNAPSHOT.jar")
    JAVA_METHOD_EXTRACTOR_EXECUTABLE = env(
        "JAVA_METHOD_EXTRACTOR_EXECUTABLE", f"{_BINARY_PATH}/JavaMethodExtractor-1.0.0-SNAPSHOT.jar"
    )
    SEMANTIC_EXECUTABLE = env("SEMANTIC_EXECUTABLE", f"{_BINARY_PATH}/semantic")
