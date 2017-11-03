import numpy as np
import math
import sys
import binarytree as bt

global index_dict

index_dict={}
index_dict['aa']=0
index_dict['ac']=1
index_dict['ag']=2
index_dict['at']=3
index_dict['ca']=4
index_dict['cc']=5
index_dict['cg']=6
index_dict['ct']=7
index_dict['ga']=8
index_dict['gc']=9
index_dict['gg']=10
index_dict['gt']=11
index_dict['ta']=12
index_dict['tc']=13
index_dict['tg']=14
index_dict['tt']=15

global cluster_index
cluster_index=0
visited_cluster_set=set([])	

def get_2mer(input_string):
	list_twomer=[]
	string_list=list(input_string)
	for index in range(len(string_list)):
		if(index< len(string_list)-1):
			list_twomer.append(input_string[index:index+2])
	return list_twomer


def create_vector(input_string):
	twomer_list=get_2mer(input_string)
	my_vector=[0]*16
	for twomer in twomer_list:
		my_vector[index_dict[twomer]]+=1
	return my_vector
	#print my_vector


def get_vector_distance(vector_one,	vector_two):
	total_sum=0
	my_vector=[0]*16
	for i in range((len(vector_one))):
		total_sum+=(math.pow(vector_one[i]-vector_two[i],2))
	return math.sqrt(total_sum)

def create_distance_matrix(vector_array):
	distance_matrix=	[[0 for x in range(len(vector_array))] for y in range(len(vector_array))]
	for index1 in range(len(vector_array)):
		for index2 in range(len(vector_array)):
			#print vector_array[index2]
			distance_matrix[index1][index2]=(get_vector_distance(vector_array[index1],vector_array[index2]))
	return distance_matrix
	

def get_min_index(distance_matrix):
	
	min_ele=sys.maxint
	min_index=(-1,-1)
	for index1 in range(len(distance_matrix)):
		for index2 in range(len(distance_matrix)):
			if(index1!=index2):
				if(distance_matrix[index1][index2]<min_ele):
					min_ele=distance_matrix[index1][index2]
					min_index=(index1,index2)
	if (min_index==(-1,-1)):
		min_index=(0,1)
	return min_index,min_ele
				

def get_cluster_distance(height_array,i,j,dist):
	HCk=float(dist)/2
	dki=HCk- height_array[i]
	dkj=HCk- height_array[j]
	return HCk,dki,dkj

def start_UPGMA(cluster_array,distance_matrix):
	C=[(cluster,1) for cluster in cluster_array ]
	height_array=[0]*len(cluster_array)
	dist_array=[x[::1] for x in distance_matrix]
	
	
	b_nodes = {cluster:bt.Node(0)for cluster in C}
	for ind in range(1,len(cluster_array)):
		(i,j),dist=get_min_index(dist_array)
		HCk,dki,dkj=get_cluster_distance(height_array,i,j,dist)
		C.append( (str(C[j][0]+C[i][0]),C[j][1]+C[i][1]) )

		new_clus_ind = len(C) -1
		height_array.append(HCk)
		dist_array.append([0]* (len(dist_array[0])))
		for row in dist_array:
		    row+=[0]

		b_nodes[C[i]].value = (C[i][0], dki)
		b_nodes[C[j]].value = (C[j][0], dkj)
		b_nodes[C[new_clus_ind]] = bt.Node((C[new_clus_ind][0],0))
		b_nodes[C[new_clus_ind]].left = b_nodes[C[i]]
		b_nodes[C[new_clus_ind]].right = b_nodes[C[j]]

		for c in range(len(C)-1):
			dist_array[new_clus_ind][c] = (C[i][1] * dist_array[i][c] +C[j][1] * dist_array[j][c])/(C[i][1] +C[j][1] )
			dist_array[c][new_clus_ind] = dist_array[new_clus_ind][c]
		if j > i:
		    i,j = j,i
		C.pop(i)
		C.pop(j)
		height_array.pop(i)
		height_array.pop(j)
		dist_array.pop(i)
		for y in range(len(dist_array)):
		    dist_array[y].pop(i)
		dist_array.pop(j)
		for y in range(len(dist_array)):
		    dist_array[y].pop(j)	
	
	bt.show(b_nodes[C[0]])
	




def run_main():
	string_list=['actgaatcgtact','cctgaatcgtact','actggtaatcact','actggtaatccct']
	vector_array=[]
	
	for s in string_list:
		vector_array.append( create_vector(s))
	
	distance_matrix=create_distance_matrix(vector_array)
	#for value in distance_matrix:
	#	print value
	start_UPGMA(string_list,distance_matrix)

run_main()


