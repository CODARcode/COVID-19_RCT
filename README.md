# Accelerating Therapeutic Discovery against COVID-19 using Heterogeneous Tasks

## Workflow Description

This repository includes two scripts written in Python using [RADICAL Cybertools](https://radical-cybertools.github.io/) (specifically Ensemble Toolkit), to benchmark the performance of simplified drug workflows used to fight against the COVID-19 pandemic. `benchmark_mixed.py` is a heterogeneous workflow with both CPU and GPU tasks, while `benchmark_gpu.py` contains GPU tasks only for comparison purposes. CPU tasks use [NAMD](https://www.ks.uiuc.edu/Research/namd/) to perform simulation of large biomolecular systems. GPU tasks use [GROMACS](http://www.gromacs.org/) to do free energy calculation involving ensemble MD simulations.

## Installation (Summit @ ORNL)

### RADICAL Cybertools (using Python Virtual Environment)

```
(python3)
. "/sw/summit/python/3.7/anaconda3/5.3.0/etc/profile.d/conda.sh"
conda create -n benchmark python=3.7 -y
conda activate benchmark
pip install radical.entk radical.pilot radical.saga radical.utils --upgrade
```

### Environmental Variables (RabbitMQ and MongoDB)

```
export RMQ_HOSTNAME=129.114.17.233
export RADICAL_PILOT_DBURL="mongodb://rct:rct_test@129.114.17.233:27017/rct_test"
```

Note that installation of the binaries used by either CPU tasks or GPU tasks are not needed, since we are using pre-installed binaries on Summit in shared locations from other efforts.

## Resource Configuration

- `res_desc` includes:
   - 'resource': HPC facility name, e.g., 'ornl.summit'
   - 'queue':
      - 'batch' for up to 2 hours time to completion at `ornl.summit`
      - 'killable' for up to 24 hours time to completion at `ornl.summit`
   - 'cpus': On Summit each node has 42 cores and each core has 4 hardware threads, so we consider 168 parallel threads
   - 'gpus': a number of GPU cores equal to N simulations (1 MD/ML run: 1 GPU)

## Run

The main script requires to be placed at a writable space before running. Output files are stored in sub-directories of the current directory. Locate this code repository at $MEMBERWORK/{{PROJECTID}}/ and run the script there. $HOME directory does not work when running the script since it becomes a read-only filesystem when a job is running.

```
$ python benchmark_mixed.py
$ python benchmark_gpu.py
```

## Performance (Avg time to completion on Summit, unit: minute)

Multiple Task TTX (CPU): 41 CPU tasks on 1 node
Multiple Task TTX (GPU): 6 GPU tasks on 1 node

| Task Type   | Signle Task TTX | Multiple Task TTX | Bug Description |
| ----------- | --------------- | ----------------- | --------------- |
| CPU         | 6.9             | 7.0               | N/A             |
| GPU         | 13.1            | 57.2              | One task finishes much later than others |
