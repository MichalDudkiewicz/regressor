from __future__ import print_function
from __future__ import unicode_literals

import math
import sys

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

import argparse
import trainee


def mainLines(set_lines, indexes, init_mult, out_data, k, n, max_iter, step, eps):
    expected_values = []
    arguments = []
    for line in set_lines:
        line_stripped = line.split()
        expected_values.append(float(line_stripped[-1]))
        arguments.append(' '.join([x for x in line_stripped[:-1]]))

    main(arguments, expected_values, indexes, init_mult, out_data, k, n, max_iter, step, eps)


def main(arguments, expected_values, indexes, init_mult, out_data, k, n, max_iter, step, eps):
    N = len(expected_values)
    p_list = training(init_mult, indexes, arguments, expected_values, n, N, out_data, max_iter, step, eps)

    print(n, k)
    for it, idx in enumerate(indexes):
        string_idxes = [str(i) for i in idx]
        print(' '.join(string_idxes), p_list[it])


def training(p_list, indexes, arguments, expected_values, n, N, out_data, iter_max, step, eps):
    arguments_values = []
    for arguments_line in arguments:
        args_splitted = arguments_line.split()
        arguments_values.append([float(val) for val in args_splitted])

    previous_derivatives = []
    # previous_length = float('inf')
    for iter in range(iter_max):

        # if iter == iter_max * 0.2:
        #     step = step / 2
        # elif iter == 0.4 * iter_max:
        #     step = step / 2
        # elif iter == 0.6 * iter_max:
        #     step = step / 2
        # elif iter == 0.8 * iter_max:
        #     step = step / 2
        # elif iter == 0.9 * iter_max:
        #     step = step / 2
        # elif iter == 0.99 * iter_max:
        #     step = step / 2

        old_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result
        sys.stdin = arguments
        trainee.main(indexes, p_list)
        sys.stdout = old_stdout
        result_string = result.getvalue()

        calculated_values = [float(val) for val in result_string.split()]

        derivatives = []
        for i in range(0, n + 1):
            sumDer = 0
            multiplier = 1
            for j in range(0, N):
                if i > 0:
                    multiplier = arguments_values[j][i - 1]
                sumDer += (calculated_values[j] - expected_values[j]) * multiplier
            sumDer /= N
            derivatives.append(sumDer)

        derivatives.reverse()
        # if next > prev:
        #     step /= 2
        #     prev = next
        #     continue
        # prev = next
        # length = math.sqrt(sum([x**2 for x in derivatives]))

        p_list = list([p - step * derivatives[i] for i, p in enumerate(p_list)])

        if len(previous_derivatives) > 0:
            if all(der * prev_der < 0 for der, prev_der in zip(derivatives, previous_derivatives)):
                step *= 0.5
        previous_derivatives = derivatives

        if all(abs(derivative) < eps for derivative in derivatives):
            iter_max = iter + 1
            break
    with open(out_data, "w") as file1:
        file1.write("iterations={}".format(iter_max))
    return p_list

# https://planetcalc.com/7886/

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('-t', type=str,
                        help='A train set')
    parser.add_argument('-i', type=str,
                        help='A data set')
    parser.add_argument('-o', type=str,
                        help='A data out set')
    args = parser.parse_args()
    train = args.t
    iter_data = args.i
    out_data = args.o

    n = 0
    k = 0
    initial_indexes = []
    initial_multipliers = []
    for line in sys.stdin:
        first_line = line.split()
        n = int(first_line[0])
        k = int(first_line[1])
        for next_line in sys.stdin:
            line_stripped = next_line.split()
            initial_multipliers.append(float(line_stripped[-1]))
            current_idx = [int(x) for x in line_stripped[:-1]]
            initial_indexes.append(current_idx)

    max_iter = 0
    with open(iter_data) as iter_data_file:
        max_iter = int(iter_data_file.readlines()[0].split('=')[1])

    default_eps = 0.00001
    default_step = 0.1

    with open(train) as train_set:
        train_set_lines = train_set.readlines()

    expected_values = []
    arguments = []
    for line in train_set_lines:
        line_stripped = line.split()
        expected_values.append(float(line_stripped[-1]))
        arguments.append(' '.join([x for x in line_stripped[:-1]]))

    sys.exit(main(arguments, expected_values, initial_indexes, initial_multipliers, out_data, k, n, max_iter, default_step, default_eps))
