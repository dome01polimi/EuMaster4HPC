import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class OmpMpiRatio(rfm.RunOnlyRegressionTest):

    num_cpus_per_task_ = parameter([1, 2, 4, 8, 16])
    num_nodes_ = parameter([1, 2, 4, 8])

    def __init__(self):
        super().__init__()
        self.num_tasks_per_node = 128 // self.num_cpus_per_task_
        self.num_cpus_per_task = self.num_cpus_per_task_
        self.num_tasks = self.num_nodes_ * self.num_tasks_per_node
        self.num_tasks_per_socket = self.num_tasks_per_node // 8
        self.current_pwd = os.getcwd()
        
    # Metadata
    valid_systems = ['deucalion']  # Update with your system and partition
    valid_prog_environs = ['x86_GNU']             # Update with the programming environment
    descr = 'ReFrame test for QMeCha VMC simulation with Graylog integration'
    executable = '/usr/bin/time'
    time_limit = '10h'

    @run_before('run')
    def setup_execution(self):
        # Pre-run commands for input preparation
        home_dir = "~"
        self.env_vars = {
            'QMECHA_EXE': f'{home_dir}/opt/{self.current_environ.name.replace("_", "/")}/QMeCha/bin/QMeCha',
            'QMECHA_TEST_DIR': 'tests/PerformanceTests/OMPMPIRatio/',
            'WORKING_DIR': self.stagedir,
            'CURR_ENV' : self.current_environ.name,
            'OMP_NUM_THREADS' : self.num_cpus_per_task,
            'OPENBLAS_NUM_THREADS' : 1,
            'walker_tasks_per_node' : 128
        }

        os.system(f"cd {self.stagedir}")
        os.system(f"cp {self.env_vars['QMECHA_TEST_DIR']}start/*.xyz {self.stagedir}/")
        os.system(f"cp {self.env_vars['QMECHA_TEST_DIR']}start/*.bas {self.stagedir}/")
        os.system(f"cp {self.env_vars['QMECHA_TEST_DIR']}start/pseudo.dat {self.stagedir}/")
        os.system(f"cp -rf {self.env_vars['QMECHA_TEST_DIR']}start/wvfn.save {self.stagedir}/")
        os.system(f"cp custom_mpirun.sh {self.stagedir}")
        os.system(f"chmod +x {self.stagedir}/custom_mpirun.sh")
        os.system(f"sed 's/numthreads/'{self.num_cpus_per_task}'/g' {self.env_vars['QMECHA_TEST_DIR']}inputs/vmc.inp > {self.stagedir}/input")

        # Dynamically set the srun command using test parameters
        self.executable_opts = [
            f"{self.env_vars['QMECHA_EXE']} -i input -m *.xyz -b *.bas -p pseudo.dat -j ma -sn OmpMPIRatio_{self.num_cpus_per_task}_{self.num_tasks}"
        ]

        # Post-run cleanup
        self.post_run = ['rm -rf pseudo.dat wvfn.save *.bas *.xyz *.inp']


    @sanity_function
    def validate(self):
        return True


    @performance_function('s')
    def execution_time(self):
        return sn.extractsingle(r'Total simulation time\s+\[sec\.\]\s+:\s+(\d+\.\d+E[+-]?\d+)',
                                self.stdout, tag=1, conv=lambda x : float(x))

    def info(self):
        return f''
