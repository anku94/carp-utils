smallCARP
---------

512 ranks, 1.6M/rank, Magnetic Reconnection ("expert crafted" to produce a magnetic island)

- reconnection.cc - original, unmodified
- reconnection512.cc - modified to dump suitably

bigCARP
-------

512 ranks, 8M/rank, Magnetic Reconnection ("amateurly modified" from smallCARP for desired scale)

- reconnection.cc - original, unmodified
- reconnection512.cc - modified to dump suitably

gen_compressed_traces.py
------------------------

This is a multithreaded parser that compresses all the eparticle files generated from a VPIC run into logs of energy values.

Given a `$vpic_run/particle` path, it will generate a `$vpic_run/particle.compressed` path with an identical directory hierarchy, except the compressed `eparticle` files will contain an aggregated property, which is currently computed using the formula `sqrt(1 + ux^2 + uy^2 + uz^2) - 1`

After a VPIC run has completed, point this script to generated `particle` directory.

Currently, this only handles the `eparticle` files and ignores the `hparticle` files. You can tweak the code to parse both.

Running a deck
--------------

- Compile `vpic407` to get a VPIC executable.
- Run `build/vpic reconnection512.cc` to get an executable (usually called `reconnection.Linux`)
- `mpirun -h hostfile -n 512 reconnection.Linux`
- This will start the simulation. All data will be dumped in the directory containing the executable. (I usually just put the executabe in PanFS and run things there)
- Periodic dumps are collected in `particle/T.ts`
