# Code Transformer

For the original readme refer to [`original_readme.md`](./original_readme.md) or
to the original [repository](https://github.com/danielzuegner/code-transformer#22-javaparser--javamethodextractor).

## Changes

List of changes w.r.t original implementation.

### Map-Style dataset

In some cases, we need to have random access to any dataset sample,
e.g. when using code-transformer for contrastive learning.
By default, vanilla implementation uses an iterable dataset.

Assuming, you have preprocessed dataset that stored in
`$CODE_TRANSFORMER_DATA_PATH/stage2/<name>`.

Steps to change dataset type:
1. Unpack dataset with
```shell
python scripts/unpack-dataset.py --data <name> 
```
2. Set environment variable
```shell
export CODE_TRANSFORMER_DATASET=mapstyle
```
If you want to return iterable dataset remove this variable or set it to `iterable`.

That is all, start training without any other changes.

### Java sources build

In order to easily build java source, we replace Maven build system with the Gradle.

To build Java-Parser that required for creating `Stage1` examples,
navigate to [`sub_modules/java-parser`] and build shadow Jar with
```shell
./gradlew shadowJar
```

After that,
copy `sub_modules/java-parser/build/libs/java-parser.jar` to folder with binaries `$CODE_TRANSFORMER_BINARY_PATH`.
