import numpy as np 
import sys




if(len(sys.argv) < 3):
	print("format: <handle.py> input_file base_dir")
	exit()
input_file = sys.argv[1]
base_dir = sys.argv[2]

Four_taxa_folder = base_dir + "/../Four_Taxa_Map"
file_sep = input_file.split("/")[-1].split("_")
print(file_sep[0])

b = np.load(input_file+".npy")
idx = file_sep[0]

file_name = Four_taxa_folder + "/FourTaxaSeqMap_" + idx
f = open(file_name,'r')
four_taxa_seq_dict = eval(f.read())

out_file = base_dir+"/Imputed_Quartets_" + idx
f_out=open(out_file,'a')
x,y,z=b.shape

# total_string=""
# final_output=""
for i in range(0,x):
	#f_out.write("\n"+"GT-> "+str(i+1)+"\n")
	print("working GT-> " + str(i+1))
	for j in range(0,y):


		temp=b[i][j]

		quartet_no=j+1
		each_seq=four_taxa_seq_dict[quartet_no]
		temp2 = each_seq.split(',')
		t1=temp2[0]
		t2=temp2[1]
		t3=temp2[2]
		t4=temp2[3]
		s1=t1+','+t2+'|'+t3+','+t4
		s2=t1+','+t3+'|'+t2+','+t4
		s3=t1+','+t4+'|'+t2+','+t3
		# if(i%10 == 0):
		# 	f_out.write(final_output)
		# 	final_output = ""
		if(temp[0] ==1.0 ): 
			#print(s1)
			if(i == x-1 and j == y-1):
				f_out.write(s1)
			else:
				f_out.write(s1+"\n")
			# final_output += s1+"\n"
			# if(i+j==0):
			# 	# total_string=s1
			# else:
			# 	total_string=total_string+" "+s1
		elif(temp[1] ==1.0 ): 
			#print(s2)
			if(i == x-1 and j == y-1):
				f_out.write(s2)
			else:
				f_out.write(s2+"\n")
			# final_output += s2+"\n"
			# if(i+j==0):
			# 	total_string=s2
			# else:
			# 	total_string=total_string+" "+s2
		elif(temp[2] ==1.0 ):	
			#print(s3)
			if(i == x-1 and j == y-1):
				f_out.write(s3)
			else:
				f_out.write(s3+"\n")
			# final_output += s3+"\n"
			# if(i+j==0):
			# 	total_string=s3
			# else:
			# 	total_string=total_string+" "+s3
		else:
			str_make = "OK"
			#print("Error, not expected")
			#exit(1)
	
#f_out.write(final_output)
#print(total_string)