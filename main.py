import extract_mzxml as em
import numpy as np
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('data_file', help='data')
parser.add_argument('directory', help='directory for output files')
parser.add_argument('--pair_dict_file',
                    action='store')
parser.add_argument('--scan_dict_file',
                    action='store')

args = parser.parse_args()
file = args.data_file
directory = args.directory
pair_dict_file = args.pair_dict_file
scan_dict_file = args.scan_dict_file


start_time = time.time()

data = em.read_data(file)

if args.scan_dict_file:
    scan_dict = em.unpack(scan_dict_file)
    simple_dict = em.find_max_min(scan_dict)
    em.output_dict(simple_dict, directory, simple=True)

elif args.pair_dict_file:
    pair_dict = em.unpack(pair_dict_file)
    processed_list = em.get_pair_scans2(data, pair_dict)
    print(len(processed_list))
    print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
    print(processed_list)
    np.savetxt('scan_array.txt', processed_list, delimiter=',', fmt='%s')
    print('operations complete')

else:
    em.count_MS2(data)
    id_list_ms2 = em.find_MS2(data, directory)
    pair_dict = em.search_MS2_pairs(data, id_list_ms2)
    em.output_dict(pair_dict, directory, pair=True)
    print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
    #pair_dict = em.unpack(pair_dict_file)
    processed_dict = em.get_pair_scans(data, pair_dict)
    print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
    em.output_dict(processed_dict, directory, scans=True)
    simple_dict = em.find_max_min(processed_dict)
    em.output_dict(simple_dict, directory, simple=True)
    print('operations complete')