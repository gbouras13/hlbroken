import os
import sys
import subprocess as sp
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import pandas as pd
import logging


def write_to_log(s, logger):
           while True:
                output = s.readline().decode()
                if output:
                    logger.log(logging.INFO, output)
                else:
                    break

def blast(input, out_dir, prefix, bin_path, logger):
    blast_db = os.path.join(bin_path, "..", 'database', "hlb.fasta") 
    output_file = os.path.join(out_dir, prefix + "_blast_output.txt") 
    try:
        blast = sp.Popen(["blastn", "-query", input, "-db",blast_db, "-evalue", "1e-20", "-out",output_file, "-outfmt", "6 qseqid qlen sseqid slen length qstart qend sstart send pident nident gaps mismatch qseq sseq"  ], stdout=sp.PIPE, stderr=sp.PIPE) 
        write_to_log(blast.stderr, logger)
    except:
        sys.exit("Error with blast\n")  



def process_blast_output(out_dir, prefix, logger):
    blast_file =  os.path.join(out_dir, prefix + "_blast_output.txt") 
    col_list = ["qseqid", "qlen", "sseqid", "slen", "length", "qstart", "qend", "sstart", "send", "pident", "nident", "gaps", "mismatch", "qseq", "sseq"] 
    blast_df = pd.read_csv(blast_file, delimiter= '\t', index_col=False , names=col_list) 
    hits = len(blast_df['qseqid'])
    if len(blast_df['qseqid']) == 0 :
        print('No hlb BLAST hit found. Check that the input is an s aureus complete genome.')
        logger.info('No hlb BLAST hit found. Check that the input is s aureus complete genome.')
    elif len(blast_df['qseqid']) == 1 :
        print('One hlb BLAST hit found. This likely means there is no Saint3 prophage disrupting the hlb gene.')
        logger.info('One hlb BLAST hit found. This likely means there is no Saint3 prophage disrupting the hlb gene.')
    elif len(blast_df['qseqid']) == 2 :
        print('Two hlb BLAST hits found. This likely means there is a Saint3 prophage.')
        logger.info('Two hlb BLAST hits found. This likely means there is a Saint3 prophage.')
    else:
        print('More than 2 hlb BLAST hits found. Something is strange - could be interesting. Please check manually.')
        logger.info('More than 2 hlb BLAST hits found. Something is strange - could be interesting. Please check manually.')
    return hits

def extract_prophage(input, out_dir, prefix, logger):
    blast_file =  os.path.join(out_dir, prefix + "_blast_output.txt") 
    col_list = ["qseqid", "qlen", "sseqid", "slen", "length", "qstart", "qend", "sstart", "send", "pident", "nident", "gaps", "mismatch", "qseq", "sseq"] 
    blast_df = pd.read_csv(blast_file, delimiter= '\t', index_col=False , names=col_list) 

    strand = "fwd"

    # fwd strand of hlb, phage is reverse strand
    if blast_df["sstart"][0] < blast_df["send"][0]:
        phage_start = blast_df["qstart"][0]
        phage_end = blast_df["qend"][1]
    
    # rev strand of hlb, phage is fwd strand so no need to rev comp
    else:
        strand = "rev"
        phage_start = blast_df["qend"][0]
        phage_end = blast_df["qstart"][1]

    if abs(phage_end - phage_start) < 20000 or abs(phage_end - phage_start) > 100000:
        print('Difference between start and end of phage is under 20000 or over 100000bp. Likely something else going on.')
        logger.info('Difference between start and end of phage is under 20000 or over 100000bp. Likely something else going on.')


    # get record
    record = SeqIO.read(input, "fasta")
    start = min(int(phage_start) - 1, int(phage_end) )
    end = max(int(phage_start) - 1, int(phage_end) )
    phage_seq = record.seq[start:end] 
    phage_id = str(prefix) + "_" +  str(phage_start)+ "_" + str(phage_end )

    # rev comp the phage

    if strand == "fwd":
        phage_seq = phage_seq.reverse_complement()

    phage_record = SeqRecord(phage_seq, id=phage_id, description="")

    outfile = os.path.join(out_dir, prefix + "_phage.fasta")  

    with open(outfile, 'w') as out_fa:
        SeqIO.write(phage_record, out_fa, 'fasta')

    # calc some summary statisstics
    length = abs(int(phage_start)-int(phage_end))


    summary_df = pd.DataFrame(
    {'name': [prefix],
     'length': [length],
     'phage_start': [phage_start],
     'phage_stop': [phage_end],
     'hlb_strand': [strand]
    })

    summary_df.to_csv(os.path.join(out_dir, prefix + "_summary_stats.csv"), sep=",", index=False)


# function to touch create a file 
# https://stackoverflow.com/questions/12654772/create-empty-file-using-python
def touch_file(path):
    with open(path, 'a'):
        os.utime(path, None)

# to create empty fasta file files
def touch_output_files(out_dir, prefix):
    touch_file(os.path.join(out_dir, prefix + "_phage.fasta"))
    touch_file(os.path.join(out_dir, prefix + "_summary_stats.tsv"))

