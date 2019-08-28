#!/usr/bin/python3

import csv
from sys import argv, exit


def print_beta_dict(betas):
    for beta in betas:
        for KS in betas[beta]:
            print("{}\t{}\t{}".format(beta, KS, betas[beta][KS]))


def csv_beta_dict(betas):
    with open(argv[2], mode='w') as f:
                w = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                w.writerow(['Beta', 'K, S', 'Winrate'])
                for beta in betas:
                    for KS in betas[beta]:
                        w.writerow((beta, KS, betas[beta][KS]))


def main():
    if len(argv) != 4:
        exit(1)

    result = {}
    with open(argv[1]) as f:
        result = eval(f.readline())

    print(len(result))
    if argv[3] == 'p':
        print_beta_dict(result)
    elif argv[3] == 'c':
        csv_beta_dict(result)

    return 0


if __name__ == '__main__':
    main()
