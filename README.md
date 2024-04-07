# clinical-trials-data <!-- omit from toc -->

## Data Extraction Module

Extract Clinical Data GOV data and create an SQLite table for prototyping.
It also allows to download and extract the text from the trials Protocol's PDF.

It uses the [Clinical Trials Gov (CTG) API](https://clinicaltrials.gov/data-api/api) to extract study information and then the `protocol_extractor` class process this output to create a data object that can then be fit into a Database.
Similarly, this class allows to extract the full protocol text by accessing the study's protocol's online PDF. 

## Quickstart 

To have a working example that extracts data from completed studies from the CTG API,  creates a DataBase populates some tables and then also creates a `json` file with the protocol's text you can simply run. 

```
python ./src/clinical_trials_gov_data/data_extraction/build_data_sources.py
```

Similarly, you can access the [Explore Data Notebook](./analysis/explore_data.ipynb) which has a step by step example of all the process. 

## Records


This project uses lightweight decision records which are stored in [decisions](./decisions/).

This file includes the basic instructions for anyone using the project code. Further guidance for developers can be found in the [Developer's Guide](./docs/devguide.md).

## Developer's Guide 

For the development guide head to [docs/devguide.md](./docs/devguide.md)

## Contents <!-- omit from toc -->

- [Data Extraction Module](#data-extraction-module)
- [Quickstart](#quickstart)
- [Records](#records)
- [Developer's Guide](#developers-guide)
- [Project Organisation](#project-organisation)
- [Set-up](#set-up)
- [Data](#data)

## Project Organisation

```raw
┌── analysis/                            <- Analysis scripts and notebooks
├── data/                                <- See data/README.md
│   ├── external/
│   ├── interim/
│   ├── processed/
│   └── raw/
├── decisions/                           <- Lightweight decision records
├── docs/
│   ├── devguide.md                      <- Developer's Guide
│   └── source/                          <- API documentation (auto-generated from Sphinx)
├── models/                              <- Trained and serialised models/predictions/summaries
├── reports/                             <- Generated analysis as markdown, html, pdf, etc.
│   └── figures/                         <- Generated graphics and figures used in reporting
├── src/                                 <- Source code used in this project
│   ├── clinical_trials_gov_data/
│   │   ├── __init__.py
│   │   ├── ...
├── tests/                               <- Unit tests for the project source code
├── .adr-dir                             <- adr-tools configuration file
├── .editorconfig                        <- editor configuration file
├── .env                                 <- dotenv file for locat configuration (DO NOT ADD TO GIT)
├── .gitignore                           <- git-ignore configuration file
├── .here                                <- marker for project root
├── .pre-commit-config.yaml              <- pre-commit configuration file
├── .talismanrc                          <- talisman secrets protection configuration file
├── CHANGELOG.md                         <- Change log for project versions
├── conda-lock.sh                        <- Lock Conda environment
├── conda-sync.sh                        <- Synchronise Conda environment (including pre-commit)
├── dev-environment.yml                  <- Conda environment development dependencies
├── environment.yml                      <- Conda environment core dependencies
└── pyproject.toml                       <- Project configuration file
```

## Set-up

It is assumed that [conda](https://docs.conda.io/en/latest/) is installed and will be used for package and environment management[^1].

Complete the following (skipping any that have already been done) in order:

1. Install [pipx](https://github.com/pypa/pipx) for creating isolated environments for management tools:

```bash
# Use current environment's interpretor to access pip
> python -m pip install --user pipx
# Add pipx to PATH
> python -m pipx ensurepath
# Close current terminal and open a new one
```

2. Install [conda-lock](https://github.com/conda/conda-lock) for dependency management:

```bash
# Install conda-lock
> pipx install conda-lock
```

3. Obtain the code:

```bash
> git clone https://github.com/patofw/clinical-trials-data.git
```

4. Synchronise the environment:

```bash
> . conda-sync.sh
```

## Data

See the [data doc](./data/README.md) for more details on the layout.

Data files are shared via: _link TBD_

[^1]: If conda is not installed then the advised installation approach is to use [miniforge](https://github.com/conda-forge/miniforge?tab=readme-ov-file#unix-like-platforms-mac-os--linux).
