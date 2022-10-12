# hlbroken
Identification and Extraction of s aureus hlb gene disruptions in complete genomes

Motivation
------------

In human colonising s aureus isolates, Sa3Int prophages often insert themselves into the genome by disrupting the hlb phospholipase C gene. See this [review](https://www.karger.com/Article/FullText/516645), this [paper](https://www.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000726#tab2) and this [paper](https://www.sciencedirect.com/science/article/pii/S2666979X22001434?via%3Dihub) for more details.

hlbroken is a quick python program that takes a complete whole genome s aureus chromosome as input, determines if the hlb gene is disrupted, and then extracts the sequence in between the two disrupted hlb gene components - this is likely an Sa3Int prophage, or remnants thereof.

Installation
----------

hlbbroken requires only blast and biopython.

The easiest way to install is via conda

```
git clone https://github.com/gbouras13/hlbroken.git
cd hlbroken
conda env create -f environment.yml
conda activate hlbroken_env
hlbroken.py -h
```
