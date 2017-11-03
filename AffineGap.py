import numpy as np


def read_data():
	with open("sequences.txt") as f:
		        data = f.readlines()	
	data =[x.strip() for x in data]
	return data

def find_global_alignment_score(stringone_file_content,stringtwo_file_content):
	match_score=0
	mismatch_score=1
	gap_score=1
	center_star_gap=[]
	stringone_len=len(stringone_file_content) +1
	stringtwo_len=len(stringtwo_file_content) +1
	score_matrix= [[0 for i in range(stringtwo_len)] for j in range(stringone_len)]
	backpointer_matrix= [[0 for i in range(stringtwo_len)] for j in range(stringone_len)]
	for i in range(0,stringtwo_len):
		score_matrix[0][i]=i*gap_score
		backpointer_matrix[0][i]=(0,i-1)
	for j in range(0,stringone_len):
		score_matrix[j][0]=j*gap_score	
		backpointer_matrix[j][0]=(j-1,0)

	backpointer_matrix[0][0]=(-1,-1)
	for i in range(1,stringone_len):
		for j in range(1,stringtwo_len):
			if(stringone_file_content[i-1]==stringtwo_file_content[j-1]):
				mactching_score=score_matrix[i-1][j-1]+match_score
			else:
				mactching_score=score_matrix[i-1][j-1]+mismatch_score

			score_matrix[i][j]=min(mactching_score,score_matrix[i-1][j]+gap_score,score_matrix[i][j-1]+gap_score)
			
			if(score_matrix[i][j]==mactching_score):
				backpointer_matrix[i][j]=(i-1,j-1)
			elif (score_matrix[i][j]==score_matrix[i-1][j]+gap_score):
				backpointer_matrix[i][j]=(i-1,j)
			else :
				backpointer_matrix[i][j]=(i,j-1)
	final_score_value= score_matrix[i][j]
	i=stringone_len-1
	j=stringtwo_len-1
	string_one=string_two=""
	alignment_score=0
	while ((i,j)!=(0,0)):
		if((i-1,j-1)== backpointer_matrix[i][j]):
			string_one+=stringone_file_content[i-1]
			string_two+=stringtwo_file_content[j-1]
		 	if(stringone_file_content[i-1]==stringtwo_file_content[j-1]):
		 		#string_score.append(2)
		 		pass
		 	else:
		 		alignment_score+=1
		elif ((i-1,j)==backpointer_matrix[i][j]):
		 	string_one+=stringone_file_content[i-1]
		 	string_two+='-'
		 	alignment_score+=1
		else : 
		 	string_one+='-'
		 	string_two+=stringtwo_file_content[j-1]
		 	alignment_score+=1
		 	center_star_gap.append(j)
	 	(i,j)= backpointer_matrix[i][j]
	 

	string_one= ''.join(reversed(string_one))
	string_two= ''.join(reversed(string_two))
	return string_one,string_two,alignment_score,center_star_gap

	


def center_star(string_list):
	
	list_length=len(string_list)
	sum_list=[0]*list_length
	matrix = [[0 for x in range(list_length)] for y in range(list_length)] 

	for i in range(list_length):
		for j in range(i+1,list_length):
			matrix[i][j]= find_global_alignment_score(string_list[i],string_list[j])[2]
	
	for i in range(list_length):
		for j in range(i+1,list_length):
			sum_list[i]+=matrix[i][j]
			sum_list[j]+=matrix[i][j]

	min_ele=min(sum_list)
	min_index=sum_list.index(min_ele)
	center_star_global_gap=[]
	center_string= string_list[min_index]
	my_string_list=[]
	for i in range(list_length):
		center_string,string_two,alignment_score,center_star_gap= find_global_alignment_score(center_string,string_list[i])
		#print string_one,string_two,center_star_gap
		my_string_list.append((string_two,center_star_gap))
		center_star_global_gap+=center_star_gap

	gx=[]
	for i in range(list_length):
		string_one,string_two,alignment_score,center_star_gap= find_global_alignment_score(center_string,string_list[i])
		#print string_one,string_two,center_star_gap
		gx.append(string_two)
		center_star_global_gap+=center_star_gap

	for stringx in gx:
		print stringx

	"""
	########## To Print Sum of Pairs Score #########
	score=0
	for i in range(len(gx)):
		for j in range(i+1,len(gx)):
			for c in range(len(gx[i])): 	
				if (gx[i][c]!=gx[j][c]):
					score+=1
	print score
	"""
data=read_data()
center_star(data)
