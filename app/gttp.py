import argparse
import os
import sys
import subprocess
import glob
from time import sleep
from tqdm import tqdm
import multiprocessing

API_KEY = os.environ.get('API_KEY')
GURL = os.environ.get('GURL')            # galaxy-url

def create_dirs():
    
    split_tool_dir  = os.path.join(os.getcwd(), "yml-file-tools")
    if os.path.isdir(split_tool_dir):
        print(split_tool_dir, "already exists")
    else:
        os.mkdir(split_tool_dir)

    
    json_report_dir  = os.path.join(os.getcwd(), "json-files-report")
    if os.path.isdir(json_report_dir):
        print(json_report_dir, "already exists")
    else:
        os.mkdir(json_report_dir)


    html_report_dir  = os.path.join(os.getcwd(), "html-files-report")
    if os.path.isdir(html_report_dir):
        print(html_report_dir, "already exists")
    else:
        os.mkdir(html_report_dir)

    return (split_tool_dir, json_report_dir, html_report_dir)

def get_tool_list():

    yml_file = 'test.galaxy.yml'
    process = subprocess.run(['get-tool-list',
                          '-g', GURL, 
                          '-o' , yml_file,
                          '--skip_changeset_revision'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True)

    if not process.returncode == 0:
        print(process.stderr,"\n",process.stdout)
    
    return yml_file


def split_yml(split_tool_dir,yml_file, lines):

    chunk = 1
    file_chunk = open(os.path.join(split_tool_dir,"galaxy-tool-chunk" + str(chunk) + ".yml"), 'w')

    f = open(yml_file)

    for i, line in enumerate(f):
        if line == "tools:\n":
            file_chunk.write(line)
            continue
        if i  % lines == 0:
            file_chunk.write(line)
            file_chunk.close()

            chunk += 1
            file_chunk = open(os.path.join(split_tool_dir,"galaxy-tool-chunk" + str(chunk) + ".yml"), 'w')
            file_chunk.write("tools:\n")

        else:
            file_chunk.write(line)
    file_chunk.close()    



def parallel_tool_test(file,json_report_dir,html_report_dir):
    print("\n##### Runnig tools in chuck ", os.path.basename(file), "\n\n")
  
    json = os.path.splitext(os.path.basename(file))[0] + ".json"
    process = subprocess.run(['shed-tools','test',
                            '-a', API_KEY, 
                            '-g' , GURL,
                            '--parallel_tests', '10',
                            '-t', file,
                            '--test_json', os.path.join(json_report_dir,json)],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)

    if not process.returncode == 0:
        print(process.stderr,"\n",process.stdout)

    print("Done Processing", json)
    print("Converting report to html")
    convert_to_html(html_report_dir, json_report_dir,json)


def convert_to_html(html_report_dir, json_report_dir, json=None):
    
    if json is not None:
        html_report = os.path.join(html_report_dir, os.path.splitext(os.path.basename(json))[0] + ".html")

        process = subprocess.run(['planemo',
                                'test_reports', os.path.join(json_report_dir,json), 
                                '--test_output' , html_report],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)

    if not process.returncode == 0:
        print(process.stderr,"\n",process.stdout)

    # Batch Mode convert the all files at once    
    else:
        json_reports = glob.glob(os.path.join(json_report_dir, "*.json"))

        for json in json_reports:
            html_report = os.path.join(html_report_dir, os.path.splitext(os.path.basename(json))[0] + ".html")

            process = subprocess.run(['planemo',
                                'test_reports', json, 
                                '--test_output' , html_report],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)

            if not process.returncode == 0:
                print(process.stderr,"\n",process.stdout)
    return 0


def main():
    
    parser = argparse.ArgumentParser(
        description="A pipeline to automate tools testing and reporting on Galaxy")

    parser.add_argument('-y', '--yml_file', action='store',
                            help='A yml file with a list of tools to be tested. If not provided the script will fecth all tools.',
                            required=False)
    
    parser.add_argument('-s', '--sleep', action='store', type=int,
                         help=' Interval between submission of tool files to be tested. Default=20 min. This is enough to test about 40 tools at time.',
                         default=10,
                         required=False)
    
    parser.add_argument('-l', '--lines', type=int,
                        help=' Set it to a multiple of 4. This values is used to split the yml tool list into chunks. The defaul is 200 which put 50 tools on each yml file.',
                        default=4,
                        required=False)

    args = parser.parse_args()

    # Create dirs
    split_tool_dir, json_report_dir, html_report_dir = create_dirs()

    yml_file = args.yml_file if args.yml_file is not None else get_tool_list()

    # Split yml
    split_yml(split_tool_dir,yml_file, args.lines)
     
    # Test Tools
    list_of_yml = glob.glob(os.path.join(split_tool_dir, "*.yml"))   

    # Parallel Processing of files
    processes = list()
    for yml in list_of_yml[1:]:
        processes.append( multiprocessing.Process(target=parallel_tool_test, args=(yml,json_report_dir,html_report_dir)))

    for process in tqdm(processes):
        process.start()
        sleep(args.sleep)
    
    #convert_to_html(html_report_dir, json_report_dir)



if __name__ == '__main__':

    if API_KEY==None or GURL==None:
        print("### Set env variables\n\nAPI_KEY -- for you Galaxy API KEY\nGURL -- for galaxu URL\n\n")
        sys.exit(1)

    main()