#!/bin/bash

# env name
env_name=noty


echo "Create environment"

# create and activate env
conda env create -f install/env.yml
source activate $env_name



echo "Install aliases"

# path aliases file
path_root=$(pwd)
path_alias=$path_root/install/alias.yml
path_script=$path_root/main.py

# get aliases as str(dict()) from yml file
aliases=$(python -c "from noty.utils import load_yml; load_yml(\"$path_alias\", shell=True)" 2>&1)

# remove the curly braces and single quotes from the string
aliases=${aliases#*\{}
aliases=${aliases%\}*}
aliases=${aliases//\'/}

# split the string into an array of key-value pairs
IFS=',' read -ra kv_pairs <<< "$aliases"

# iterate over the key-value pairs
for kv_pair in "${kv_pairs[@]}"; do
    IFS=':' read -r key value <<< "$kv_pair"

    # alias to exec cmd from noty env
    echo -e "alias $key=\"conda run -n $env_name python $path_script $value\"" >> ~/.bashrc 
done

# deactivate env
conda deactivate