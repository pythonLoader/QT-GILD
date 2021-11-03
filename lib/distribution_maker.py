import subprocess
import os
import shutil
from time import time

d_map = {}
g_map = {}

base_direc = ""
def Array_dir_and_moving():
	direc = base_direc+"/Array_dir"
	if not os.path.exists(direc):
		os.mkdir(direc)
	source = os.listdir(base_direc)
	for file in source:
	    if file.endswith('.npy'):
	    	file = base_direc +"/" + file
	    	shutil.move(file, direc)


def numpy_to_quartets():
	print(os.getcwd())
	direc = base_direc+"/Imputed_Quartets"
	if not os.path.exists(direc):
		os.mkdir(direc)
	in_direc = base_direc+"/Array_dir"
	for file in os.listdir(in_direc):
		print(file)
		i = file.split("_")[0]
		print(i)
		# if(int(i) != 11):
		# 	continue
		f_name = in_direc+"/"+str(i) + "_imputed_numpy"

		out_file = "Imputed_Quartets_" + str(i) 
		copy_file = base_direc + "/Imputed_Quartets_" + str(i) 
		subprocess.call(['python','lib/numpy_to_quartets.py',f_name, base_direc])
		shutil.move(copy_file,direc+"/"+out_file)

def quartets_wqmc_format():

	input_dir = base_direc+"/Imputed_Quartets"
	for file in os.listdir(input_dir):
		i = file.split("_")[2]
		input_file = "Imputed_Quartets_" + str(i) 
		subprocess.call(['python','lib/Imputed_quartets_counter_maker_fl.py',input_dir,input_file,base_direc])


def quartets_newick_format():
	input_dir = base_direc+"/Imputed_Quartets_wqmc_format"
	for file in os.listdir(input_dir):
		i = file.split("_")[3]
		input_file = input_dir +"/" + file
		# input_file = input_dir + "/Imputed_Quartets_wqmc_" + str(i)+".qrtt" 
		subprocess.call(['python','lib/wqmc_to_newick_converter.py',input_file, base_direc])


def qdist(base_directory):
	# leaving_dir = os.getcwd()
	# os.chdir(base_directory)

	global base_direc
	base_direc = base_directory + "/GT_Numpy/Imputed_GT_Numpy"
	Array_dir_and_moving()
	numpy_to_quartets()
	quartets_wqmc_format()
	quartets_newick_format()

	# os.chdir(leaving_dir)

