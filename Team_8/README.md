# Preliminaries 
After cloning this repo, make sure to clone also the `qmecha_beta` library in your home directory:
```
cd ~
git clone git@gitlab.com:uniluxembourg/hpc/eumaster4hpc/challenge-2024-2025/qmecha_beta.git
```
To compile it, use
```
cd SoftwareAtelier/compilation
./compile_all.sh
cd ..
```

# How to run
First, copy the `test` folder from QMeCha to the `SoftwareAtelier` folder:
```
cp -r qmecha_beta/tests SoftwareAtelier/
```
From the login node, in order to run reframe tests do:
```
module load ReFrame
cd SoftwareAtelier
reframe --prefix reframe_out -C deucalion.py -c path_to_test/test_name.py -r
```
For example, to run the 2stepopt test
```
reframe --prefix reframe_out -C deucalion.py -c CorrectnessTests/2stepopt.py.py -r
```
and to run the `dmc_vmc` correctness test
```
reframe --prefix reframe_out -C deucalion.py -c CorrectnessTests/dmc_vmc.py -r
```
It is important to notice that all tests must be started from the root folder of the repository.


# How to run Grafana
In order to access Grafana from a local machine, it is necessary to use ssh forwarding (e):
```
ssh -L 3000:[ln03]:3000 <username>@deucalion
```
N.B.: We here assume that deucalion ssh connection is properly setup in the `~/.ssh/config` file. If not please refer to the Deucalion user manual.

In order to run the Grafana server on a Deucalion login node launch:
```
cd SoftwareAtelier
./run_grafana.sh
```
The server will run by default on the port 3000 that is mapped to the local address `localhost:3000`, accessible from a browser.
The password for the admin user is "admin".

Once the Grafana server is no more needed, insert `Ctrl+C` on the terminal where the server was started in order to clean-up the environment.
