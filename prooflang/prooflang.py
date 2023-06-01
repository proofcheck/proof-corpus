# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The ProofLang Corpus of arXiv Proofs"""


import csv
import os

import datasets


_CITATION = """\
@inproceedings{prooflang:dataset,
title = "{ProofLang: the Language of arXiv Proofs}",
booktitle = "{Intelligent Computer Mathematics (CICM 2023)}",
author = "{Henry Hammer and Nanako Noda and Christopher A. Stone}",
year = {2023},
note = {To appear}
}
"""

_DESCRIPTION = """\ The ProofLang Corpus includes over three million
English-language proofs—558 million words—mechanically extracted from the papers
(Math, CS, Physics, etc.) posted on arXiv.org between 1992 and 2020. The focus
of this corpus is written proofs, not the explanatory text that surrounds them,
and more specifically on the language used in such proofs; mathematical
content is filtered out, resulting in sentences such as ``Let MATH be
the restriction of MATH to MATH.'' This dataset reflects how people prefer to
write informal proofs. It is also amenable to statistical analyses and to
experiments with  Natural Language Processing (NLP) techniques.
"""

_HOMEPAGE = "https://huggingface.co/datasets/proofcheck/prooflang"

_LICENSE = "CC-BY 4.0"

_URLS = {
    "proofs": "proofs.zip",
    "sentences": "sentences.zip",
    "raw": "raw.zip",
    "tags": "tags.zip",
}

class ArxivProofs(datasets.GeneratorBasedBuilder):
    """English text from proofs found in arXiv preprints."""

    VERSION = datasets.Version("0.6.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'proofs')
    # data = datasets.load_dataset('my_dataset', 'sentences')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="proofs", version=VERSION, description="One proof per line"),
        datasets.BuilderConfig(name="sentences", version=VERSION, description="One sentence per line"),
        datasets.BuilderConfig(name="raw", version=VERSION, description="One (less agressively cleaned) proof per line"),
        datasets.BuilderConfig(name="tags", version=VERSION, description="arXiv subject tags for each paper"),
    ]

    DEFAULT_CONFIG_NAME = "proofs"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if self.config.name in {"proofs", "raw"}:  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "paper": datasets.Value("string"),
                    "proof": datasets.Value("string"),
                }
            )
        elif self.config.name == "tags":  # This is an example to show how to have different features for "proofs" and "sentences"
            features = datasets.Features(
                {
                    "paper": datasets.Value("string"),
                    "tags": datasets.Value("string"),
                }
            )
        else:  # This is an example to show how to have different features for "proofs" and "sentences"
            features = datasets.Features(
                {
                    "paper": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            # supervised_keys=("sentence", "label"),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        urls = _URLS[self.config.name]
        data_dir = dl_manager.download_and_extract(urls)
        # data_file = dl_manager.download_and_extract(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir,
                    "split": "train",   # Prooflang doesn't have a train/test split.
                },
            ),
            # datasets.SplitGenerator(
            #     name=datasets.Split.TEST,
            #     # These kwargs will be passed to _generate_examples
            #     gen_kwargs={
            #         "filepath": os.path.join(data_dir, "test.jsonl"),
            #         "split": "test"
            #     },
            # ),
            # datasets.SplitGenerator(
            #     name=datasets.Split.VALIDATION,
            #     # These kwargs will be passed to _generate_examples
            #     gen_kwargs={
            #         "filepath": os.path.join(data_dir, "dev.jsonl"),
            #         "split": "dev",
            #     },
            # ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        # TODO: This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        csv.field_size_limit(256000)  # Some of the raw proofs are slightly longer than 131072 characters
        with open(os.path.join(filepath, self.config.name + ".tsv"), encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
            for key, data in enumerate(reader):
                yield key, data
                # if self.config.name == "proofs":
                #     # Yields examples as (key, example) tuples
                #     # print(key, repr(data))
                #     yield key, {
                #         "fileID" : data[0],
                #         "proof": data[1],
                #     }
                # else:
                #     yield key, {
                #         "fileID" : data[0],
                #         "sentence": data[1],
                #     }
