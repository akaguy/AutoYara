import os
import subprocess
import argparse
from etpstorage._azure.azure_storage import AzureStorage
import uuid


CONN_STR = os.environ['CONN_STR']
CONTAINER = os.environ['CONTAINER']
base_remote_path = 'models'



def run_command(cmd):
    sshProcess = subprocess.Popen([cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = sshProcess.communicate()

def get_file(file_path,dst,azure_object):
    bin_data = azure_object.read_file(file_path)
    filename = os.path.basename(file_path)
    dst = os.path.join(dst,filename)
    with open(dst,'wb') as f:
        f.write(bin_data)

def main(id_str,benign_file,fp_rate,azure_object):
    new_folder = os.path.join(base_remote_path,args.id_str)
    run_command(f"mkdir -p {new_folder}")
    send_file(benign_file,new_folder,azure_object)
    bloom_folder = os.path.join(new_folder,'bloom')
    remote_file = os.path.join(new_folder,os.path.basename(benign_file))
    run_command(f"mkdir {bloom_folder}")
    run_command(f'./run_bloom.sh {remote_file} {bloom_folder} {fp_rate}'))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--id-str", help="Id for saving the results",
                        type=str, required=True)
    parser.add_argument("-b", "--benign-file", help="Id for saving the results",
    type=str, required=True)
    parser.add_argument("-fp", "--fp-rate", help="Max FP rate",
    type=float, required=True)
    parser.add_argument("-cs", "--conn_str", help="Connection string of Storage",
    type=str, default='')
    parser.add_argument("-c", "--container", help="container of Storage",
    type=str, default='')

    args = parser.parse_args()
    if args.conn_str == '':
        azure_object = AzureStorage(CONN_STR, CONTAINER)
    else:
        azure_object = AzureStorage(args.conn_str,args.container)
    main(args.id_str,args.benign_file,args.fp_rate,azure_object)
    


    