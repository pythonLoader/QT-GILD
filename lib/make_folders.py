import os
import sys



def create(mode):

	folder_list=[]

	folder_list.append("{}/Incomplete_GT".format(base_directory))
	if(int(mode) == 1):
		folder_list.append("{}/Incomplete_ST_WQFM".format(base_directory))
	
	for folder in folder_list:
		if not os.path.exists(folder):
			os.mkdir(folder)

mode = sys.argv[1]
base_directory = sys.argv[2]
# print(mode)

create(mode)