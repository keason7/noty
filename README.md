# :green_book: noty

## Overview

Simple CLI note taker and note management

## :wrench: Install

### Clone the project

```bash
git clone [repo_url]
cd noty
```

### Rename .env file

```bash
mv .template_env .env
```

### Edit preferences

```bash
root_path = path to dir where noty is installed
text_editor = favorite text editor such as gedit (keyword=gedit), sublime-text (keyword=subl)
```

### Install conda env and create aliases

- Method 1

```bash
bash install/install.sh
```

This will create a conda env named 'noty'. Then commands aliases are edited in ~/.bashrc

- Method 2

Create the env

```bash
conda env create -f install/environment.yml
conda activate noty
```

Add the aliases in ~/.bashrc file such as :

```bash
alias <alias_name>="conda run -n noty python /path/to/cloned_repository/main.py <alias_value>"
```

Aliases can be found in install/alias.yml such as:

```bash
<alias_name>: <alias_value>
```

## :rocket: Usage

Aliases enable to launch commands from anywhere within a specific env

### Create a note and launch it

```bash
ncreate <subject>
```

### Delete a note

```bash
ndelete <id>
```

### Launch a note

```bash
nlaunch <id>
```

### List all notes

```bash
nlist
```

### Search for a keywork in notes

```bash
nsearch <pattern>
```
