#echo "Submit to condor? (y/n)"


#read userInput


read -p 'runPG: (y/n) ' user1
read -p 'createPDFs: (y/n) ' user2

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo $SCRIPT_DIR

current_dir="${SCRIPT_DIR##*/}"
Z=${current_dir#z_}

echo $Z

#mkdir -p e_50 e_100 e_200 e_300 e_400 e_500 e_750 e_1000 e_1250 e_1500 e_2000

for dir in e_*/; do (cd $dir && mkdir error log output);done # make empty error log and output dirs

# for dir in e_*/; do cp -v -r ~/SND-LHC/z_$Z/e_50/error $dir;done # copy file to mulitple folders

# for dir in e_*/; do cp -v -r ~/SND-LHC/z_$Z/e_50/log $dir;done # copy file to mulitple folders

# for dir in e_*/; do cp -v -r ~/SND-LHC/z_$Z/e_50/output $dir;done # copy file to mulitple folders

for dir in e_*/; do cp -v ~/SND-LHC/z_$Z/e_50/runPG.sh $dir;done # copy file to mulitple folders

for dir in e_*/; do cp -v ~/SND-LHC/z_$Z/e_50/runPG.sub $dir;done # copy file to mulitple folders

for dir in e_*/; do cp -v ~/SND-LHC/z_$Z/e_50/pythonPDF.sh $dir;done # copy file to mulitple folders

for dir in e_*/; do cp -v ~/SND-LHC/z_$Z/e_50/pythonPDF.sub $dir;done # copy file to mulitple folders

for dir in e_*/; do cp -v ~/SND-LHC/z_$Z/e_50/update_params.sh $dir;done # copy file to mulitple folders

for dir in e_*/; do bash "$dir"update_params.sh ;done # run update script for all files

if [ "$user1" == "y" ];
then

        for dir in e_*/; do (cd $dir && condor_submit runPG.sub) ;done # submit multiple config sets of jobs
fi


if [ "$user2" == "y" ];
then

        for dir in e_*/; do condor_submit "$dir"pythonPDF.sub ;done # submit multiple config sets of jobs
fi

