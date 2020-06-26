from radical import entk
import os
import argparse, sys

class BENCHMARK(object):

    def __init__(self):
        self._set_rmq()
        self.am = entk.AppManager(hostname=self.rmq_hostname, port=self.rmq_port)
        self.p = entk.Pipeline()
        self.s = entk.Stage()

    def _set_rmq(self):
        self.rmq_port = int(os.environ.get('RMQ_PORT', 33239))
        self.rmq_hostname = os.environ.get('RMQ_HOSTNAME', 'two.radical-project.org')

    def set_resource(self, res_desc):
        res_desc["schema"] = "local"
        self.am.resource_desc = res_desc

    def sim(self, task_count):

        #os.system("export RADICAL_PROFILE=\"TRUE\"")
        #os.system("export RADICAL_PILOT_PROFILE=\"TRUE\"")
        #os.system("export RADICAL_ENTK_PROFILE=\"TRUE\"")
        #os.system("export RADICAL_VERBOSE=\"DEBUG\"")
        #os.system("export RADICAL_LOG_LVL=\"DEBUG\"")
        #os.system("export RADICAL_LOG_TGT=\"radical.log\"")

        gromacs_path = '/gpfs/alpine/world-shared/csc393/hrlee/gromacs-5.1.5/build/bin/gmx'
        gromacs_example_path = '/gpfs/alpine/world-shared/csc393/hrlee/'

        for i in range(1, task_count + 1):

            t = entk.Task()

            """if i <= 20:
                t.pre_exec = [
                    "module load gcc/7.4.0",
                    "export OUTDIR=\"/gpfs/alpine/med110/scratch/litan/FFEA/output/rep{}\"".format(i),
                    "mkdir -p $OUTDIR"
                ]
                t.executable = '/gpfs/alpine/csc299/scratch/litan/FFEA/ffea-2.6.0/build/bin/ffea'
                t.arguments = ['/gpfs/alpine/csc299/scratch/litan/FFEA/ffea-2.6.0/build/bin/input/emd_5043_albert_E1GPa.ffea']
                t.post_exec = []
                t.cpu_reqs = {
                    'processes': 1,
                    'process_type': None,
                    'threads_per_process': 1,
                    'thread_type': 'OpenMP'
                }
                t.gpu_reqs = {
                    'processes': 0,
                    'process_type': None,
                    'threads_per_process': 1,
                    'thread_type': 'CUDA'
                }"""
            '''if i > 6:
                t.executable = '/bin/date'''
            if i <= 4:
                t.pre_exec = [
                    ##"export OMP_NUM_THREADS=1",
                    "export WORKDIR=\"/gpfs/alpine/csc299/scratch/litan/NAMD\"",
                    "export OUTDIR=\"$WORKDIR/output/rep{}\"".format(i),
                    #"mkdir -p $OUTDIR",
                    "export NAMD=\"/ccs/home/jimp/NAMD_binaries_Summit/NAMD_LATEST_Linux-POWER-MPI-smp-Summit\"",
                    #". /ccs/home/litan/miniconda3/etc/profile.d/conda.sh",
                    #"conda activate entk",
                    "module load gcc/8.1.1 spectrum-mpi/10.3.1.2-20200121",
                    "module load fftw/3.3.8"
                ]
                t.executable = '$NAMD/namd2'
                t.arguments = ['$OUTDIR/ubq_ws_eq.conf']#'+ppn 1', '+replicas 1', ' > $OUTDIR/ubq_ws_eq.log'
                t.post_exec = []

                t.cpu_reqs = {
                    'processes': 1,
                    'process_type': None,
                    'threads_per_process': 4,
                    'thread_type': 'OpenMP'
                }
                '''t.gpu_reqs = {
                    'processes': 0,
                    'process_type': None,
                    'threads_per_process': 1,
                    'thread_type': 'CUDA'
                }'''
            else:
                '''t.pre_exec = [
                    ##"export OMP_NUM_THREADS=1",
                    "export INPATH=\"$MEMBERWORK/med110/inpath\"",
                    ". /ccs/home/litan/miniconda3/etc/profile.d/conda.sh",
                    "conda activate wf3",
                    "module load cuda/10.1.243 gcc/7.4.0 spectrum-mpi/10.3.1.2-20200121",
                    "mkdir -p $INPATH; cd $INPATH",
                    "export OUTPATH=$INPATH",#"export OUTPATH=\"$INPATH/rep{}\"".format(i),
                    "mkdir -p $OUTPATH; cd $OUTPATH",
                    "rm -f traj.dcd sim.log"
                ]
                t.executable = '/ccs/home/litan/miniconda3/envs/wf3/bin/python3.7'
                t.arguments = ['$INPATH/sim_esmacs.py', '-i$INPATH', '-n0.2', '-r{}'.format(i)]
                t.post_exec = []'''
                grompp_bin = (gromacs_path + ' grompp -f ' + 
                    (' %s/gromacs_example/inp_files/grompp.mdp' % gromacs_example_path) +
                     ' -c ' +
                    (' %s/gromacs_example/inp_files/input.gro' % gromacs_example_path) +
                     ' -p ' +
                    (' %s/gromacs_example/inp_files/topol.top' % gromacs_example_path) +
                     ' &> grompp.log')
                t.pre_exec = ["module load gcc/8.1.1", grompp_bin]
                t.executable = gromacs_path
                t.arguments = ['mdrun']
                t.post_exec = []
                t.cpu_reqs = {
                    'processes': 1,
                    'process_type': None,
                    'threads_per_process': 4,
                    'thread_type': 'OpenMP'
                }
                t.gpu_reqs = {
                    'processes': 1,
                    'process_type': None,
                    'threads_per_process': 1,
                    'thread_type': 'CUDA'
                }

            self.s.add_tasks(t)

        self.p.add_stages(self.s)

    def run(self):
        self.am.workflow = [self.p]
        self.am.run()


if __name__ == "__main__":

    benchmark = BENCHMARK()

    n_nodes = 4#1
    benchmark.set_resource(res_desc = {
        'resource': 'ornl.summit',
        'queue'   : 'batch',
        'walltime': 1440, #MIN
        'cpus'    : 168 * n_nodes,
        'gpus'    : 6 * n_nodes,
        'project' : 'MED110'
        })
    benchmark.sim(task_count=8)
    benchmark.run()
