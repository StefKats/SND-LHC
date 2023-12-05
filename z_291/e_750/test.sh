current_dir="${PWD##*/}"
E=${current_dir#e_}

echo $E

filepath=$PWD
path=${filepath%/*}
parent_dir=${path##*/}
Z=${parent_dir#z_}

echo $Z

for i in {1..100}
do
    if [[ `ls  /eos/user/s/skatsaro/PGsim/depth_330/pions_100/Ntuples/$i 2> /dev/null | wc -l` == "0" ]];
        then
        echo $i
    fi
done

