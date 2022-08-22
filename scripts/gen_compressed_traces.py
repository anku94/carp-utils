import sys
import pathlib
import io
import struct
import glob
import argparse

from multiprocessing import Pool


def get_header(fstream):
    (so_char_bits, so_short_int, so_int, so_float, so_double) = struct.unpack(
        "ccccc", fstream.read(5))

    cafe_b = fstream.read(2)
    deadbeef_b = fstream.read(4)
    (cafe,) = struct.unpack("h", cafe_b)
    (deadbeef,) = struct.unpack("i", deadbeef_b)

    float_1 = struct.unpack("f", fstream.read(4))
    double_1 = struct.unpack("d", fstream.read(8))

    v_0 = struct.unpack("i", fstream.read(4))
    dump_type = struct.unpack("i", fstream.read(4))

    (step,) = struct.unpack("i", fstream.read(4))

    imx = struct.unpack("i", fstream.read(4))
    jmx = struct.unpack("i", fstream.read(4))
    jmx = struct.unpack("i", fstream.read(4))

    grid_dt = struct.unpack("f", fstream.read(4))
    dx = struct.unpack("f", fstream.read(4))
    dy = struct.unpack("f", fstream.read(4))
    dz = struct.unpack("f", fstream.read(4))

    x0 = struct.unpack("f", fstream.read(4))
    y0 = struct.unpack("f", fstream.read(4))
    z0 = struct.unpack("f", fstream.read(4))

    cvac = struct.unpack("f", fstream.read(4))
    eps0 = struct.unpack("f", fstream.read(4))

    zero = struct.unpack("f", fstream.read(4))

    (rank,) = struct.unpack("i", fstream.read(4))
    (nproc,) = struct.unpack("i", fstream.read(4))

    sp_id = struct.unpack("i", fstream.read(4))
    q_m = struct.unpack("f", fstream.read(4))

    return {'rank': rank, 'nproc': nproc, 'step': step}


def get_array_header(fstream):
    (so_p0,) = struct.unpack("i", fstream.read(4))
    (ndim,) = struct.unpack("i", fstream.read(4))

    dim_array = []

    for idx in range(ndim):
        (dim_elem,) = struct.unpack("i", fstream.read(4))
        dim_array.append(dim_elem)

    print(so_p0, ndim, dim_array)
    return {'psize': so_p0, 'nelem': dim_array[0]}


def parse(file_in, file_out):
    print("Parsing %s to %s..." % (file_in, file_out))

    f = open(file_in, "rb")
    g = open(file_out, "wb")

    header = get_header(f)
    print(header)

    array_header = get_array_header(f)
    print(array_header)

    # particle struct format:
    # dxdydz,i,uxuyuz,w,tag,tag
    for i in range(array_header['nelem']):
        particle = struct.unpack("fffiffffqq", f.read(48))
        px, py, pz = particle[4], particle[5], particle[6]
        energy = (1 + px * px + py * py + pz * pz) ** 0.5 - 1
        g.write(struct.pack("f", energy))

    f.close()
    g.close()
    return


def parse_wrap(x):
    parse(x[0], x[1])


def confirm():
    check = input("Proceed? y/N ")
    if check != 'y':
        sys.exit(0)


def run_job(par_dir, num_threads):
    all_paths_in = glob.glob(par_dir + "/**/eparticle*", recursive=True)
    print("Found {0} eparticle files".format(len(all_paths_in), ))

    confirm()

    all_paths_out = [s.replace("/particle", "/particle.compressed") for s in
                     all_paths_in]

    for path in all_paths_out:
        pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    #  print("Parsing %s..." % (file_in))
    path_pairs = zip(all_paths_in, all_paths_out)

    with Pool(num_threads) as p:
        p.map(parse_wrap, path_pairs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Compress particle structs in some path in parallel. 
        Path is usually $vpic_data/particle. Another directory 
        $vpic_data/particle.compressed will be created, with an identical 
        hierarchy, containing compressed versions of the pearticle files.""")

    parser.add_argument('dir_path', type=str,
                        help='path to a directory containing eparticle files')

    parser.add_argument('--num_threads', '-t', type=int, default=64)
    args = parser.parse_args()
    run_job(args.dir_path, args.num_threads)
