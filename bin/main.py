import extract_mzxml as em
import numpy as np
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('data_file', help='data')
parser.add_argument('directory', help='directory for output files')
parser.add_argument('--match_index_file', action='store')
parser.add_argument('--processed_dict_file', action='store')
parser.add_argument('--binned_dict_file', action='store')
parser.add_argument('--pairs_list_file', action='store')
parser.add_argument('--ordered_list_file', action='store')

args = parser.parse_args()
file = args.data_file
directory = args.directory
match_index_file = args.match_index_file
processed_dict_file = args.processed_dict_file
binned_dict_file = args.binned_dict_file
pairs_list_file = args.pairs_list_file
ordered_list_file = args.ordered_list_file

start_time = time.time()

data = em.read_data(file) #reads in as a pyteomics object

if args.ordered_list_file: #test the convert_to_ready2() function
    ordered_list = em.unpack(ordered_list_file)
    ready_array = em.convert_to_ready(ordered_list)
    em.output_list(ready_array, directory, two=True)

elif args.pairs_list_file: #test the arrange_min_max() function
    pairs_list = em.unpack(pairs_list_file)
    ordered_list = em.arrange_min_max(pairs_list)
    em.output_file2(ordered_list, directory, ordered=True)

elif args.binned_dict_file: #tests the create_pairs() function
    binned_dict = em.unpack(binned_dict_file)
    pairs_list = em.create_pairs(binned_dict)
    em.output_file2(pairs_list, directory, pairs=True)

elif args.processed_dict_file: #tests the bin_array2() function
    processed_dict = em.unpack(processed_dict_file)
    binned_dict = em.bin_array2(processed_dict)
    em.output_file2(binned_dict, directory, binned=True)

elif args.match_index_file: #tests the get_match_scans() function
    match_index_dict = em.unpack(match_index_file)
    processed_dict = em.get_match_scans(data, match_index_dict)
    print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
    em.output_file(processed_dict, directory, processed=True)


###NEEDS TO BE CHECKED FOR ACCURACY
else: #complete run through
    em.count_MS2(data) #this lines doesn't matter        
    id_list_ms2 = em.find_MS2(data, directory) #made some adjustments, works as intended 
    
    match_index_dict = em.search_MS2_matches(data, id_list_ms2, rt_tol=0.10) #matches high and low spectra within the file
    print('--- %s seconds runtime ---' %(str(time.time() - start_time)))
    current_time = time.time() 
    
    processed_dict = em.get_match_scans(data, match_index_dict) 
    print('--- %s seconds runtime ---' %(str(time.time() - current_time)))
    current_time = time.time()
        
    #binned_dict = em.bin_array(processed_dict)
    binned_dict = em.bin_array2(processed_dict) #SO THIS IS THE POINT AT WHICH THINGS BECOME SPARSE
    print('--- %s seconds runtime ---' %(str(time.time() - current_time)))
    current_time = time.time() 
       
    pairs_list = em.create_pairs(binned_dict)
    print('--- %s seconds runtime ---' %(str(time.time() - current_time)))
    current_time = time.time()
    
    ordered_list = em.arrange_min_max(pairs_list)
    print('--- %s seconds runtime ---' %(str(time.time() - current_time)))
    current_time = time.time()
   
    ready_array, ready_mass = em.convert_to_ready(ordered_list)
    print('--- %s seconds runtime ---' %(str(time.time() - current_time)))
    current_time = time.time()
    em.output_list(ready_array, directory)
    
    print("Before New Code")
    #ready_array = em.convert_to_ready(ordered_list)
    #ready_array = em.convert_to_ready2(ordered_list)
    ready_array = em.convert_to_ready2(ordered_list)
    print(type(ready_array))
    print('--- %s seconds runtime ---' %(str(time.time() - current_time)))
    current_time = time.time()
    em.output_list(ready_array, directory, two=True, ready_mass=None)

print('operations complete')
