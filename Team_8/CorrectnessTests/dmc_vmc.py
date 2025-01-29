import reframe as rfm
import reframe.utility.sanity as sn
import os
import subprocess

@rfm.simple_test
class DmcVmcCorrectnessTest(rfm.RunOnlyRegressionTest):

    calculation = parameter(["dmc_1_0.2", "dmc_1_0.2_nc", "vmc_3dg_ts"])
    rpf = parameter(["H2O/RPF_J12A", "H2O/RSD_J11A", "H2O/RSD_J12A", "H2O/RSD_J12D", "H2O/RSD_J12F", "H2O/RSD_J21A", "H2O/RSD_J22A", "H2O/RSG_J12A", "H2O/RTG_J12A", "OH/RSD_J12A", "OH/RSG_J12A", "OH/UPF_J12A", "OH/USD_J12A", "OH/USG_J12A", "OH/UTG_J12A"])

    def __init__(self):
        super().__init__()
        self.num_tasks_per_node = 1
        self.num_tasks = 1
        self.num_cpus_per_task = 6
        self.current_pwd = os.getcwd()
  
    # Metadata
    valid_systems = ['deucalion']  # Update with your system and partition
    valid_prog_environs = ['x86_GNU']              # Update with the programming environment
    descr = 'ReFrame test for QMeCha VMC simulation with Graylog integration'
    executable = '/usr/bin/time'
    time_limit = '1h'

    @run_before('run')
    def setup_execution(self):
        # Pre-run commands for input preparation
        home_dir = "~"
        self.env_vars = {
            'QMECHA_EXE': f"{home_dir}/opt/{self.current_environ.name.replace('_', '/')}/QMeCha/bin/QMeCha",
            'QMECHA_TEST_DIR': 'tests/CorrectnessTests/',
            'CURR_ENV' : self.current_environ.name

        }

        # Prepare input data 
        os.system(f"cd {self.stagedir}")
        os.system(f"cp {self.env_vars['QMECHA_TEST_DIR']}ElectronicWavefunctions/AllElectron/{self.rpf}/*.bas {self.stagedir}/")
        os.system(f"cp {self.env_vars['QMECHA_TEST_DIR']}ElectronicWavefunctions/AllElectron/{self.rpf}/*.xyz {self.stagedir}/")
        os.system(f"cp -rf {self.env_vars['QMECHA_TEST_DIR']}ElectronicWavefunctions/AllElectron/{self.rpf}/start {self.stagedir}/wvfn.save")

        os.system(f"cp {self.env_vars['QMECHA_TEST_DIR']}inputs/{self.calculation}.inp {self.stagedir}/{self.calculation}.inp")
        os.system(f"sed 's/NUM_WALKERS/'{self.num_cpus_per_task}'/g' {self.stagedir}/{self.calculation}.inp > {self.stagedir}/input")
        
        os.system(f"cp {self.env_vars['QMECHA_TEST_DIR']}ElectronicWavefunctions/AllElectron/{self.rpf}/{self.calculation[:3]}_eval{self.calculation[3:]}.ref {self.stagedir}/reference.ref")
        os.system(f"cp CorrectnessTests/test_functions.sh {self.stagedir}/")
        os.system(f"cp custom_mpirun.sh {self.stagedir}")
        os.system(f"chmod +x {self.stagedir}/custom_mpirun.sh")

        # Dynamically set the srun command using test parameters
        self.executable_opts = [
            f"{self.env_vars['QMECHA_EXE']} -i input -m *.xyz -b *.bas -j m{self.rpf[-1].lower()} -sn {self.calculation}_correctness_test"
        ]
        
        # Post-run cleanup
        self.post_run = [f"rm -rf *.bas *.xyz input wvfn.save opt.inp input"]

    @sanity_function
    def validate(self):
        script_path = f"./test_functions.sh"
        output_path = f"{self.stagedir}/*.dat"
        reference_path = f"{self.stagedir}/*.ref"
        result = subprocess.run(
            [script_path, 'check_test_results_eval', '0.00001', output_path, reference_path], 
            capture_output=True,
            text=True)

        if result.returncode != 0:
            return False
        return True

    @performance_function('s')
    def dummy(self):
        return 0

    def info(self):
        return f'%rpf:{self.rpf}%calculation:{self.calculation}'
