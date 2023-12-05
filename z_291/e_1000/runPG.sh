#!/bin/bash
ProcId=$2
LSB_JOBINDEX=$((ProcId+1))
NEVENTS=10
STARTEVENT=$((ProcId*NEVENTS))
echo $LSB_JOBINDEX

# Energy [GeV]
E=1000
Z=291
# PDG code pion
PART=211

sleep $ProcId

# Setup the environment for Fairship
echo "--Setup"
RUN_PATH=/eos/user/s/skatsaro/sndsw/shipLHC
SNDBUILD_DIR=/eos/user/s/skatsaro/sw/

source /cvmfs/sndlhc.cern.ch/SNDLHC-2023/Jan22/setUp.sh
eval `alienv load -w $SNDBUILD_DIR --no-refresh sndsw/latest`
export EOSSHIP=root://eosuser.cern.ch/

echo "STARTING PG with pions, $E GeV"
echo "Starting event number: $STARTEVENT"

outdir=/eos/user/s/skatsaro/PGsim/depth_$Z/pions_$E/Ntuples/
mkdir -p $outdir$LSB_JOBINDEX
echo "python $RUN_PATH/run_simSND.py --PG --pID $PART --Estart $E --Eend $E --EVx -28 --EVy 35.5 --EVz $Z -n $NEVENTS -o $outdir$LSB_JOBINDEX"

# Run the Particle Gun simulation
python $RUN_PATH/run_simSND.py --PG --pID $PART --Estart $E --Eend $E --EVx -28 --EVy 35.5 --EVz $Z -n $NEVENTS -o $outdir$LSB_JOBINDEX

DIRECTORY=$outdir$LSB_JOBINDEX
cd $DIRECTORY
echo "STARTING digitisation for the directory $DIRECTORY"
python $RUN_PATH/run_digiSND.py -g $DIRECTORY/geofile_full.PG_$PART-TGeant4.root -f $DIRECTORY/sndLHC.PG_$PART-TGeant4.root -cpp -n $NEVENTS

echo "--End"
