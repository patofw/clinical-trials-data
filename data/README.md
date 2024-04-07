# Data Overview

## Raw

The original immutable data dump. These are the original files received from the client, and must not be modified.

## External

Data from third-party vendors.

## Interim

Intermediate data that have been transformed. Example transformations

- Clean data (white space, spelling mistakes)
- Discard irrelevant features
- Merge data between (and within) tables, but only within datasets
- Convert data types
- Reshape data

At this stage data should not be merged between datasets.

Data are stored in **TBD** formats.

## Processed

The final, canonical datasets for modelling. Example actions

- Merge datasets
- Engineer features

Data are stored in formats optimised for modelling.
