import os
import subprocess
import argparse
import etpstorage
from etpstorage._azure.azure_storage import AzureStorage
import uuid

base_remote_path = 'models'
autoyara_jar = 'target/AutoYara-1.0-SNAPSHOT.jar'
CONN_STR = os.environ['CONN_STR']
CONTAINER = os.environ['CONTAINER']



def run_command(cmd):
    sshProcess = subprocess.Popen([cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = sshProcess.communicate()
    print(out)
    print(err)

def get_file(file_path,dst,azure_object):
    bin_data = azure_object.read_file(file_path)
    filename = os.path.basename(file_path)
    dst = os.path.join(dst,filename)
    with open(dst,'wb') as f:
        f.write(bin_data)


def send_file(remote_path,dst,azure_object):
    with open(tmp_file,'rb') as f:
        bin_data = f.read()
        azure_object.write_file(dst,bin_data,overwrite=True)
    os.remove(tmp_file)



def main(id_str,benign_file,malicious_file,fp_rate,output,azure_object):
    new_folder = os.path.join(base_remote_path,args.id_str)
    get_file(benign_file,new_folder,azure_object)
    get_file(malicious_file,new_folder,azure_object)
    
    bloom_folder = os.path.join(new_folder,'bloom')
    remote_benign_file = os.path.join(new_folder,os.path.basename(benign_file))
    remote_malicious_file = os.path.join(new_folder,os.path.basename(malicious_file))
    yara_filename = 'malicious_js.yara'
    json_filename = 'malicious_js.json'
    results_rule = os.path.join(new_folder,yara_filename)
    json_path = os.path.join(new_folder,json_filename)

    java_cmd = f'java -Xmx14G -jar {autoyara_jar} -b {bloom_folder} -m {bloom_folder} --fp-dirs {remote_benign_file} --input-dir {remote_malicious_file} -o {results_rule} -j {json_path} -pl'

    run_command(java_cmd)

    send_file(results_rule,os.path.join(output,yara_filename),azure_object)
    send_file(json_path,os.path.join(output,json_filename),azure_object)
    



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--id-str", help="Id for saving the results",
                        type=str, required=True)
    parser.add_argument("-b", "--benign-file", help="File contains paths to malicious js",
    type=str, required=True)
    parser.add_argument("-m", "--malicious-file", help="File contains paths to malicious js",
    type=str, required=True)
    parser.add_argument("-o", "--output", help="Output yara rule",
    type=str, default='')
    parser.add_argument("-cs", "--conn_str", help="Connection string of Storage",
    type=str, default='')
    parser.add_argument("-c", "--container", help="container of Storage",
    type=str, default='')
    parser.add_argument("-fp", "--fp-rate", help="Max FP rate",
    type=float, required=True)
    args = parser.parse_args()
    if args.conn_str == '':
        azure_object = AzureStorage(CONN_STR, CONTAINER)
    else:
        azure_object = AzureStorage(args.conn_str,args.container)
    main(args.id_str,args.benign_file,args.malicious_file,args.fp_rate,args.output,azure_object)
    


    