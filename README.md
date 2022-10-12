# hlbroken
Identification and Extraction of s aureus hlb gene disruptions in complete genomes

Motivation
------------

In human colonising s aureus isolates, Sa3Int prophages often insert themselves into the genome by disrupting the hlb phospholipase C gene. See this [review](https://www.karger.com/Article/FullText/516645), this [paper](https://www.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000726#tab2) and this [paper](https://www.sciencedirect.com/science/article/pii/S2666979X22001434?via%3Dihub) for more details.

hlbroken is a quick python program that takes a complete whole genome s aureus chromosome as input, determines if the hlb gene is disrupted, and then extracts the sequence in between the two disrupted hlb gene components - this is likely an Sa3Int prophage, or remnants thereof.

Installation
----------

hlbbroken requires only blast and biopython.

The easiest way to install is via conda either manually

```
git clone https://github.com/gbouras13/hlbroken.git
cd hlbroken
conda env create -f environment.yml
conda activate hlbroken_env
hlbroken.py -h
```

or via my conda channel.

```
conda install -c gbouras13 hlbroken
```

Usage
----------

```
usage: hlbroken.py [-h] -c CHROMOSOME [-o OUTDIR] [-f] [-p PREFIX] [-V]

hlbroken: Identification and Extraction of s aureus hlb gene disruptions in complete genomes.

optional arguments:
  -h, --help            show this help message and exit
  -c CHROMOSOME, --chromosome CHROMOSOME
                        s aureus chromosome assembly file in FASTA format.
  -o OUTDIR, --outdir OUTDIR
                        Directory to write the output to.
  -f, --force           Overwrites the output directory.
  -p PREFIX, --prefix PREFIX
                        Prefix for output files. This is not required
  -V, --version         show program's version number and exit
```
