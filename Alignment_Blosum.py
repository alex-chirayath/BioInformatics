import numpy
import sys


def create_codon_map():
	with open("codon.txt") as f:
	        data = f.readlines()
	codon={}
	for row in data:
		row_list=row.split('\t')
		codon[row_list[0]]=row_list[2]
	return codon

def create_blosum_matrix():
	with open("BLOSUM80") as f:
	        data = f.readlines()
	matrix=[]
	acid_list=[]
	i=0
	for line in data:
		if i>0:
			row=line[2:-2]
			row_list=row.split(' ')
			for item in row_list:
				if item.strip()=='':
					row_list.remove(item)
			matrix.append(row_list)
		else :
			row=line[2:-2]
			acid_list=row.split(' ')
			for item in acid_list:
				if item.strip()=='':
					acid_list.remove(item)
		i+=1

	return acid_list,matrix

def get_score(a,b,acid_list,matrix):
	index_a=acid_list.index(str(a))
	index_b=acid_list.index(str(b))
	return int(matrix[index_a][index_b])

def preprocess_string(codonstring,codon_map):
	string_len=len(codonstring)
	converted_string=''
	i=0
	while (i<=(string_len-3)):
		converted_string+= str(codon_map[codonstring[i:i+3]])
		i+=3
	return converted_string
def main():
	
	codon_map=create_codon_map()
	stringone_file=open("seq1.faa","r")
	stringone_file_content=stringone_file.read()

	
	stringtwo_file=open("seq2.faa","r")
	stringtwo_file_content=stringtwo_file.read()

	string_one=preprocess_string(stringone_file_content,codon_map)
	
	string_two=preprocess_string(stringtwo_file_content,codon_map)
	

	calculate_scores(string_one,string_two,-2,-0.5)
	calculate_scores(string_one,string_two,-1,-0.25)
	calculate_scores(string_one,string_two,-1,-0.1)
	calculate_scores(string_one,string_two,-0.5,-0.05)


def calculate_scores(stringone_file_content,stringtwo_file_content, gap_score,gap_expansion_score):
	g=gap_score
	h=gap_expansion_score
	stringone_len=len(stringone_file_content) +1
	stringtwo_len=len( stringtwo_file_content) +1
	acid_list,blosum_matrix=create_blosum_matrix()
	
	#print get_score('G','K',acid_list, blosum_matrix)
	

	V  = [[0 for i in range(stringtwo_len)] for j in range(stringone_len)]
	B  = [[0 for i in range(stringtwo_len)] for j in range(stringone_len)]
	Gx = [[0 for i in range(stringtwo_len)] for j in range(stringone_len)]
	Gy = [[0 for i in range(stringtwo_len)] for j in range(stringone_len)]
	S  = [[0 for i in range(stringtwo_len)] for j in range(stringone_len)]
	

	for i in range(0,stringtwo_len):
		S[0][i]=-1 * sys.maxint
		B[0][i]=(0,i-1)
		Gy[0][i]=g + i*(h)
		Gx[0][i]=-1 * sys.maxint

	for j in range(0,stringone_len):
		S[j][0]=-1 * sys.maxint
		B[j][0]=(j-1,0)
		Gy[j][0]=g + i*(h)
		Gx[j][0]=-1 * sys.maxint

	S[0][0]=0
	B[0][0]=(-1,-1)


	for i in range(1,stringone_len):
		for j in range(1,stringtwo_len):
			S[i][j]=max(S[i-1][j-1],Gx[i-1][j-1],Gy[i-1][j-1])+get_score(stringone_file_content[i-1],stringtwo_file_content[j-1],acid_list,blosum_matrix)
			Gx[i][j]=max(S[i-1][j]+g+h,Gx[i-1][j]+h,Gy[i-1][j]+g+h)
			Gy[i][j]=max(S[i][j-1]+g+h,Gx[i][j-1]+g+h,Gy[i][j-1]+h)
			V[i][j]=max(S[i][j],Gx[i][j],Gy[i][j])
			
			if(V[i][j]==S[i][j]):
				B[i][j]=(i-1,j-1)
			elif (V[i][j]==Gx[i][j]):
				B[i][j]=(i-1,j)
			else :
				B[i][j]=(i,j-1)

	final_score_value= V[i][j]

	i=stringone_len-1
	j=stringtwo_len-1
	string_one=string_two=""
	string_score=[]
	x_score = g+h
	y_score = g+h

	while ((i,j)!=(0,0)):
		 if((i-1,j-1)== B[i][j]):
		 	string_one+=stringone_file_content[i-1]
		 	string_two+=stringtwo_file_content[j-1]
		 	string_score.append(get_score(stringone_file_content[i-1],stringtwo_file_content[j-1],acid_list,blosum_matrix) )
			x_score=g+h
			y_score=g+h
		 elif ((i-1,j)==B[i][j]):
		 	string_one+=stringone_file_content[i-1]
		 	string_two+='-'
			y_score=h
			x_score=g+h		 	
			string_score.append(y_score)
		 else : 
		 	string_one+='-'
		 	string_two+=stringtwo_file_content[j-1]
		 	x_score=h
			y_score=g+h
			string_score.append(x_score)
		 
		 (i,j)= B[i][j]
		 

	print ""
	string_one= ''.join(reversed(string_one))
	string_two= ''.join(reversed(string_two))
	final_score=[]
	for i in reversed(string_score):
			final_score.append(i)


	for i in range (0,len(final_score)):
		print string_one[i] + " " +string_two[i] + " " + str(final_score[i])

	mytuple=(gap_score,gap_expansion_score)
	print final_score_value , str (mytuple)
	print ""



if __name__ == '__main__':
    main()

