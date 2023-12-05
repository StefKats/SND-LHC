SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo $SCRIPT_DIR

current_dir="${SCRIPT_DIR##*/}"
Z=${current_dir#z_}

echo $Z


for dir in e_*/; do cp -v ~/PGsim/z_$Z/e_50/pythonPDF.sh $dir;done # copy file to mulitple folders

for dir in e_*/; do cp -v ~/PGsim/z_$Z/e_50/pythonPDF.sub $dir;done # copy file to mulitple folders

for dir in e_*/; do cp -v ~/PGsim/z_$Z/e_50/update_params.sh $dir;done # copy file to mulitple folders

for dir in e_*/; do bash "$dir"update_params.sh ;done # run update script for all files

for dir in e_*/; do condor_submit "$dir"pythonPDF.sub ;done # submit multiple config sets of jobs

