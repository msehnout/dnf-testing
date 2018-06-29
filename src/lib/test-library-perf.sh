#!/bin/bash
# Run the test 100 times
for i in $(seq 0 100);
do
    echo "Running round - ${i}"
    # Run the Python script, store the time
    python3 test-library.py | grep time | awk '{print $3}' >> resolver-perf-test-result
    sleep 5
done
