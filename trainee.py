from __future__ import print_function
from __future__ import unicode_literals

import sys
import argparse


def mainLines(polynomial_indexes, polynomial_multipliers, lines):
    data = []
    for line in lines:
        line_stripped = line.split()
        unit_data = [float(x) for x in line_stripped]
        data.append(unit_data)

    score = []
    for current_data in data:
        sum = 0.0
        for polynomial_component_count, multiplier in enumerate(polynomial_multipliers):
            product = multiplier
            for idx in polynomial_indexes[polynomial_component_count]:
                if idx != 0:
                    product *= current_data[polynomial_component_count]
            sum += product
        score.append(sum)

    [print(x) for x in score]

def main(polynomial_indexes, polynomial_multipliers):
    data = []
    for line in sys.stdin:
        line_stripped = line.split()
        unit_data = [float(x) for x in line_stripped]
        data.append(unit_data)

    score = []
    for current_data in data:
        sum = 0.0
        for polynomial_component_count, multiplier in enumerate(polynomial_multipliers):
            product = multiplier
            for idx in polynomial_indexes[polynomial_component_count]:
                if idx != 0:
                    product *= current_data[idx - 1]
            sum += product
        score.append(sum)

    [print(x) for x in score]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('-d', type=str,
                        help='A description')
    args = parser.parse_args()
    polynomial_desc = args.d

    n = 0
    k = 0
    indexes = []
    multipliers = []
    with open(polynomial_desc) as topo_file:
        first_line = topo_file.readline().split()
        n = int(first_line[0])
        k = int(first_line[1])
        for line in topo_file:
            line_stripped = line.split()
            multipliers.append(float(line_stripped[-1]))
            current_idx = [int(x) for x in line_stripped[:-1]]
            indexes.append(current_idx)

    sys.exit(main(indexes, multipliers))
