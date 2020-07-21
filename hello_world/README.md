# Hello World on OSG

This directory is the a first introduction to submitting jobs on OSG. We go through a few examples of common tasks, using just simple bash scripts without any input/output files, etc. 

For more information, see the HTCondor docs [here](https://htcondor.readthedocs.io/en/v8_9_7/).

Below we go through 2 example workflows, the first of which is a simple Hello World job and the second involves multiple jobs with slightly different arguments passed as input.

## 1. Hello, it's me
##### Overview of submit script and executable
The first job we look at is `submit_01hello.sub`. This is a Condor _submit script_, analogous to SLURM's `.sbatch` scripts we use on, e.g. the Midway cluster at UChicago. Before submitting, take a look inside. 

The first line in the submit file is 
```
executable = 01hello.sh
```
This is the actual executable that will be run on the job. Typically this will be a simple bash script that sets up the environment and then maybe runs something else, but it could also be an executable python script; however, one needs to remember that this job will be running on another machine and thus won't have access to a local python interpreter. It's recommended to have this executable be a bash script. 

Anyway, you will see that `01hello.sh` is just a simple jobs prints "Hello World" to standard output. If you want, try running this bash script in your local terminal (if you do this remember to make sure it's executable first, with `chmod +x 01hello.sh`). Now back to the submit script...

Also included in the submit script are lines for the error/output/logs which you can see we point to the local `logs` directory. The `Error` log file will contain stderr, `Output` will contain stdout, and `Log` contains metadata about the job, like when/where it is running, resource usage, etc.

You then see lines for requesting resources like memory, # cpus, and disk space, which are self-explanatory. The final lines are XENON-specific and should just be considered boilerplate in all of our OSG scripts.
```
+WANT_RCC_ciconnect = True
+ProjectName = "xenon1t"
+AccountingGroup = "group_opportunistic.xenon1t.processing"
```

The last line just says `queue`, which is the command to tell condor to submit the job. As we will see, we can submit multiple jobs by

##### Submitting the job
After understanding what the job does, we are ready to submit it to the grid. The command (and expected output )is 

```
$ condor_submit submit_01hello.sub
Submitting job(s).
1 job(s) submitted to cluster 3578993.
```

##### Job Status
To check the status of the job, do

```
[ershockley@login-el7 hello_world]$ condor_q


-- Schedd: login-el7.xenon.ci-connect.net : <192.170.227.173:9618?... @ 07/21/20 16:03:23
OWNER      BATCH_NAME     SUBMITTED   DONE   RUN    IDLE  TOTAL JOB_IDS
ershockley ID: 3578994   7/21 16:03      _      _      1      1 3578994.0
```

where you can see that I have one job in the `IDLE` state. This just means it hasn't started running yet; when it starts running the will instead be a `1` under the `RUN` column. Sometimes it take a bit for the job to start running, as condor needs to search for machines all over the world for openings to run our job.

TODO: using `-analyze` and `-better-analyze` to check on jobs. 

You can also get some information on the job by looking at the `Log` file specified in the submit script.

##### Job Completion
When the job finishes (regardless of whether it was successful or not), the error/output is copied to the specified location from the submit script.

To see the output of our script run on the grid, see 

```
[ershockley@login-el7 hello_world]$ cat logs/01hello.out
----------------------------
| HELLO WORLD, this is OSG |
----------------------------
```

## 2. Passing Arguments
We typically use the vast resources of OSG to parallelize our workflow and make it faster/possible. Thus it is useful to be able to pass different arguments to the same executable. A simple example of this in action is our second example script: `submit_02count.sub`

This submit script calls the executable `02count.sh`, which as you can see takes as input a number to count to. You can test this script locally with
```
[ershockley@login-el7 hello_world]$ ./02count.sh 5

----------------------------
| HELLO WORLD, this is OSG |
----------------------------
Look, I can count to 5 :D
    1
    2
    3
    4
    5
```

With Condor, we pass arguments to the executable using the `arguments` field of the submit script, where as you can see in `submit02_count.sub` we have `arguments = 5`. This will then run the above job on the grid with argument `5` passed as input. 

You can submit this job following the same procedure as above, and then check the output in `logs/02count.out`. 


## 3. Same job, different arguments
It's often useful to pass many different arguments to the same executable. If the arguments are integers, we can make use of Condor's `queue` functionality to do this in a single shot. 

In `submit03_multiple.sub`, we use the same executable as above, `02count.sh`, but you can see that we modify to have
 
```
arguments = $(Process)

queue 10
```

The `queue 10` line means we are going to submit 10 jobs instead of one, and the `$(Process)` variable is a placeholder for the index of the corresponding job that is running. That is, we will submit 10 jobs which have corresponding $(Process) variables ranging between 0--9. To differentiate the different error/output/log files of the jobs, you can see that we also pass $(Process) there.

When you submit this job, you should see:
```
[ershockley@login-el7 hello_world]$ condor_submit submit_03multiple.sub
Submitting job(s)..........
10 job(s) submitted to cluster 3578996.
```
And there will be 10 corresponding error/output/logs as well. When the jobs complete, take a look at the output files to see how the jobs did different things. For example, 

```
[ershockley@login-el7 hello_world]$ cat logs/03multiple.0.out

----------------------------
| HELLO WORLD, this is OSG |
----------------------------
I can't count :'(
```

compared to...
```
[ershockley@login-el7 hello_world]$ cat logs/03multiple.9.out

----------------------------
| HELLO WORLD, this is OSG |
----------------------------
Look, I can count to 9 :D
    1
    2
    3
    4
    5
    6
    7
    8
    9
```

This type of job submission is quite handy for simulation jobs, for example, where we often want to run the same code many times, just split into many jobs. 
