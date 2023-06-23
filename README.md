# noty

## Overview


## Install

### Clone the project
```
git clone [repo_url]
cd noty
```

### Rename .env file
```
mv .template_env .env
```

### Edit preferences
```
root_path = path to dir where noty is installed  
text_editor = favorite text editor such as gedit (keyword=gedit), sublime-text (keyword=subl)
```

### Install conda env and create aliases
- Method 1
```
bash install/install.sh 
```

This will create a conda env named 'noty'. Then commands aliases are edited in ~/.bashrc  

- Method 2
Create the env
```
conda env create -f install/env.yml
conda activate noty
```

Add the aliases in ~/.bashrc file such as :  
```
alias <alias_name>="conda run -n noty python /path/to/cloned_repository/main.py <alias_value>"
```

Aliases can be found in install/alias.yml such as:
```
<alias_name>: <alias_value>
```

## Usage
Aliases enable to launch commands from anywhere within a specific env

### Create a note and launch it
```
noty_create <subject>
```

### Delete a note
```
noty_delete <id>
```

### Launch a note
```
noty_launch <id>
```

### List all notes
```
noty_list
```

### Search for a keywork in notes
```
noty_search <pattern>
```
