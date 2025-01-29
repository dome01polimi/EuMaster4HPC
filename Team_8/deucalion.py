from reframe.core.backends import register_launcher
from reframe.core.launchers import JobLauncher


@register_launcher('custom_mpirun')
class MySmartLauncher(JobLauncher):
    def command(self, job):
        return ['./custom_mpirun.sh', str(job.num_tasks), str(job.num_tasks_per_node)]


site_configuration = {
    'systems': [
        {
            'name': 'deucalion',
            'descr': 'HPC Cluster',
            'hostnames': ['.*'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'normal-x86',
                    'descr': 'Deucalion compute nodes x86',
                    'scheduler': 'squeue',
                    'launcher': 'custom_mpirun',
                    'access': ['--partition=normal-x86', '--qos=normal', '--account=eehpc-dev-2024d08-066x'],
                    'max_jobs': 65536,
                    'environs': ['x86_GNU', 'x86_Intel'],
                },
                {
                    'name': 'normal-arm',
                    'descr': 'Deucalion compute nodes arm',
                    'scheduler': 'squeue',
                    'launcher': 'custom_mpirun',
                    'access': ['--partition=normal-arm', '--qos=normal', '--account=eehpc-dev-2024d08-066a'],
                    'max_jobs': 65536,
                    'environs': ['arm_GNU', 'arm_Fujitsu'],
                }
            ]
        }
    ],
    'environments': [
        {
            'name': 'x86_GNU',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn' : 'mpif90',
            'target_systems': ['deucalion']
        },
        {
            'name': 'x86_Intel',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn' : 'mpif90',
            'target_systems': ['deucalion']
        },
        {
            'name': 'arm_GNU',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn' : 'mpif90',
            'target_systems': ['deucalion']
        },
        {
            'name': 'arm_Fujitsu',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn' : 'mpif90',
            'target_systems': ['deucalion']
        }
    ],
    'logging': [
        {
	        'handlers': [
                {
                    'type': 'file',
                    'name': 'reframe.log',
                    'timestamp': '%FT%T',
                    'level': 'debug2',
                    'format': ('[%(asctime)s] %(levelname)s: '
                               '%(check_info)s: %(message)s'),
                    'append': False
                },
                {
                    'type': 'file',
                    'name': 'reframe.out',
                    'timestamp': '%FT%T',
                    'level': 'info',
                    'format': '%(message)s',
                    'append': False
                }
            ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': '.',
                    'level': 'info',
                    'format': ('%(check_result)s,'
                           '%(check_job_completion_time)s,'
                           '%(check_info)s,'
                           '%(check_system)s:%(check_partition)s,'
                           '%(check_environ)s,'
                           '%(check_num_tasks)s,'
                           '%(check_num_tasks_per_node)s,'
                           '%(check_num_cpus_per_task)s,'
                           '%(check_perfvalues)s'),
                    'format_perfvars': ('%(check_perf_value)s,'
                                    '%(check_perf_unit)s,'), 
                    'append': False
                }
	        ]
        }
    ]
}
