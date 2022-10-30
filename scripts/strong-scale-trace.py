import glob
import os
import sys

from pathlib import Path

from multiprocessing import Pool


class CopyTask:
    def __init__(self, fpin, fpout, off, sz):
        self.fpin = fpin
        self.fpout = fpout
        self.off = off
        self.sz = sz

    def __str__(self):
        return (
            f"CopyTask[{self.off}, {self.sz}]\n\tFROM: {self.fpin}\n\tTO: {self.fpout}"
        )


def get_ts():
    trace_in = "/mnt/lustre/carp-big-run/particle.compressed.uniform"
    all_ts = glob.glob(trace_in + "/T.*")
    all_ts = sorted(all_ts, key=lambda x: int(x.split(".")[-1]))
    return all_ts


def get_copy_tasks(ts):
    files_in = glob.glob(ts + "/eparticle*")
    all_copy_tasks = []
    for f in files_in:
        fout = f.replace("uniform", "uniform.strongscaled")
        dir_out = Path(fout).parent.parent
        fsz = os.path.getsize(f)
        assert fsz % 4 == 0
        itemsz = fsz / 4
        itemsz_half = int(itemsz / 2)
        fsz_half = int(itemsz_half * 4)

        fpin = Path(f)
        epart, ts, rank = fpin.name.split(".")
        fnout_a = f"{epart}.{ts}.{rank}"
        fnout_b = f"{epart}.{ts}.{int(rank) + 512}"
        fpout_a = dir_out / f"T.{ts}" / fnout_a
        fpout_b = dir_out / f"T.{ts}" / fnout_b

        fh = CopyTask(f, fpout_a, 0, fsz_half)
        sh = CopyTask(f, fpout_b, fsz_half, fsz)
        all_copy_tasks.append(fh)
        all_copy_tasks.append(sh)

    return all_copy_tasks


def run_copy_task(task):
    print(f"Running {task}")
    fdata = open(task.fpin, "rb").read()
    fdata_to_write = fdata[task.off : task.sz]

    #  fdir = os.path.dirname(task.fpout)
    fdir = Path(task.fpout).parent
    fdir.mkdir(parents=True, exist_ok=True)

    with open(task.fpout, "wb+") as fout:
        fout.write(fdata_to_write)


def run_all_copy_tasks(copy_tasks):
    with Pool(32) as p:
        p.map(run_copy_task, copy_tasks)


def run():
    all_ts = get_ts()
    for ts in all_ts:
        copy_tasks = get_copy_tasks(ts)
        run_all_copy_tasks(copy_tasks)


if __name__ == "__main__":
    run()
