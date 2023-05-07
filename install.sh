#!/bin/bash 

python3 -m venv .venv 

source .venv/bin/activate

pip install -r requirements.txt 

pip install -U \
  -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04 \
  wxPython

