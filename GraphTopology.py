
class TopologicalGraph():

    def __init__(self,vert_num,edges,faces): #takes number of vertices, list of edges,
        self.vert_e=[[] for i in range (vert_num)] # lists of edges from each vertex
        #self.vert_f=[[] for i in range (vert_num)] # lists of faces which are bounded by vertex 
        self.edges=[] 
        for i in range (len(edges)):
            self.edges.append([edges[i][0],edges[i][1],-1,-1,-1])  #each edge is added twice in consetutive places in list
            self.edges.append([edges[i][1],edges[i][0],-1,-1,-1])  #besides endpoints it also remembers boundary, previous and next edge
            e=edges[i][0]
            self.vert_e[edges[i][0]].append(2*i)
            self.vert_e[edges[i][1]].append(2*i+1)
        self.faces=[{} for i in range (len(faces))]  #for each face dictionary stores its boundaries
        self.borders={}
        self.borders_num=0
        for i in range (len(faces)):
            for j in range (len(faces[i])):
                self.faces[i][self.borders_num]=True
                if faces[i][j][0][1]==None:
                    self.borders[self.borders_num]=(-faces[i][j][0][0]-1,i)  #negative values are for single points
                    self.vert_e[faces[i][j][0][0]]=-self.borders_num -1
                else:
                    e=2*faces[i][j][0][0]
                    if not faces[i][j][0][1]:
                        e+=1
                    self.borders[self.borders_num]=(e,i)
                    e1=2*faces[i][j][-1][0]
                    if not faces[i][j][-1][1]:
                        e1+=1
                    self.edges[e][2]=self.borders_num
                    self.edges[e][4]=e1
                    self.edges[e1][3]=e
                    for k in range (1,len(faces[i][j])):
                        e1=e
                        e=2*faces[i][j][k][0]
                        if not faces[i][j][k][1]:
                            e+=1
                        self.edges[e][4]=e1
                        self.edges[e1][3]=e
                        self.edges[e][2]=self.borders_num
                self.borders_num+=1

    def add_vertex(self,face): #adds a new vertex inside of face
        self.vert_e.append([-self.borders_num-1])
        self.faces[face][self.borders_num]=True
        self.borders[self.borders_num]=(-len(self.vert_e),face)
        self.borders_num+=1

    def add_edge(self,v1,v2,e1=None,e2=None,*borders):   #adds a new edge between vertices v1 and v2 inside of face f, if it creates a new face
        '''if e1<0:
            v1=-e1-1
        else:
            v1=self.edges[e1][0]
        if e2<0:
            v2=-e2-1
        else:
            v2=self.edges[e2][0]'''
        self.edges.append([v1,v2,-1,-1,-1])
        self.edges.append([v2,v1,-1,-1,-1])
        print(self.vert_e[v2])
        if len(self.vert_e[v1])==1 and self.vert_e[v1][0]<0:
            b1=-self.vert_e[v1][0]-1     # b1 and b2 are borders
            self.vert_e[v1]=[]
        else:
            b1=self.edges[e1][2]
        if len(self.vert_e[v2])==1 and self.vert_e[v2][0]<0:
            b2=-self.vert_e[v2][0]-1
            self.vert_e[v2]=[]
        else:
            b2=self.edges[e1][2]
        self.vert_e[v1].append(len(self.edges)-2)
        self.vert_e[v2].append(len(self.edges)-1)
        if b1!=b2:
            j1,k1=self.borders[b1]
            j2,k2=self.borders[b2]
            if k1!=k2:
                print('Wrong input')
                raise
            del self.faces[k1][b2]
            del self.borders[b2]
            self.borders[b1]=(len(self.edges)-2,k1)
            l1=self.edges[j1][3]
            l2=self.edges[j2][3]
            self.edges[len(self.edges)-2][2]=b1
            self.edges[len(self.edges)-2][3]=l1
            self.edges[len(self.edges)-2][4]=j2
            self.edges[len(self.edges)-1][2]=b1
            self.edges[len(self.edges)-1][3]=j1
            self.edges[len(self.edges)-1][4]=l2
            self.edges[j1][3]=len(self.edges)-1
            self.edges[l1][4]=len(self.edges)-2
            self.edges[j2][3]=len(self.edges)-2
            self.edges[l2][4]=len(self.edges)-1
            self.edges[j2][2]=b1
            while j2!=l2:
                j2=self.edges[j2][4]
                self.edges[j2][2]=b1
        else:
            k=self.borders[b1][1]
            self.borders[self.borders_num]=(len(self.edges)-1,len(self.faces))
            self.borders[b1]=(len(self.edges)-2,k)
            l1=self.edges[e1][3]
            l2=self.edges[e2][3]
            self.edges[len(self.edges)-2][2]=b1
            self.edges[len(self.edges)-2][3]=l1
            self.edges[len(self.edges)-2][4]=e2
            self.edges[len(self.edges)-1][2]=self.borders_num
            self.edges[len(self.edges)-1][3]=e1
            self.edges[len(self.edges)-1][4]=l2
            self.edges[e1][3]=len(self.edges)-1
            self.edges[l1][4]=len(self.edges)-2
            self.edges[e2][3]=len(self.edges)-2
            self.edges[l2][4]=len(self.edges)-1
            j=e1
            self.edges[e1][2]=self.borders_num
            while j!=l2:
                j=self.edges[j][4]
                self.edges[j][2]=self.borders_num
            self.faces.append({})
            if borders:
                for i in range (len(borders)): 
                    self.faces[-1][borders[i]]=True
                    del self.faces[k][borders[i]]
                    self.borders[borders[i]]=(self.borders[borders[i]][0],len(self.faces)-1)       


g=TopologicalGraph(5,[(0,2),(1,2),(0,1),(3,4)],[[[(2,False),(0,True),(1,False)]],[[(2,True),(0,False),(1,True)],[(3,False),(3,True)]]])
print(g.vert_e)
print(g.edges)
print(g.faces)
print(g.borders)
g.add_vertex(0)
print(g.vert_e)
print(g.edges)
print(g.faces)
print(g.borders)
g.add_edge(5,5,[0])
print(g.vert_e)
print(g.edges)
print(g.faces)
print(g.borders)
