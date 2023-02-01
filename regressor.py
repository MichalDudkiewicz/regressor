from __future__ import print_function
from __future__ import unicode_literals
import argparse
import math
# import multiprocessing
import sys
from itertools import combinations_with_replacement
# from multiprocessing import Process

import trainee
import trainer

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

max_iter = 20000
final_max_iter = 30000
step = 0.3
eps = 0.000001
out_iter_data = "data_out.txt"


def normalize(x, xmin, xmax):
    # https: // stats.stackexchange.com / questions / 134877 / normalization - effect - on - polynomial - regression
    # https: // stats.stackexchange.com / questions / 178626 / how - to - normalize - data - between - 1 - and -1
    return 2 * (x - xmin) / (xmax - xmin) - 1


def denormalize(xnormalized, xmin, xmax):
    # https: // stats.stackexchange.com / questions / 178626 / how - to - normalize - data - between - 1 - and -1
    return (xnormalized + 1)(xmax - xmin) / 2 - 1


# def validate(validation_argument_line_strings, validation_values, train_argument_line_strings, train_values,
#              init_n, init_k, min_error, result):
#     # https://ichi.pro/pl/ml-od-podstaw-liniowe-wielomianowe-i-uregulowane-modele-regresji-125715608723574
#     L = int(math.factorial(init_n + init_k) / (math.factorial(init_k) * math.factorial(init_n)))
#     indexes = [[i] for i in reversed(range(L))]
#
#     init_mult = [1] * len(indexes)
#     k = 1
#     n = L - 1
#
#     combos = [combinations_with_replacement(range(init_n), i)
#               for i in range(1, init_k + 1)]
#     combinations = [item for sublist in combos for item in sublist]
#     combinations.sort(key=lambda val: (max([val.count(i) for i in val]), len(val), -sum(val)), reverse=True)
#
#     arg_line_strings_converted = []
#     for argument_line_string in train_argument_line_strings:
#         arguments_f = [float(a) for a in argument_line_string.split()]
#         arguments_converted = []
#         for comb in combinations:
#             iloczyn = 1
#             for idx in comb:
#                 iloczyn *= arguments_f[idx]
#             arguments_converted.append(str(iloczyn))
#         arguments_converted = reversed(arguments_converted)
#         arg_line_strings_converted.append(' '.join(arguments_converted))
#
#     result = StringIO()
#     sys.stdout = result
#
#     trainer.main(arg_line_strings_converted, train_values, indexes, init_mult, out_iter_data, k, n, max_iter, step,
#                  eps)
#
#     trained_polynomial = result.getvalue().split('\n')
#
#     trained_polynomial = [n.split() for n in trained_polynomial][1:-1]
#
#     indexes = [idx[:-1] for idx in trained_polynomial]
#     int_indexes = []
#     for i in indexes:
#         int_indexes.append([int(idx) for idx in i])
#
#     multipliers = [float(mult[-1]) for mult in trained_polynomial]
#
#     valid_arg_line_strings_converted = []
#     for argument_line_string in validation_argument_line_strings:
#         arguments_f = [float(a) for a in argument_line_string.split()]
#         arguments_converted = []
#         for comb in combinations:
#             iloczyn = 1
#             for idx in comb:
#                 iloczyn *= arguments_f[idx]
#             arguments_converted.append(str(iloczyn))
#         valid_arg_line_strings_converted.append(' '.join(arguments_converted))
#
#     old_stdout = sys.stdout
#     result_val = StringIO()
#     sys.stdout = result_val
#     trainee.mainLines(int_indexes, multipliers, valid_arg_line_strings_converted)
#
#     values = [val for val in result_val.getvalue().split('\n') if val]
#     sys.stdout = old_stdout
#     l = [(float(calculated_value) - expected_value) ** 2 for calculated_value, expected_value in
#          zip(values, validation_values)]
#     mse = math.sqrt(sum(l))
#     # print(trained_polynomial)
#     # print(mse)
#     if mse < min_error.value:
#         with min_error.get_lock():
#             if mse >= min_error.value:
#                 return
#             min_error.value = mse
#             result.value = init_k


