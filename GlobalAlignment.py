import numpy

stringone_file=open("gene1.txt","r")
stringone_file_content=stringone_file.read()

match_score=2
mismatch_score=-3
gap_score=-2

stringtwo_file=open("gene2.txt","r")
stringtwo_file_content=stringtwo_file.read()

stringone_len=len(stringone_file_content) +1
stringtwo_len=len( stringtwo_file_content) +1

#print stringtwo_len
#print stringone_len



#print stringtwo_len
#print stringone_len

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

		score_matrix[i][j]=max(mactching_score,score_matrix[i-1][j]+gap_score,score_matrix[i][j-1]+gap_score)
		
		if(score_matrix[i][j]==mactching_score):
			backpointer_matrix[i][j]=(i-1,j-1)
		elif (score_matrix[i][j]==score_matrix[i-1][j]+gap_score):
			backpointer_matrix[i][j]=(i-1,j)
		else :
			backpointer_matrix[i][j]=(i,j-1)

final_score_value= score_matrix[i][j]

"""
for i in range(0,stringone_len):
		print backpointer_matrix[i]
	
for i in range(0,stringone_len):
		print score_matrix[i]	
"""
i=stringone_len-1
j=stringtwo_len-1
string_one=string_two=""
string_score=[]

while ((i,j)!=(0,0)):
	 if((i-1,j-1)== backpointer_matrix[i][j]):
	 	string_one+=stringone_file_content[i-1]
	 	string_two+=stringtwo_file_content[j-1]
	 	if(stringone_file_content[i-1]==stringtwo_file_content[j-1]):
	 		string_score.append(2)
	 	else:
	 		string_score.append(-3)
	 elif ((i-1,j)==backpointer_matrix[i][j]):
	 	string_one+=stringone_file_content[i-1]
	 	string_two+='-'
	 	string_score.append(-2)
	 else : 
	 	string_one+='-'
	 	string_two+=stringtwo_file_content[j-1]
	 	string_score.append(-2)
	 
	 (i,j)= backpointer_matrix[i][j]
	 

string_one= ''.join(reversed(string_one))
string_two= ''.join(reversed(string_two))
final_score=[]
for i in reversed(string_score):
		final_score.append(i)


for i in range (0,len(final_score)):
	print string_one[i] + " " +string_two[i] + " " + str(final_score[i])

print final_score_value
