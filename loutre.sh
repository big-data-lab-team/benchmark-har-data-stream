#!/bin/bash
echo Initializing the process...

export VFC_BACKENDS="libinterflop_vprec.so --precision-binary64=50"
#bin/mondrian_t10 <file1> <seed> <model id> <run id> <parameter classifier ...>
make run
