# script to read in a folder containing pptx files and convert them to pdf
#
# Path: scripts/convert.py
# Compare this snippet from autopages/topdf.py:
#

import argparse
import logging
from pathlib import Path

from autopages.ppt import create_ppt
from autopages.topdf import ppt_to_pdf

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="Create pdf documents pptx files"
    )
    # add directory argument
    parser.add_argument(
        "directory",
        help="Directory containing pptx files",
    )
    # add optional output directory argument
    parser.add_argument(
        "-o",
        "--output",
        help="Output directory for pdf files",
    )
    args = parser.parse_args()

    # get the directory
    directory = Path(args.directory).resolve()
    # get the output directory
    output = Path(args.output).resolve() if args.output else directory

    # convert in parallel using multiprocessing
    import multiprocessing

    # get the number of cores
    cores = multiprocessing.cpu_count()
    # create a pool of workers
    pool = multiprocessing.Pool(cores)
    # create a list of pptx files
    pptx_files = list(directory.glob("*.pptx"))
    # convert the pptx files to pdf
    pool.map(ppt_to_pdf, pptx_files)
    # wait for the pool to finish
    pool.join()
    # close the pool
    pool.close()
