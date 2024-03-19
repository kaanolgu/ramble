# Copyright 2022-2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# https://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or https://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

from ramble.appkit import *


class Babelstream(SpackApplication):
    """Babelstream is a benchmark application to measure memory bandwidth
    See https://github.com/UoB-HPC/BabelStream for more information

    The spack_spec for babelstream determines the value for the exec_name variable.
    """
    name = "babelstream"

    tags('sycl','sycl2020','omp','cuda','ocl','tbb','acc','hip','thrust','raja','std','kokkos')

    maintainers('douglasjacobsen')

    default_compiler('gcc12', spack_spec='gcc@12.2.0')

    software_spec('babelstream',
                  spack_spec='babelstream@5.0',
                  compiler='gcc12')
    executable('get_bin',
               template=['cp {env_path}/.spack-env/view/bin/{exec_name} {experiment_run_dir}/{exec_name}'],
               use_mpi=False, output_capture=OUTPUT_CAPTURE.STDERR)
    executable('get_bin_fortran',
               template=['cp {env_path}/.spack-env/view/bin/BabelStream.{f_compiler_name}.{f_model} {experiment_run_dir}/{exec_name}'],
               use_mpi=False, output_capture=OUTPUT_CAPTURE.STDERR)

    executable('execute_template', '{exec_pre} {exec_name} --arraysize $(({array_size})) {additional_args}',
               use_mpi=False, output_capture=OUTPUT_CAPTURE.ALL)

    executable('execute_fortran', './{exec_name} --arraysize $(({array_size})) {additional_args}',
               use_mpi=False, output_capture=OUTPUT_CAPTURE.ALL)

    executable('output_csv', 'echo "Babelstream |{exec_name} | {array_size} | {partition}" >> ./perflog.csv',
               use_mpi=False, output_capture=OUTPUT_CAPTURE.ALL)


    workload('isambard-phase3', executables=['get_bin','execute_template'])

    workload('fortran', executables=['get_bin_fortran','execute_fortran'])
    
    workload('print-csv', executables=['get_bin_fortran','execute_fortran'])
    

    workload_variable('exec_pre',
                      description='Pre Command for execution (e.g. numatcl)',
                      default='', workloads=['isambard-phase3', 'fortran'])

    workload_variable('exec_name',
                      description='Name of babelstream executable. Depends on spec used to installed babelstream',
                      default='std-data-stream', workloads=['isambard-phase3', 'fortran','print-csv'])

    workload_variable('array_size',
                      description='Number of elements in array that will be streamed',
                      default='2**27', workloads=['isambard-phase3', 'fortran','print-csv'])

    workload_variable('num_times',
                      description='Number of times to repeat stream test',
                      default='10', workloads=['isambard-phase3', 'fortran'])

    workload_variable('additional_args',
                      description='Additional arguments to babelstream executable',
                      default='', workloads=['isambard-phase3', 'fortran'])

    workload_variable('partition',
                      description='Define which partition we are going to use for execution',
                      default='milan', workloads=['isambard-phase3', 'fortran','print-csv'])

#  BabelStream
#  Version: 5.0
#  Implementation: OpenMP
#  Running kernels 100 times
#  Precision: double
#  Array size: 268.4 MB (=0.3 GB)
#  Total size: 805.3 MB (=0.8 GB)
#  Init: 0.074336 s (=10833.309933 MBytes/sec)
#  Read: 0.239713 s (=3359.463988 MBytes/sec)
#  Function    MBytes/sec  Min (sec)   Max         Average
#  Copy        22381.909   0.02399     0.03809     0.02490
#  Mul         21829.570   0.02459     0.02709     0.02538
#  Add         23909.045   0.03368     0.03851     0.03456
#  Triad       23935.398   0.03364     0.05200     0.03470
#  Dot         25113.014   0.02138     0.05118     0.02234

    success_criteria('data_header', mode='string', match=r'.*Function.*MBytes.*')

    figure_of_merit('Version',
                    fom_regex=r'\s*Version: (?P<ver>\S+)',
                    group_name='ver', units='')

    figure_of_merit('Implementation',
                    fom_regex=r'\s*Implementation: (?P<impl>\S+)',
                    group_name='impl', units='')

    figure_of_merit('Precision',
                    fom_regex=r'\s*Precision: (?P<prec>\S+)',
                    group_name='prec', units='')

    figure_of_merit('Number of times',
                    fom_regex=r'\s*Running kernels (?P<times>[0-9]+) times',
                    group_name='times', units='')

    size_regex = r'\s*(?P<type>\S+) size: (?P<size_mb>[0-9]+\.[0-9]+) MB \(=(?P<size_gb>[0-9]+\.[0-9]+) GB\)'

    figure_of_merit('{type} size MB',
                    fom_regex=size_regex,
                    group_name='size_mb', units='MB')

    figure_of_merit('{type} size GB',
                    fom_regex=size_regex,
                    group_name='size_gb', units='GB')

    method_regex = r'\s*(?P<method>\S+)\s+(?P<rate>[0-9]+\.[0-9]+)\s+(?P<min>[0-9]+\.[0-9]+)\s+(?P<max>[0-9]+\.[0-9]+)\s+(?P<avg>[0-9]+\.[0-9]+)'

    figure_of_merit('{method} rate',
                    fom_regex=method_regex,
                    group_name='rate', units='MB/s')

    figure_of_merit('{method} min',
                    fom_regex=method_regex,
                    group_name='min', units='s')

    figure_of_merit('{method} max',
                    fom_regex=method_regex,
                    group_name='max', units='s')

    figure_of_merit('{method} avg',
                    fom_regex=method_regex,
                    group_name='avg', units='s')
