#!/usr/bin/python3
# Auto-tuner prototype
# Built for INE5540 robot overlords

import subprocess # to run stuff
import sys # for args, in case you want them
import time # for time
import operator

def tuner(argv):
    times = {}
    best_half = [1,2]
    while len(best_half) > 1:
        times = compare_steps(1, 9, 2, 9, 3)
        ordered = sorted(times.items(), key=operator.itemgetter(1))
        best_half = ordered[:len(ordered)//2]
    print(best_half)
    #print('Best: Step={}, opt_level={}, time={}'.format(best[0], best[1], best[2]))

def compare_steps(step_min, step_max, mult, matrix_size, optimization_level):
    best = (0,0,500000)
    times = {}
    amplitude = [step_min, step_max]
    for i in range(step_min, step_max):
        times[i] = 0
    for i in range(mult):
        for step in range(step_min, step_max):
            exec_time = compile_and_run(step, optimization_level, matrix_size)
            times[step] += exec_time
            #print('Step={}, opt_level={}, time={}'.format(step, optimization_level, exec_time))
            if exec_time > 0 and exec_time < best[2]:
                best = (step, optimization_level, exec_time)
    #print('Final results:')
    for i in times.keys():
        #print('Step={}, opt_level={}, time={}'.format(i, optimization_level, times[i]/mult))
        times[i] /= mult
    return times


def compile_and_run(step_value, optimization_level, matrix_size):
    exec_file = 'matmult'
    compiler = 'gcc'
    compilation_line = [compiler,'-o',exec_file,'mm.c']
    steps = ['-DSTEP=' + str(2**step_value)]
    optimization_flag = ['-O' + str(optimization_level)]

    # Compile code
    compilation_try = subprocess.run(compilation_line + steps + optimization_flag)
    if (compilation_try.returncode != 0):
        return -2

    # Run code
    input_size = str(matrix_size)
    t_begin = time.time() # timed run
    run_trial = subprocess.run(['./'+exec_file, input_size])
    t_end = time.time()
    if (run_trial.returncode == 0):
        return t_end - t_begin
    else:
        return -1


if __name__ == "__main__":
    tuner(sys.argv[1:]) # go auto-tuner
