# gttp
## Galaxy test tools pipeline

gttp is a pipeline to automatically test Galaxy tools and generate html reports about the success or fail of a tool.

## Requirements
Although this can be used as a standalone script, gttp was designed to run from a docker container. Hence all requirements should be taken for you.
In case you want to run as a standalone, make sure you are running python 3.8 or higher.
To install the python dependencies run 

```
pip install -r requirements.txt
```

## Standalone pipeline

### Help
```
python gttp.py -h

usage: gttp.py [-h] [-y YML_FILE] [-s SLEEP] [-l LINES] [-c] [-o OUT_DIR]

A pipeline to automate tools testing and reporting on Galaxy

optional arguments:
  -h, --help            show this help message and exit
  -y YML_FILE, --yml_file YML_FILE
                        A yml file with a list of tools to be tested. If not provided the script will fecth all tools from
                        Galaxy.
  -s SLEEP, --sleep SLEEP
                        Interval between submission of tool files to be tested. Default=20 min. This is enough to test about
                        40 tools at time.
  -l LINES, --lines LINES
                        Set it to a multiple of 4. This values is used to split the yml tool list into chunks. The defaul is
                        200 which put 50 tools on each yml file.
  -c, --clear           Clear output and dirs of previous runs. It will delete yml, json and html dirs in the current
                        directory if they exist. Default False.
  -o OUT_DIR, --out_dir OUT_DIR
                        Dir where all outputs will be written to. Default current dir

```
#### *** IMPORTANT ****
Before running the pipeline you must go to your Galaxy instance and create an API_KEY.

This key must be exported as an enviromental variable.
You can do it in your session by 

```
export API_KEY=<you-key>
```

or by adding this line to your .bashrc

You also must export the Galaxy url as an env. variable

```
export GURL=<galaxy-url>
```

Both vars must be written as API_KEY and GURL

### Examples of usage
```


# Get a list of all Galaxy tools and test them all

python gttp.py 

# Test all tools contained in a list of tools
python gttp.py -y <list-of-tools.yml>

# By default the program output to cwd, to modify this behavior
python gttp.py -o <path-to-output-dir>

# GTTP splits the yml file into chunks of 50 tools per yml (this prevents the tool to hang due to proxy problems)
# You can modify this by passing -l with a multiple of 4 
python gttp.py -l 400 

# Cleaning previous runs

python gttp.py -c 

```
#### ***All options can be combined (except -c which deletes all output dirs)***


## Using with Docker

It is advisable to run the test case before running the whole pipeline.

```

```
