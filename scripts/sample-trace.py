import struct
import sys

def read_trace(trace_path, ibeg, iend):
    bytes_beg = ibeg * 4
    bytes_end = iend * 4

    f = open(trace_path, "rb").read()
    bytes_to_decode = f[bytes_beg:bytes_end]
    nitems = iend - ibeg
    unpackstr = f'{nitems}f'

    items = struct.unpack(unpackstr, bytes_to_decode)
    for idx, item in enumerate(items):
        print(f'{ibeg + idx}: {item}')

if __name__ == '__main__':
    ts = 200
    rank = 699
    ibeg = 0
    iend = 10

    trace_root = '/mnt/lustre/carp-big-run/particle.compressed.uniform.strongscaled'
    trace_path = f"{trace_root}/T.{ts}/eparticle.{ts}.{rank}"
    read_trace(trace_path, ibeg, iend)
