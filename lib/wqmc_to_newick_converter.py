
import os,sys
import time
if(len(sys.argv) < 3):
		print("Format -> handle.py <input_file> <base_directory>")
		exit()

input_file_name = sys.argv[1]
base_direc = sys.argv[2]
# with open(input_file_name, "r") as input_file:
# 	data = input_file.read()
input_ = open(input_file_name, "r")
newick_format=""
# lines=data.split("\n")
# no_of_lines=len(lines)
# 
# total_weight = 0.0

print("Working with", input_file_name)

start_time = time.time()
for lines in input_:
	# print(i)
	splt = lines.split(":")
	weight = splt[1]
	parts = splt[0].split("|")
	left_part = parts[0]
	right_part = parts[1]
	lps = left_part.split(",")
	rps = right_part.split(",")
	A = lps[0]
	B = lps[1]
	C = rps[0]
	D = rps[1]
	newick_format += "(("+A+","+B+"),("+C+","+D+")); " + weight
	# ((BOS,CAL),(CAN,CHO)); 1
	# if(i == no_of_lines-2):
	# 		# print("OK?")
	# 	newick_format=newick_format+"(("+A+","+B+"),("+C+","+D+")); " + weight
	# else:
	# 	newick_format=newick_format+"(("+A+","+B+"),("+C+","+D+")); " + weight+"\n"


print("End_Time",time.time()-start_time)

# for i in range(0,no_of_lines):
# 	if lines[i].startswith('('):
# 		#print(lines[i])
# 		left_part=lines[i].split(';')
# 		weight=left_part[1]
# 		weight=weight.replace(' ','')
# 		total_weight += int(weight)
		
# #print(total_weight)
# print(no_of_lines)
# for i in range(0,no_of_lines):
# 	if lines[i].startswith('('):
# 		#print(lines[i])
# 		left_part=lines[i].split(';')
# 		#parts=lines[i].split(',')
# 		parts=left_part[0].split(',')
# 		weight=left_part[1]
# 		#total_weight += int(weight)
# 		weight=weight.replace(' ','')
# 		#weight = float(weight)
# 		#weight = str(weight/total_weight)
# 		#print(parts)
# 		#q1=parts[0][2:]
# 		q1=parts[0].replace('(','')
# 		q2=parts[1].replace(')','')
# 		q3=parts[2].replace('(','')
# 		q4=parts[3].replace(')','')
# 		#q2=parts[1][0:len(parts[1])-1]
# 		#q3=parts[2][1:]
# 		#q4=parts[3][0:len(parts[3])-5]
# 		if(i == no_of_lines-2):
# 			# print("OK?")
# 			wqmc_format=wqmc_format+q1+","+q2+"|"+q3+","+q4+":"+weight
# 		else:
# 			wqmc_format=wqmc_format+q1+","+q2+"|"+q3+","+q4+":"+weight+"\n"
		
	
#print(wqmc_format)
output_dir = base_direc +"/Quartets_Newick_format"
# output_dir = "Quartets_Newick_format_RE"
if not os.path.exists(output_dir):
	os.mkdir(output_dir)

out_file = input_file_name.split('/')[-1].split(".")[0].split('_')[3] + "_GT_newick.quartets"
with open(output_dir+"/"+out_file, "w+") as f:
	f.write(newick_format)
