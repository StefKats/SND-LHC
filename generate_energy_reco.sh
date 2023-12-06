echo "recoEnergy: (y/n)"
read userInput

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo $SCRIPT_DIR

for dir in z_*/; do rsync -v -aP ~/SND-LHC/z_291/. $dir;done # copy the first energy dir

for dir in z_*/; do cp -v ~/SND-LHC/z_291/generate_PDF.sh $dir;done # copy file to mulitple folders

for dir in z_*/; do cp -v ~/SND-LHC/z_291/energy_reco.sh $dir;done # copy file to mulitple folders

for dir in z_*/; do cp -v ~/SND-LHC/z_291/energy_reco.sub $dir;done # copy file to mulitple folders

for dir in z_*/; do cp -v ~/SND-LHC/z_291/update_energy_reco.sh $dir;done # copy file to mulitple folders

for dir in z_*/; do bash "$dir"update_energy_reco.sh;done # run update script for all files

for dir in z_*/; do (cd $dir && bash generate_PDF.sh);done # run update script for all files

for dir in z_*/; do (cd $dir && mkdir error log output);done # make empty error log and output dirs

#(cd /tmp && pwd)

if [ "$userInput" == "y" ];
then 

	for dir in z_*/; do condor_submit "$dir"energy_reco.sub ;done # submit multiple config sets of jobs
fi
