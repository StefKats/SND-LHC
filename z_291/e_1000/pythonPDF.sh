#!/bin/bash


E=1000
Z=291

#sleep $ProcId

# Setup the environment for Fairship
echo "--Setup"
RUN_PATH=/eos/user/s/skatsaro/sndsw/shipLHC
SNDBUILD_DIR=/eos/user/s/skatsaro/sw/

source /cvmfs/sndlhc.cern.ch/SNDLHC-2023/Jan22/setUp.sh
eval `alienv load -w $SNDBUILD_DIR --no-refresh sndsw/latest`
export EOSSHIP=root://eosuser.cern.ch/

outdir=/eos/user/s/skatsaro/PGsim/depth_$Z/pions_$E/PDF/
mkdir -p $outdir
mkdir -p $outdir/events/

# Run the PDF script
python $RUN_PATH/PDF_python_code.py --Z $Z --E $E --N 100 -o $outdir

echo "--End"
