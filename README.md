# gttp
## Galaxy test tools pipeline

gttp is a pipeline to automatically test Galaxy tools and generate html reports about the success or fail of a test.

## Requirements
Although this can be used as a standalone script, gttp was designed to run from a docker container. Hence all requirements are be taken care for you.

In case you want to run as a standalone, make sure you are running python >=3.8 .

To install the python dependencies run 

```
pip install -r requirements.txt
```


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

## Standalone pipeline

#### ***IMPORTANT***
Before running the pipeline you must go to your Galaxy instance and create an API_KEY. 
```
(User -> Preferences -> Manage API key -> Create a key)

```

This key must be exported as an enviromental variable.

You can do it in your session by 

```
export API_KEY=<your-key>
```

or by adding the above line to your .bashrc

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

# GTTP splits the yml file into chunks of 50 tools per yml (this prevents the tool from hanging due to proxy/network problems)
# You can modify this by passing -l with a multiple of 4 
python gttp.py -l 400 

# Cleaning previous runs
python gttp.py -c 

```
#### ***All options can be combined (except -c which deletes all output dirs)***


## Using with Docker

It is advisable to run the test case before running the whole pipeline.

***Before running, export the API_KEY and GURL env. vars as explained above***

To Run the test simply run

```
docker pull docker.io/dmorais/gttp:<version>

docker run -it --name gttp-test -e API_KEY -e GURL gttp:<version>
```

### NOTE

***-e API_KEY and -e GURL passes those env. variable to the container.***


Run the pipeline, fetch all tools and save the results inside the container

```
docker container run -it --name gttp-test -e API_KEY -e GURL  gttp:<version> python app/gttp.py 

```

To run the pipeline from a yml file (list of tools) inside the host machine and save the results inside the host machine.

```
# Fisrt create a input dir (where the yml file will be). Put the yml with a list of tools there.
# Then create the output dir

docker container run -it --name gttp-test -e API_KEY -e GURL --mount src=/path-to-input-dir,dst=/home/gttp/input,type=bind  --mount src=/path-to-output-dir,dst=/home/gttp/output,type=bind gttp:<version> python app/gttp.py -y /home/gttp/input/test.galaxy.yml -o /home/gttp/output

### IN CASE YOUR DOCKER DOES NOT SUPPORT THE --mount OPTION ###
docker container run -it --name gttp-test -e API_KEY -e GURL -v /path-to-input-dir:/home/gttp/input  -v /path-to-output-dir:/home/gttp/output docker.io/dmorais/gttp:v2 python app/gttp.py -y /home/gttp/input/test.galaxy.yml -o /home/gttp/output

```

Clear output from previous run

```
docker container run -it --name gttp-test -e API_KEY -e GURL  gttp:<version> python app/gttp.py  -o <ouput-dir>

```

# Interacting with pipeline from within the container

```
# Start in dectached mode and pass /bin/bash as an argument

docker container run -dit --name gttp-test -e API_KEY -e GURL  docker.io/dmorais/gttp:v2  /bin/bash

# Get the container id
docker container attach <container_id>

# At this point the pipeline will not be running. You must run 
python app/gttp.py ARGS            

```

# Interacting after the container has stopped

```
# Get container name
docker container ls -a

# Start the container
docker container start <container-name>

# Exec in detached mode
docker exec -dit <container-name>  /bin/bash

# Attach the container
docker container attach  <container-name>


```