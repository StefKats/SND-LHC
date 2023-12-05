SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo $SCRIPT_DIR

current_dir="${SCRIPT_DIR##*/}"
E=${current_dir#e_}

echo $E

#filepath=$PWD
path=${SCRIPT_DIR%/*}
parent_dir=${path##*/}
Z=${parent_dir#z_}

echo $Z


#DIR_STRING="${SCRIPT_DIR}"

sed -i "4s/.*/E=${E}/" "$SCRIPT_DIR/"pythonPDF.sh


sed -i "5s/.*/Z=${Z}/" "$SCRIPT_DIR/"pythonPDF.sh


sed -i "1s|.*|executable = ${SCRIPT_DIR}/pythonPDF.sh|" "$SCRIPT_DIR/"pythonPDF.sub
