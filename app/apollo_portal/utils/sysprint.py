"""Utilities for printing to the console with color."""


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def ok(msg):
    print(f"{BColors.OKCYAN}{msg}{BColors.END}")


def success(msg):
    print(f"{BColors.OKGREEN}{msg}{BColors.END}")


def warn(msg):
    print(f"{BColors.WARNING}{msg}{BColors.END}")


def fail(msg):
    print(f"{BColors.FAIL}{msg}{BColors.END}")
