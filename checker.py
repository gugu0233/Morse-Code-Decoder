#!/usr/bin/env python3
import argparse
from enum import IntEnum
import os
import sys

from parse_tms import parse_tms
from parse_xlsx import parse_xlsx
from write_tms import write_tms
from write_xlsx import write_xlsx
import tm


from tests import TESTS


LOGDIR = "logs/"
MAX_STEPS = 100000

def eprint(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


class What(IntEnum):
    TRANSLATE = 0
    FILTER = 1


CRITTERIA_DICT = {
        "translate": What.TRANSLATE,
        "filter": What.FILTER,
    }


def what_to_str(what):
    if what == What.TRANSLATE:
        return "translate"
    elif what == What.FILTER:
        return "filter"


def run_on_input(machine, args):
    res = machine.run(word=args.test_input, max_steps=args.max_steps,
                      debug=True)


def run_test(machine, args, test, critteria, log):
    word, ref_config = test

    res = machine.run(word=word, max_steps=args.max_steps, debug=True,
                      dbglog=log)

    score = 0
    for i in range(len(critteria)):
        if res[critteria[i]] == ref_config[critteria[i]]:
            score += 0.5

    return score


def run_tests(machine, args, tests=TESTS):
    if not isinstance(args.validation_type, list):
        critteria = [CRITTERIA_DICT[args.validation_type]]
    else:
        critteria = [CRITTERIA_DICT[c] for c in args.validation_type]

    total = 0
    total_max_score = 100

    os.makedirs(LOGDIR, exist_ok=True)

    what_str = ", ".join(what_to_str(w) for w in critteria)
    print(f"Testing {what_str} verification:")

    for i, test in enumerate(tests.items()):
        dbglog = os.path.join(LOGDIR, f"dbglog_{i+1}")

        print(f"#{i+1:<3} ({test[1][0]})", "."*40, sep=" ", end=" ")
        try:
            cscore = run_test(machine, args, test, critteria, dbglog)
            print("PASS" if 2 * cscore == len(critteria) else "FAIL")
            cscore *= 5
            total += cscore
        except tm.StepLimitExceeded:
            print("SLE")

    print(f"Total:{int(total)}/{total_max_score}")


def parse_machine(path):
    extension = path.split(".")[-1]
    if extension == "tms":
        return parse_tms(path)
    elif extension == "xlsx":
        return parse_xlsx(path)
    else:
        raise ValueError(f"Don't know what to do with {path} (valid \
                extensions are \".tms\" and \".xlsx\"")


def write_machine(machine, args):
    path = args.output
    extension = path.split(".")[-1]
    if extension == "tms":
        return write_tms(path, machine)
    elif extension == "xlsx":
        return write_xlsx(path, machine)
    else:
        raise ValueError(f"Don't know what to do with {path} (valid \
                extensions are \".tms\" and \".xlsx\"")


def main():
    parser = argparse.ArgumentParser(description="Checker for the first \
            assignment for the Analysis of Algorithm course. \
            The main functionality is to load a Turing Machine and either \
            run it on some input or convert it to another format.")
    parser.add_argument("--tm", help="Input Turing Machine file (.xlsx or \
                        .tms)", required=True)
    parser.add_argument("--max-steps", type=int, default=MAX_STEPS,
            help="Maximum number of steps a TM is allowed to make before a \
            \"Step Limit Exceded\" error is produced. Default is %(default)s.")
    tgroup = parser.add_mutually_exclusive_group(required=True)
    tgroup.add_argument("--run-tests", action="store_true", help="Run the \
                        machine on all tests")
    tgroup.add_argument("--test-input", type=str, help="Test a specific input")
    tgroup.add_argument("--output", help="Output Turing Machine file (.xlsx \
            or .tms).")
    parser.add_argument("--validation-type", choices=["translate", "filter",
    "all"], nargs="+", default="all", help="Choose which kind of \
            checks are performed (by default, they all are).")

    args = parser.parse_args()

    path = args.tm
    machine = parse_machine(path)

    if os.path.exists("README"):
        with open("README", "r") as fin:
            first = fin.readline().strip("\n")

        critteria = first.split(" ")
        validation_type = []
        valid_line = True
        for crit in critteria:
            if crit not in ["translate", "filter"]:
                valid_line = False

            validation_type.append(crit)

        if valid_line:
            args.validation_type = validation_type

    if args.validation_type == ["all"] or args.validation_type == "all":
        args.validation_type = ["translate", "filter"]

    if args.run_tests:
        run_tests(machine, args)
    elif args.test_input:
        try:
            run_on_input(machine, args)
        except tm.StepLimitExceeded:
            eprint("Step Limit Exceeded!")
    elif args.output:
        write_machine(machine, args)


if __name__ == "__main__":
    main()
