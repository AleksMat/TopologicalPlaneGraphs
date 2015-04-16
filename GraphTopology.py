from tkinter import *
from tkinter.font import Font

class Triangulation():
    def __init__(self,window):

        mainMenu=Menu(window) #making menu options
        editMenu=Menu(mainMenu,tearoff=0)
        mainMenu.add_cascade(menu=editMenu,label='Edit')
        editMenu.add_command(label='{0} {1:>11}'.format('New','Ctrl-N'),command=self.clearCanvas)
        window.bind('<Control-n>',self.clearCanvas)
        window.bind('<Control-N>',self.clearCanvas)
        window.config(menu=mainMenu)
        
        self.w=1000 #canvas dimensions
        self.h=650
        self.sw = window.winfo_screenwidth() #screen dimensions (for centering)
        self.sh = window.winfo_screenheight()
        
        tw=int((self.sw-self.w)/2)
        th=int((self.sh-self.h)/2)
        window.geometry(str(self.w)+'x'+str(self.h+20)+'+'+str(tw)+'+'+str(th)) #this centers canvas on screen
        self.canvas=Canvas(window,width=self.w,height=self.h)
        self.canvas.pack()
        self.canvas.bind('<Button-1>',self.newVertex)
        self.canvas.grid(row=0)
        self.canvas.configure(background='white')
        
        frame = Frame(window)
        frame.grid(row=1)
        label=Label(frame,text='Connect: ')
        label.grid(row=0,column=0)
        self.entry=Entry(frame)
        self.entry.bind('<Return>',self.newEdge)
        self.entry.grid(row=0,column=1)
        
        self.font=Font(family='Arial', size=8, weight='bold')

        self.clearCanvas() #starts new 

    def clearCanvas(self,event=0):
        self.canvas.delete("all")
        self.entry.delete(0, 'end')
        
        self.graph=TopologicalGraph(0,[],[[]]) #TopologicalGraph(4,[(0,1),(1,2),(2,3),(3,0)],[ [[(0,True),(1,True),(2,True),(3,True)]],[[(0,False),(1,False),(2,False),(3,False)]]])
        self.points=[(0,0),(self.w,0),(self.w,self.h),(0,self.h)]
        self.lines={}
        self.lines_num=0
        self.add_line(0,1,None,0)
        self.add_line(1,2,None,0)
        self.add_line(2,0,1,0)
        self.add_line(0,3,1,None)
        self.add_line(3,2,1,None)
        self.triangles=[[0,2,1,5,3,1],[2,0,3,4,6,8]] #first 3 are points, second 3 are lines
        

    def add_line(self,p1,p2,t1,t2): #line between points p1 and p2 that is dividing triangles t1 and t2
         self.lines[self.lines_num]=[p1,p2,t1,False]
         self.lines[self.lines_num+1]=[p2,p1,t2,False]
         self.lines_num+=2
         self.canvas.create_line(self.points[p1][0],self.points[p1][1],self.points[p2][0],self.points[p2][1])
        
    def newVertex(self,event):
        print(event.x,event.y)
        tri=self.position(event.x,event.y)
        print(tri)
        p=len(self.points)
        t=len(self.triangles)
        l=self.lines_num
        self.graph.add_vertex(0)
        r=2 #radius
        self.canvas.create_oval(event.x-r,event.y-r,event.x+r,event.y+r,fill='red',outline='red')
        self.points.append((event.x,event.y))
        self.canvas.create_text(event.x+3*r,event.y+3*r,text=str(len(self.graph.vert_e)-1),font=self.font)
        if len(tri)==1:  #tu je še za premislt...
            self.add_line(self.triangles[tri[0]][0],p,t+1,tri[0])
            self.add_line(self.triangles[tri[0]][1],p,tri[0],t)
            self.add_line(self.triangles[tri[0]][2],p,t,t+1)
            self.triangles.append([self.triangles[tri[0]][1],self.triangles[tri[0]][2],p,self.triangles[tri[0]][4],l+4,l+3])
            self.triangles.append([self.triangles[tri[0]][2],self.triangles[tri[0]][0],p,self.triangles[tri[0]][5],l,l+5])
            self.lines[self.triangles[tri[0]][4]][2]=t
            self.lines[self.triangles[tri[0]][5]][2]=t+1
            self.triangles[tri[0]][2]=p
            self.triangles[tri[0]][4]=l+2
            self.triangles[tri[0]][5]=l+1

    def position(self,x,y):   #find triangles that contain the point (at least on border) ... this is not optimal algorithm
        tri=[]
        for i in range (len(self.triangles)):
            #print(x,y,i)
            t=True
            for j in range (3):
                j1=(j+1)%3
                if (self.points[self.triangles[i][j1]][0]-self.points[self.triangles[i][j]][0])*(y-self.points[self.triangles[i][j]][1]) - (x-self.points[self.triangles[i][j]][0])*(self.points[self.triangles[i][j1]][1]-self.points[self.triangles[i][j]][1])>0:       
                    t=False
                    break
            if t:
                tri.append(i)
        return tri

    def newEdge(self,event=0):
        try:
            s1=self.entry.get()
            s=s1.split(',')
            t1=True
            for i in range (len(s)):
                s[i]=int(s[i].strip())
                if s[i]>=len(self.graph.vert_e):
                    t1=False
            if len(s)==2 and t1:
                self.entry.delete(0, 'end')
                p=self.path(s) #gets path
        except:
            pass

    def path(s): #calculates shortest path with BFS
        return []
        
            

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
    
    def __repr__(self):
        s=str(len(self.vert_e))+' Vertices: \n'+str(self.vert_e)+'\n'
        s+=str(len(self.edges)//2)+' Edges: \n'+str(self.edges)+'\n'
        s+=str(len(self.faces))+' Faces: \n'+str(self.faces)+'\n'
        s+=str(len(self.borders))+' Borders: \n'+str(self.borders)
        for i in self.borders.keys():
            s+='\n'+str(i)+':'
            j=self.borders[i][0]
            if j<0:
                s+=' v'+str(-j-1)
            else:
                s+=' '+str(j)
                j1=self.edges[j][4]
                while j1!=j:
                    s+=' '+str(j1)
                    j1=self.edges[j1][4]
                    
                
        #'\n'+str(self.edges)+'\n'+str(self.faces)+'\n'+str(self.borders)
        return s
        '''print(g.vert_e)
        print(g.edges)
        print(g.faces)
        print(g.borders)'''
        

    def add_vertex(self,face): #adds a new vertex inside of face
        self.vert_e.append([-self.borders_num-1])
        self.faces[face][self.borders_num]=True
        self.borders[self.borders_num]=(-len(self.vert_e),face)
        self.borders_num+=1

    def add_edge(self,v1,v2,e1=None,e2=None,*borders):   #adds a new edge between vertices v1 and v2 inside of face f, if it creates a new face
        self.edges.append([v1,v2,-1,-1,-1])
        self.edges.append([v2,v1,-1,-1,-1])
        if len(self.vert_e[v1])==1 and self.vert_e[v1][0]<0:
            b1=-self.vert_e[v1][0]-1     # b1 and b2 are borders
            self.vert_e[v1]=[]
        else:
            if e1==None:
                e1=self.vert_e[v1][0]
            b1=self.edges[e1][2]
        if len(self.vert_e[v2])==1 and self.vert_e[v2][0]<0:
            b2=-self.vert_e[v2][0]-1
            self.vert_e[v2]=[]
        else:
            if e2==None and len(self.vert_e[v2])>0:
                e2=self.vert_e[v2][0]
            if v1==v2:
                b2=b1
            else:
                b2=self.edges[e2][2]
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
            self.edges[len(self.edges)-2][2]=b1
            self.edges[len(self.edges)-1][2]=b1
            if e1!=None:
                l1=self.edges[e1][3]
                self.edges[len(self.edges)-2][3]=l1
                self.edges[len(self.edges)-1][4]=e1
                self.edges[e1][3]=len(self.edges)-1
                self.edges[l1][4]=len(self.edges)-2
            else:
                self.edges[len(self.edges)-2][3]=len(self.edges)-1
                self.edges[len(self.edges)-1][4]=len(self.edges)-2
            if e2!=None:
                l2=self.edges[e2][3]
                self.edges[len(self.edges)-2][4]=e2
                self.edges[len(self.edges)-1][3]=l2
                self.edges[e2][3]=len(self.edges)-2
                self.edges[l2][4]=len(self.edges)-1
                self.edges[l2][2]=b1
                while e2!=l2:
                    l2=self.edges[l2][3]
                    self.edges[l2][2]=b1
            else:
                self.edges[len(self.edges)-2][4]=len(self.edges)-1
                self.edges[len(self.edges)-1][3]=len(self.edges)-2
                
        else:
            k=self.borders[b1][1]
            self.borders[self.borders_num]=(len(self.edges)-1,len(self.faces))
            self.borders[b1]=(len(self.edges)-2,k)
            self.edges[len(self.edges)-2][2]=b1
            self.edges[len(self.edges)-1][2]=self.borders_num
            if e1!=None:
                l1=self.edges[e1][3]
                l2=self.edges[e2][3]
                self.edges[len(self.edges)-2][3]=l1
                self.edges[len(self.edges)-2][4]=e2
                self.edges[len(self.edges)-1][3]=l2
                self.edges[len(self.edges)-1][4]=e1
                self.edges[e1][3]=len(self.edges)-1
                self.edges[l1][4]=len(self.edges)-2
                self.edges[e2][3]=len(self.edges)-2
                self.edges[l2][4]=len(self.edges)-1
                j=e1
                self.edges[e1][2]=self.borders_num
                while j!=l2:
                    j=self.edges[j][4]
                    self.edges[j][2]=self.borders_num
            else:
                self.edges[len(self.edges)-2][3]=len(self.edges)-2
                self.edges[len(self.edges)-2][4]=len(self.edges)-2
                self.edges[len(self.edges)-1][3]=len(self.edges)-1
                self.edges[len(self.edges)-1][4]=len(self.edges)-1
            self.faces.append({})
            self.faces[-1][self.borders_num]=True
            if borders:
                for i in range (len(borders)):
                    print(self.faces[-1],borders[i])
                    self.faces[-1][borders[i]]=True
                    del self.faces[k][borders[i]]
                    self.borders[borders[i]]=(self.borders[borders[i]][0],len(self.faces)-1)
            self.borders_num+=1

window=Tk()
window.title('PlaneGraph')
root=Triangulation(window)
#window.mainloop()

#g=TopologicalGraph(0,[],[[]])
#print(g)
#g.add_vertex(0)
#g.add_vertex(0)
#g.add_vertex(0)
#g.add_edge(0,1,None,None)
#g.add_vertex(0)
#print(g)
#h=TopologicalGraph(5,[(0,2),(1,2),(0,1),(3,4)],[[[(2,False),(0,True),(1,False)]],[[(2,True),(0,False),(1,True)],[(3,False),(3,True)]]])
#print(h)


'''g=TopologicalGraph(5,[(0,2),(1,2),(0,1),(3,4)],[[[(2,False),(0,True),(1,False)]],[[(2,True),(0,False),(1,True)],[(3,False),(3,True)]]])
print(g.vert_e)
print(g.edges)
print(g.faces)
print(g.borders)
g.add_edge(0,3,4,6)
print(g.vert_e)
print(g.edges)
print(g.faces)
print(g.borders)'''
'''g.add_vertex(0)
print(g.vert_e)
print(g.edges)
print(g.faces)
print(g.borders)
g.add_edge(5,5,None,None)
print(g.vert_e)
print(g.edges)
print(g.faces)
print(g.borders)'''
