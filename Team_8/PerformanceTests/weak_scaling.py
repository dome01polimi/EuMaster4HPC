import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class WeakScalingTest(rfm.RunOnlyRegressionTest):

    num_nodes_ = parameter([1, 2, 4, 8, 16]) 
    calculation = parameter(["opt", "vmc", "dmc"])

    def __init__(self):
        super().__init__()
        self.num_cpus_per_task_ = 16

        self.num_tasks_per_node = 128 // self.num_cpus_per_task_
        self.num_cpus_per_task = self.num_cpus_per_task_
        self.num_tasks = self.num_nodes_ * self.num_tasks_per_node
        self.num_tasks_per_socket = self.num_tasks_per_node // 8

        self.current_pwd = os.getcwd()
        
    # Metadata
    valid_systems = ['deucalion']  # Update with your system and partition
    valid_prog_environs = ['*']             # Update with the programming environment
    descr = 'ReFrame test for QMeCha VMC simulation'
    executable = '/usr/bin/time'
    time_limit = '10h'

    @run_before('run')
    def setup_execution(self):
        # Pre-run commands for input preparation
        home_dir = "~"
        self.env_vars = {
            'QMECHA_EXE': f"{home_dir}/opt/{self.current_environ.name.replace('_', '/')}/QMeCha/bin/QMeCha",
            'QMECHA_TEST_DIR': 'tests/PerformanceTests/WeakScalingW30/',
            'CURR_ENV' : self.current_environ.name
        }

        # Prepare input data 
        os.system(f"cd {self.stagedir}")
        os.system(f"cp -r {self.env_vars['QMECHA_TEST_DIR']}start/* {self.stagedir}/")
        os.system(f"cp {self.env_vars['QMECHA_TEST_DIR']}inputs/{self.calculation}.inp {self.stagedir}/")
        os.system(f"cp custom_mpirun.sh {self.stagedir}")
        os.system(f"chmod +x {self.stagedir}/custom_mpirun.sh")
        os.system(f"sed 's/numthreads/'{self.num_cpus_per_task}'/g' {self.stagedir}/{self.calculation}.inp > {self.stagedir}/input")
        
        # Dynamically set the srun command using test parameters
        self.executable_opts = [
            f"{self.env_vars['QMECHA_EXE']} -i input -m *.xyz -b *.bas -p pseudo.dat -j ma -sn WeakScaling_{self.calculation}_{self.num_tasks}"
        ]
        
        # Post-run cleanup
        self.post_run = [f"rm -rf pseudo.dat *.bas *.xyz input wvfn.save"]

    @sanity_function
    def validate(self):
        return True

    @performance_function('s')
    def execution_time(self):
        return sn.extractsingle(r'Total simulation time\s+\[sec\.\]\s+:\s+(\d+\.\d+E[+-]?\d+)',
                                self.stdout, tag=1, conv=lambda x : float(x))

    def info(self):
        return f'%calculation:{self.calculation}'