def main(train_set):
    old_stdin = sys.stdin
    argument_line_strings = []
    output_values = []
    init_n = 0

    args_mins = []
    args_maxs = []
    with open(train_set, 'r') as train_set_file:
        lines = []
        for line in train_set_file:
            line_splitted = line.split()
            init_n = len(line_splitted) - 1
            lines.append(line_splitted)
            line_splitted_vals = [float(val) for val in line_splitted[:-1]]
            if len(args_mins) == 0:
                args_mins = list(line_splitted_vals)
            else:
                for i, arg in enumerate(line_splitted_vals):
                    args_mins[i] = min(args_mins[i], arg)

            if len(args_maxs) == 0:
                args_maxs = list(line_splitted_vals)
            else:
                for i, arg in enumerate(line_splitted_vals):
                    args_maxs[i] = max(args_maxs[i], arg)

        for line in lines:
            # output_values.append(float(line[-1]))
            # argument_line_strings.append(' '.join(line[:-1]))

            # train set normalization
            normalized_line = [normalize(float(val), arg_min, arg_max) for val, arg_min, arg_max in
                               zip(line, args_mins, args_maxs)]
            output_values.append(float(line[-1]))
            argument_line_strings.append(' '.join([str(val) for val in normalized_line]))

    validation_part = 4
    validation_argument_line_strings = [argument_line_string for i, argument_line_string in
                                        enumerate(argument_line_strings) if i % validation_part == 0]
    validation_values = [val for i, val in
                         enumerate(output_values) if i % validation_part == 0]

    train_argument_line_strings = [argument_line_string for i, argument_line_string in
                                   enumerate(argument_line_strings) if i % validation_part != 0]
    train_values = [val for i, val in
                    enumerate(output_values) if i % validation_part != 0]

    old_stdout = sys.stdout

    # min_error = multiprocessing.Value('f', math.inf)
    # result = multiprocessing.Value('i', 0)
    # processes = [Process(target=validate,
    #                      args=(
    #                          validation_argument_line_strings, validation_values,
    #                          train_argument_line_strings,
    #                          train_values, init_n, init_k, min_error, result)) for init_k in range(1, 11)]
    # for process in processes:
    #     process.start()
    # for process in processes:
    #     process.join()
    #
    # best_k = result.value

    best_k = 0
    best_mse = float('inf')

    for init_k in range(1, 11):
        # https://ichi.pro/pl/ml-od-podstaw-liniowe-wielomianowe-i-uregulowane-modele-regresji-125715608723574
        L = int(math.factorial(init_n + init_k) / (math.factorial(init_k) * math.factorial(init_n)))
        indexes = [[i] for i in reversed(range(L))]

        init_mult = [1] * len(indexes)
        k = 1
        n = L - 1

        combos = [combinations_with_replacement(range(init_n), i)
                  for i in range(1, init_k + 1)]
        combinations = [item for sublist in combos for item in sublist]
        combinations.sort(key=lambda val: (max([val.count(i) for i in val]), len(val), -sum(val)), reverse=True)

        arg_line_strings_converted = []
        for argument_line_string in train_argument_line_strings:
            arguments_f = [float(a) for a in argument_line_string.split()]
            arguments_converted = []
            for comb in combinations:
                iloczyn = 1
                for idx in comb:
                    iloczyn *= arguments_f[idx]
                arguments_converted.append(str(iloczyn))
            arguments_converted = reversed(arguments_converted)
            arg_line_strings_converted.append(' '.join(arguments_converted))

        result = StringIO()
        sys.stdout = result

        trainer.main(arg_line_strings_converted, train_values, indexes, init_mult, out_iter_data, k, n, max_iter, step,
                     eps)

        sys.stdout = old_stdout
        trained_polynomial = result.getvalue().split('\n')

        trained_polynomial = [n.split() for n in trained_polynomial][1:-1]

        indexes = [idx[:-1] for idx in trained_polynomial]
        int_indexes = []
        for i in indexes:
            int_indexes.append([int(idx) for idx in i])

        multipliers = [float(mult[-1]) for mult in trained_polynomial]

        valid_arg_line_strings_converted = []
        for argument_line_string in validation_argument_line_strings:
            arguments_f = [float(a) for a in argument_line_string.split()]
            arguments_converted = []
            for comb in combinations:
                iloczyn = 1
                for idx in comb:
                    iloczyn *= arguments_f[idx]
                arguments_converted.append(str(iloczyn))
            valid_arg_line_strings_converted.append(' '.join(arguments_converted))

        old_stdout = sys.stdout
        result_val = StringIO()
        sys.stdout = result_val
        trainee.mainLines(int_indexes, multipliers, valid_arg_line_strings_converted)

        values = [val for val in result_val.getvalue().split('\n') if val]
        sys.stdout = old_stdout
        l = [(float(calculated_value) - expected_value) ** 2 for calculated_value, expected_value in
             zip(values, validation_values)]
        mse = math.sqrt(sum(l))
        if mse < best_mse:
            best_mse = mse
            best_k = init_k

    # https://ichi.pro/pl/ml-od-podstaw-liniowe-wielomianowe-i-uregulowane-modele-regresji-125715608723574
    L = int(math.factorial(init_n + best_k) / (math.factorial(best_k) * math.factorial(init_n)))
    indexes = [[i] for i in reversed(range(L))]

    init_mult = [1] * len(indexes)
    k = 1
    n = L - 1
    combos = [combinations_with_replacement(range(init_n), i)
              for i in range(1, best_k + 1)]
    combinations = [item for sublist in combos for item in sublist]
    combinations.sort(key=lambda val: (max([val.count(i) for i in val]), len(val), -sum(val)), reverse=True)

    arg_line_strings_converted = []
    for argument_line_string in argument_line_strings:
        arguments_f = [float(a) for a in argument_line_string.split()]
        arguments_converted = []
        for comb in combinations:
            iloczyn = 1
            for idx in comb:
                iloczyn *= arguments_f[idx]
            arguments_converted.append(str(iloczyn))
        arguments_converted = reversed(arguments_converted)
        arg_line_strings_converted.append(' '.join(arguments_converted))

    result = StringIO()
    sys.stdout = result

    trainer.main(arg_line_strings_converted, output_values, indexes, init_mult, out_iter_data, k, n, final_max_iter, step,
                 eps)

    sys.stdout = old_stdout
    trained_polynomial = result.getvalue().split('\n')

    trained_polynomial = [n.split() for n in trained_polynomial][1:-1]
    indexes = [idx[:-1] for idx in trained_polynomial]
    int_indexes = []
    for i in indexes:
        int_indexes.append([int(idx) for idx in i])

    multipliers = [float(mult[-1]) for mult in trained_polynomial]

    arg_line_strings_converted = []
    sys.stdin = old_stdin
    for argument_line_string in sys.stdin:
        arguments_f = [float(a) for a in argument_line_string.split()]
        # input normalization
        arguments_f = [normalize(val, arg_min, arg_max) for val, arg_min, arg_max in
                       zip(arguments_f, args_mins, args_maxs)]
        arguments_converted = []
        for comb in combinations:
            iloczyn = 1
            for idx in comb:
                iloczyn *= arguments_f[idx]
            arguments_converted.append(iloczyn)

        arg_line_strings_converted.append(' '.join([str(val) for val in arguments_converted]))

    trainee.mainLines(int_indexes, multipliers, arg_line_strings_converted)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('-t', type=str,
                        help='A train set')
    args = parser.parse_args()
    train_set = args.t

    sys.exit(main(train_set))
