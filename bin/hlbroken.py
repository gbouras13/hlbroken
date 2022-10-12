#!/usr/bin/env python3
import input_commands
import processes
import os
import logging
import time
import datetime



if __name__ == "__main__":

    # get start time
    start_time = time.time()

    # getting time for log file 

    time_for_log = datetime.datetime.now().strftime("%m%d%Y_%H%M%S")

    args = input_commands.get_input()
        # set the prefix
    if args.prefix == "Default":
        prefix = "hlb_mapper"
    else:
        prefix = args.prefix
    
    out_dir = input_commands.instantiate_dirs(args.outdir, args.force) # incase there is already an outdir

    LOG_FILE = os.path.join(args.outdir, prefix + "_" + str(time_for_log) + ".log")
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO,filename=LOG_FILE,format='%(asctime)s - %(levelname)s - %(message)s')
    print("Starting hlb_mapper.")
    logger.info("Starting hlb_mapper")
    print("Checking input fasta.")
    logger.info("Checking input fasta.")

    # instantiation/checking fastq 
    input_commands.validate_fasta(args.chromosome)

    print("Running Blast.")
    logger.info("Running Blast.")

    # run blast
    processes.blast(args.chromosome, args.outdir, prefix, logger)

    # determines the number of hits
    hits = processes.process_blast_output(args.outdir, prefix, logger) 
    


    # extract phage if 2 hits, otherwise create empty file (for snakemake etc)
    if hits == 2:
        print("Extracting hlb disrupting sequence.")
        logger.info("Extracting hlb disrupting sequence.")
        processes.extract_prophage(args.chromosome, args.outdir, prefix, logger)
    else:
        processes.touch_output_files(args.out_dir, prefix)

    # Determine elapsed time
    elapsed_time = time.time() - start_time
    elapsed_time = round(elapsed_time, 2)

    # Show elapsed time for the process
    logger.info("plassembler has finished")
    logger.info("Elapsed time: "+str(elapsed_time)+" seconds")

    print("plassembler has finished")
    print("Elapsed time: "+str(elapsed_time)+" seconds")

    




