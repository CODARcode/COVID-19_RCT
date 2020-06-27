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

        gromacs_path = '/gpfs/alpine/world-shared/csc393/hrlee/gromacs-5.1.5/build/bin/gmx'
        gromacs_example_path = '/gpfs/alpine/world-shared/csc393/hrlee/'

        for i in range(1, task_count + 1):
            t = entk.Task()
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
                'threads_per_process': 1,#4
                'thread_type': 'CUDA'
            }

            self.s.add_tasks(t)

        self.p.add_stages(self.s)

    def run(self):
        self.am.workflow = [self.p]
        self.am.run()


if __name__ == "__main__":

    benchmark = BENCHMARK()

    n_nodes = 1
    benchmark.set_resource(res_desc = {
        'resource': 'ornl.summit',
        'queue'   : 'batch',
        'walltime': 1440, #MIN
        'cpus'    : 168 * n_nodes,
        'gpus'    : 6 * n_nodes,
        'project' : 'MED110'
        })
    benchmark.sim(task_count=6)
    benchmark.run()
