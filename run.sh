#!/bin/bash
trap "kill 0" EXIT

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

export PYTHONPATH=$PYTHONPATH:$(pwd)/src

echo "Starting LLM-WebToGraph..."
echo "Press 'q' to quit, 'r' to restart both servers."

while true; do
    # Start Backend
    python3 src/app/main.py &
    BPID=$!
    
    # Start Svelte Frontend
    cd src/frontend && npm run dev &
    FPID=$!
    cd ..

    while true; do
        read -n 1 -s key
        if [[ $key == "q" ]]; then
            echo "Quitting..."
            kill $BPID $FPID
            exit 0
        elif [[ $key == "r" ]]; then
            echo "Restarting..."
            kill $BPID $FPID
            break
        fi
    done
done
