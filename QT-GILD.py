import os
import sys
import subprocess
import shutil
from shutil import copyfile
from subprocess import Popen, PIPE
from random import seed
from random import randint
from time import time
import subprocess
import argparse

from lib.imputer import modified_numpy_formation
from lib.imputer import impute
from lib.Quartet_Numpy_Generation import generate_numpy
from lib.distribution_maker import qdist
# data_directory="11-taxon/100_genes/"

# base_directory=os.getcwd()
base_directory = ""
Numpy_Folder = ""
Whole_GT_Numpy = ""
Whole_GT_Numpy_Taxa_Map_and_Quartets = ""
Taxa_num = 0

def numpy_generator_whole_GT():
	in_directory=base_directory+"/Incomplete_GT"
	for filename in os.listdir(in_directory):
		input_file = in_directory + "/" + filename
		file_sep= filename.split('_')

		idx = file_sep[0]
		
		print("============= Starting file -> " + filename + "===================")
		numpy_outfile_whole = Whole_GT_Numpy + "/" + idx + "_whole_arr"
		#if((idx == "04")):
		in_time = time()
		global Taxa_num
		Taxa_num = generate_numpy(input_file,Whole_GT_Numpy_Taxa_Map_and_Quartets,numpy_outfile_whole,idx)
		print("Total Taxa", Taxa_num)
		print("Time Required -> ", time()-in_time)
		print("=============== done with file -> " + filename + "================")



def working_folder_creation(gt_path,temp_dir,mode):
	
	global base_directory

	base_directory = temp_dir
	if not os.path.exists(base_directory):
		os.mkdir(base_directory)

	subprocess.call(['python','lib/make_folders.py',str(mode),base_directory])
	final_gt = base_directory +"/Incomplete_GT"
	shutil.copy2(gt_path,final_gt)
	
	global Numpy_Folder
	global Whole_GT_Numpy
	global Whole_GT_Numpy_Taxa_Map_and_Quartets
	Numpy_Folder = base_directory +"/"+ 'GT_Numpy'
	Whole_GT_Numpy = Numpy_Folder + "/" + "Whole_GT_Numpy"
	Whole_GT_Numpy_Taxa_Map_and_Quartets = Whole_GT_Numpy +"/" + "Taxa_Map_Quartets"
	if not os.path.exists(Numpy_Folder):
		os.mkdir(Numpy_Folder)

	if not os.path.exists(Whole_GT_Numpy):
		os.mkdir(Whole_GT_Numpy)

	if not os.path.exists(Whole_GT_Numpy_Taxa_Map_and_Quartets):
		os.mkdir(Whole_GT_Numpy_Taxa_Map_and_Quartets)

def parseArguments():

    parser = argparse.ArgumentParser(prog='QT-GILD.py', description='QT-GILD: Quartet Based Gene Tree Imputation Using DeepLearning Improves Phylogenomic Analyses Despite Missing Data')
    required = parser.add_argument_group('Required Arguments')
    required.add_argument(
    	'-i',
    	'--input',
    	help="Input gene trees path",
    	dest="gt_path",
    	metavar="Input gene trees")

    required.add_argument("-o", "--output",
        dest="output", metavar="Output",
        default="output",
        type=str,
        help="output quartets with prefix OUTPUT. [default: %(default)s]")

    required.add_argument("-t", "--tempDir",
        dest="temp_dir", metavar="temporary directory",
        default="temp",
        type=str,
        help="temporary directory for the intermediate files [default: %(default)s]")
    

    optional_for_st = parser.add_argument_group('Optional Arguments For Species Tree Generation')
    optional_for_st.add_argument('--st',
		help="Create WQFM Species Trees",
		action='store_true',
		dest='mode')
		  

    args = parser.parse_args()
    args.mode = 0 if args.mode == False else 1


    return args

def copy_four_taxa_identifiers(temp_dir):
	
	base_directory = temp_dir +"/GT_Numpy"
	Four_Taxa_Dir = "Four_Taxa_Map"
	_dir_  = base_directory + "/" + Four_Taxa_Dir
	if not os.path.exists(_dir_ ):
		os.mkdir(_dir_)
	Whole_Taxa_Map = base_directory + "/Whole_GT_Numpy/Taxa_Map_Quartets"
	files = os.listdir(Whole_Taxa_Map)
	for file in files:
		if file.startswith("Four"):
			out_dir=base_directory + "/"+Four_Taxa_Dir
			print(file)
			shutil.copy2(os.path.join(Whole_Taxa_Map,file),os.path.join(out_dir,file))

def copy_results_to_output(output_direc,base_direc):
	if not os.path.exists(output_direc):
		os.mkdir(output_direc)
	wqmc_style = base_direc +"/GT_Numpy/Imputed_GT_Numpy/Imputed_Quartets_wqmc_format"
	newick_style = base_direc +"/GT_Numpy/Imputed_GT_Numpy/Quartets_Newick_format"

	out_wqmc = output_direc + "/Imputed_Quartets_wqmc_format"
	out_newick = output_direc + "/Imputed_Quartets_Newick_format"

	shutil.copytree(wqmc_style,out_wqmc)
	shutil.copytree(newick_style,out_newick)




def main():
	arguments = parseArguments()
	
	gt_path = arguments.gt_path
	temp_dir = arguments.temp_dir
	output_path = arguments.output

	print("========= QT-GILD commencing =========")

	working_folder_creation(gt_path,temp_dir,arguments.mode)
	numpy_generator_whole_GT()
	modified_numpy_formation(base_directory)
	impute(base_directory,Taxa_num)
	copy_four_taxa_identifiers(temp_dir)
	qdist(temp_dir)
	copy_results_to_output(output_path,temp_dir)

	print("========= QT-GILD executed =========")

if __name__ == "__main__":
	
	main()