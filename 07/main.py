"""
Matrix chain miltiplication.
Main file
Copyright 2022 by Artem Ustsov
"""

import argparse
import logging
import os
import sys

from matrixes import matrixes_python
from matrixes import matrixes_ctypes


if __name__ == "__main__":
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    FORMAT_LOG = "%(asctime)s: %(message)s"
    file_log = logging.FileHandler("logs/matrix.log")
    console_out = logging.StreamHandler()

    logging.basicConfig(
        handlers=(file_log, console_out),
        format=FORMAT_LOG,
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--chain", default="2,3,2")
    parser.add_argument("-r", "--is_random", default="True")
    parser.add_argument("-t", "--type", default="python")
    parser.add_argument("-e", "--edge", type=int, default=5)
    parser.add_argument("-i", "--input_fd", default="stdin")
    parser.add_argument("-v", "--verbose", type=int, default=1)

    args = parser.parse_args()

    logging.getLogger().info("=====PROGRAM START=====")

    if args.type in ["C++", "c++", "CPP", "cpp", "c"]:
        matrix_chain_pattern = list(map(int, args.chain.split(",")))
        matrixes_ctypes.multiply_matrix_chain_command(
            matrix_chain_pattern, args.edge, args.verbose,
        )
    else:
        with open(
            args.input_fd, "r", encoding="utf-8"
        ) if args.input_fd != "stdin" else sys.stdin as input_fd:
            matrixes_python.multiply_matrix_chain_command(
                args.chain, args.is_random, input_fd,
            )
        logging.getLogger().info("=====PROGRAM STOP=====")
