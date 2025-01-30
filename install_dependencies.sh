#!/bin/bash
if [ -f "requirements.txt" ]; then
    python -m pip install -r requirements.txt
else
    echo "requirements.txt not found"
fi