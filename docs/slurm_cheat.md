# Slurm (Cheat Sheet)

| What | Command |
|------|---------|
| Connect to submission nodes | `ssh shellhost` |
| Show workers | `sinfo` |
| Show schedule | `squeue -l` |
| My jobs | `squeue -u $(whoami)` |
| Submit interactive job | `srun --time=01:00:00 --cpus-per-task=1 --pty bash -i` |
| Submit batch job | `sbatch job.sh` |
| Submit batch job w/o shell script | `sbatch --wrap="python -m ..."` |
| Target GPU nodes | `sbatch --partition=GPUampere,GPUhopper --gpus=1 --time=01:00:00 job.sh` |
| Allocate resources for later | `salloc [ARGS] --time=01:00:00` |
| Show job info | `scontrol show jobid -dd [JOB_ID]` |
| Show assigned GPUs | `scontrol show jobid -dd [JOB_ID] | grep IDX` |
| Cancel job | `scancel [JOB_ID]` |
