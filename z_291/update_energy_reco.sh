SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo $SCRIPT_DIR

current_dir="${SCRIPT_DIR##*/}"
Z=${current_dir#z_}

echo $Z

sed -i "4s/.*/Z=${Z}/" "$SCRIPT_DIR/"energy_reco.sh


sed -i "1s|.*|executable = ${SCRIPT_DIR}/energy_reco.sh|" "$SCRIPT_DIR/"energy_reco.sub

