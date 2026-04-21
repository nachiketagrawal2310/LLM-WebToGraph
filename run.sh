#!/bin/bash
trap "kill 0" EXIT

source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

while true; do
    python src/app/main.py &
    BPID=$!
    streamlit run src/UI/ui.py &
    FPID=$!

    while true; do
        read -n 1 -s key
        if [[ $key == "q" ]]; then
            exit 0
        elif [[ $key == "r" ]]; then
            kill $BPID $FPID
            break
        fi
    done
done
