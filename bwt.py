my_file=open("bwt.txt","r")
bwt=my_file.read()
my_qfile=open("query.txt","r")
q=my_qfile.read()
import math

def compute_block(ltf,bwt):
	for i in range(len(ltf)):
		ltf[i]=bwt[i]+ltf[i]
	return sorted(ltf)

def find_final_string(ltf):
	for string in ltf:
		if string[-1]=='$':
			return string

def create_suffix_array(suffix_list):
	sorted_suffix_list=sorted(suffix_list)
	suffix_array=[]
	for suffix in sorted_suffix_list:
		suffix_array.append(suffix_list.index(suffix))
	return suffix_array
def create_suffix_list(my_string):
	suffix_list=[]
	n=len(my_string)
	for i in range(n):
		suffix_list.append(my_string[i:n])
	return suffix_list

def compute_string(bwt):
	ltf=bwt
	ltf =list(''.join(sorted(ltf)))
	for i in range (1,len(ltf)):
		ltf=compute_block(ltf,bwt)
		#print ltf
	my_string=find_final_string(ltf)
	return my_string

def get_LCP_len(text1,text2):
	n=min(len(text1),len(text2))
	c=0
	for i in range(n):
		if(text1[i]==text2[i]):
			c+=1
	return c


def search_query_string(query,suffix_list,suffix_array):
	q_len=len(query)
	n=len(suffix_list[0])-1
	L=0
	R=len(suffix_array)-1
	l=get_LCP_len(query,suffix_list[suffix_array[0]])
	r=get_LCP_len(query,suffix_list[suffix_array[n]])
	x=0
	while(L<=R):
		x+=1
		M=int(math.ceil((L+R)/2))
		minlr=min(l,r)
		m=get_LCP_len(query,suffix_list[suffix_array[M]])
		print "L: "+str(L)+"\tR: "+str(R)+"\tM: "+str(M)+"\tl: "+str(l)+"\tr: "+str(r)+"\tminlr: "+str(minlr)
		if (m==q_len):

			print "m :"+str(m)+" " +q+" was found at "+str(M)
			return
		elif(suffix_list[suffix_array[M]]>query):
			if(R==M):
				break
			print "m :"+str(m)+" Q > suffix SA[M]" 
			R=M
			r=m
		else:
			if(L==M):
				break
			print "m :"+str(m)+" Q < suffix SA[M]"
			L=M
			l=m
		if(L==R):
			break
	print "String not found"


my_string=compute_string(bwt)
print list(my_string)
suffix_list=create_suffix_list(my_string)
suffix_array=create_suffix_array(suffix_list)
print suffix_array
search_query_string(q,suffix_list,suffix_array)
