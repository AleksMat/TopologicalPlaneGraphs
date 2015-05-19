from tkinter import *
from tkinter.font import Font
from math import sqrt
from queue import *


class Triangulation():
    def __init__(self,window):

        mainMenu=Menu(window) #making menu options
        self.editMenu=Menu(mainMenu,tearoff=0)
        mainMenu.add_cascade(menu=self.editMenu,label='Edit')
        self.editMenu.add_command(label='{0} {1:>11}'.format('New','Ctrl-N'),command=self.clearCanvas)
        window.bind('<Control-n>',self.clearCanvas)
        window.bind('<Control-N>',self.clearCanvas)
        window.config(menu=mainMenu)
        
        self.editMenu.add_command(label='{0} {1:>11}'.format('Triangulation','On'),command=self.redraw)
        
        self.w=1000 #canvas dimensions
        self.h=650
        self.sw = window.winfo_screenwidth() #screen dimensions (for centering)
        self.sh = window.winfo_screenheight()
        
        tw=int((self.sw-self.w)/2)
        th=int((self.sh-self.h)/2)
        window.geometry(str(self.w)+'x'+str(self.h+20)+'+'+str(tw)+'+'+str(th)) #this centers canvas on screen
        self.canvas=Canvas(window,width=self.w,height=self.h)
        self.canvas.pack()
        self.canvas.bind('<Button-1>',self.click)
        self.canvas.grid(row=0)
        self.canvas.configure(background='white')
        
        #frame = Frame(window)
        #frame.grid(row=1)
        #label=Label(frame,text='Connect: ')
        #label.grid(row=0,column=0)
        #self.entry=Entry(frame)
        #self.entry.bind('<Return>',self.newEdge)
        #self.entry.grid(row=0,column=1)
        
        self.font=Font(family='Arial', size=8, weight='bold')

        self.r=4 #point radius

        self.connect=[] #state of move

        self.tri_switch=True  #if program should draw triangluation or not

        self.clearCanvas() #starts new 
    
    def clearCanvas(self,event=0):
        self.canvas.delete("all")
        #self.entry.delete(0, 'end')
        
        self.graph=TopologicalGraph(0,[],[[]]) #TopologicalGraph(4,[(0,1),(1,2),(2,3),(3,0)],[ [[(0,True),(1,True),(2,True),(3,True)]],[[(0,False),(1,False),(2,False),(3,False)]]])
        self.points=[(0,0),(self.w,0),(self.w,self.h),(0,self.h)]
        self.vert_p=[] #pointers from vertices to self.points
        self.lines={}
        self.lines_num=0
        self.add_line(0,1,None,0,False)
        self.add_line(1,2,None,0,False)
        self.add_line(2,0,1,0,False)
        self.add_line(0,3,1,None,False)
        self.add_line(3,2,1,None,False)
        self.triangles=[[0,2,1,5,3,1,0],[2,0,3,4,6,8,0]] #first 3 are points, second 3 are lines, last is face
        self.connect=[]

    def redraw(self,event=0):
        self.tri_switch=not self.tri_switch
        if self.tri_switch:
            ss='On'
        else:
            ss='Off'
        self.editMenu.entryconfig(2, label='{0} {1:>11}'.format('Triangulation',ss))
        self.canvas.delete("all")
        for i in range (len(self.vert_p)):
            x=self.points[self.vert_p[i]][0]
            y=self.points[self.vert_p[i]][1]
            self.canvas.create_oval(x-self.r,y-self.r,x+self.r,y+self.r,fill='red',outline='red')
            self.canvas.create_text(x+3*self.r,y+3*self.r,text=str(i),font=self.font)
        for i in self.lines.keys():
            if ((i>>1)<<1)==i:
                p1=self.lines[i][0]
                p2=self.lines[i][1]
                if self.lines[i][3]:
                    self.canvas.create_line(self.points[p1][0],self.points[p1][1],self.points[p2][0],self.points[p2][1],fill='red')
                elif self.tri_switch:
                    self.canvas.create_line(self.points[p1][0],self.points[p1][1],self.points[p2][0],self.points[p2][1])
        

    def add_line(self,p1,p2,t1,t2,b): #line between points p1 and p2 that is dividing triangles t1 and t2
         self.lines[self.lines_num]=[p1,p2,t1,b]
         self.lines[self.lines_num+1]=[p2,p1,t2,b]
         self.lines_num+=2
         if b:
             self.canvas.create_line(self.points[p1][0],self.points[p1][1],self.points[p2][0],self.points[p2][1],fill='red')
         elif self.tri_switch:
             self.canvas.create_line(self.points[p1][0],self.points[p1][1],self.points[p2][0],self.points[p2][1])

    def click(self,event): #function for processing mouse clicks
        t=False
        for i in range (len(self.vert_p)):
            x,y=self.points[self.vert_p[i]]
            d=(x-event.x)*(x-event.x) + (y-event.y)*(y-event.y)
            if d<=self.r*self.r:
                t=True
                if len(self.connect)==0 or len(self.connect)==2:
                    self.connect.append(i)
                elif len(self.connect)==4:
                    s=set()
                    s.add(i)
                    self.connect.append(i)
                elif len(self.connect)==5:
                    self.connect[4].add(i)
                break
            elif len(self.connect)==0 and  d<=4*self.r*self.r:
                return
        l=len(self.connect)
        if l==0:
            self.newVertex(event)
            return
        if not t:
            if l==5:
                l=4
            tri=self.position(event.x,event.y)
            if len(tri)>1:
                return
            if l%2==1:
                self.connect.append(tri[0])
            else:
                self.connect[l-1]=tri[0]
            '''l=(((l-1)>>1)<<1)
            for i in range (3):
                if self.triangles[tri[0]][i]==self.vert_p[self.connect[l]]:
                    #print(self.triangles[tri[0]])
                    #print(i,self.lines[self.triangles[tri[0]][i+3]])
                    if len(self.connect)-1==l:
                        self.connect.append(self.triangles[tri[0]][i+3])
                    else:
                        self.connect[-1]=self.triangles[tri[0]][i+3]
                    self.tryconnect()
                    return'''
            self.tryconnect()
            return
        self.tryconnect()
            
    def tryconnect(self):
        print(self.connect)
        if len(self.connect)==1 or len(self.connect)==3:
            if len(self.graph.vert_e[self.connect[-1]])<=1:
                print('Choose next vertex.')
                x,y=self.points[self.vert_p[self.connect[-1]]]
                tri=self.position(x+self.r,y+0.00001)
                self.connect.append(tri[0])
                '''for i in range (3):
                    if self.triangles[tri[0]][i]==self.vert_p[self.connect[-1]]:
                        self.connect.append(self.triangles[tri[0]][i+3])
                        break'''
            else:
                print('Choose edge direction.')
        if len(self.connect)>=4:
            if self.triangles[self.connect[1]][6]!=self.triangles[self.connect[3]][6]:
                print('Cannot connect!')
                self.connect=[]
                return
            else:
                if len(self.connect)==4:
                    s=set()
                    self.connect.append(s)
                f=self.triangles[self.connect[1]][6]
                b1=-1
                b2=-1
                u=True
                for i in self.graph.faces[f].keys():
                    t=self.graph.borders[i][0]
                    u1=False
                    if t<0:
                        t=-t-1
                        if t==self.connect[0]:
                            b1=i
                            u1=True
                        if t==self.connect[2]:
                            u1=True
                            b2=i
                        if t in self.connect[4]:
                            u1=True
                    else:
                        t1=t
                        if self.graph.edges[t][1]==self.connect[0]:
                            b1=i
                            u1=True
                        if self.graph.edges[t][1]==self.connect[2]:
                            b2=i
                            u1=True
                        if self.graph.edges[t][1] in self.connect[4]:
                            u1=True
                        t=self.graph.edges[t][4]
                        while t1!=t:
                            if self.graph.edges[t][1]==self.connect[0]:
                                b1=i
                                u1=True
                            if self.graph.edges[t][1]==self.connect[2]:
                                b2=i
                                u1=True
                            if self.graph.edges[t][1] in self.connect[4]:
                                u1=True
                            t=self.graph.edges[t][4]
                    if not u1:
                        u=False
                if b1!=b2:
                    print('easy')
                    self.easyEdge()
                else:
                    if u:
                        print('hard')
        
        
    def newVertex(self,event):
        tri=self.position(event.x,event.y)
        if len(tri)>1:
            return
        p=len(self.points)
        t=len(self.triangles)
        l=self.lines_num
        f=self.triangles[tri[0]][6]
        self.graph.add_vertex(f)
        self.canvas.create_oval(event.x-self.r,event.y-self.r,event.x+self.r,event.y+self.r,fill='red',outline='red')
        self.points.append((event.x,event.y))
        self.vert_p.append(len(self.points)-1)
        self.canvas.create_text(event.x+3*self.r,event.y+3*self.r,text=str(len(self.graph.vert_e)-1),font=self.font)

        self.add_line(self.triangles[tri[0]][0],p,t+1,tri[0],False)
        self.add_line(self.triangles[tri[0]][1],p,tri[0],t,False)
        self.add_line(self.triangles[tri[0]][2],p,t,t+1,False)
        self.triangles.append([self.triangles[tri[0]][1],self.triangles[tri[0]][2],p,self.triangles[tri[0]][4],l+4,l+3,f])
        self.triangles.append([self.triangles[tri[0]][2],self.triangles[tri[0]][0],p,self.triangles[tri[0]][5],l,l+5,f])
        self.lines[self.triangles[tri[0]][4]][2]=t
        self.lines[self.triangles[tri[0]][5]][2]=t+1
        self.triangles[tri[0]][2]=p
        self.triangles[tri[0]][4]=l+2
        self.triangles[tri[0]][5]=l+1

    def position(self,x,y):   #find triangles that contain the point (at least on border) ... this is not optimal algorithm
        tri=[]
        for i in range (len(self.triangles)):
            t=True
            for j in range (3):
                j1=(j+1)%3
                if (self.points[self.triangles[i][j1]][0]-self.points[self.triangles[i][j]][0])*(y-self.points[self.triangles[i][j]][1]) - (x-self.points[self.triangles[i][j]][0])*(self.points[self.triangles[i][j1]][1]-self.points[self.triangles[i][j]][1])>0:       
                    t=False
                    break
            if t:
                tri.append(i)
        return tri

    def easyEdge(self):
        s1=self.triangleList(self.connect[0],self.connect[1])
        s2=self.triangleList(self.connect[2],self.connect[3])
        print(s1,s2)
        a={}
        q=PriorityQueue()
        for j in range (len(s1)):
            l=self.triangles[s1[j][0]][(s1[j][1]+1)%3+3]^1
            if not self.lines[l][3]:
                x=(self.points[self.lines[l][0]][0] + self.points[self.lines[l][1]][0])/2
                y=(self.points[self.lines[l][0]][1] + self.points[self.lines[l][1]][1])/2
                x1,y1=self.points[self.vert_p[self.connect[0]]]
                d=sqrt( (x-x1)*(x-x1) + (y-y1)*(y-y1))
                a[l]=(d,-1,s1[j][0])
                a[l^1]=(d,-1,s1[j][0])
                q.put((d,l))
        while not q.empty():
            d,l=q.get()
            if d==a[l][0]:
                x=(self.points[self.lines[l][0]][0] + self.points[self.lines[l][1]][0])/2
                y=(self.points[self.lines[l][0]][1] + self.points[self.lines[l][1]][1])/2    
                t=self.lines[l][2]
                if t!=None:
                    for i in range (3,6):
                        #print(self.triangles[t])#,self.lines[self.triangles[t][i]])
                        if self.triangles[t][i]!=l and not self.lines[self.triangles[t][i]][3]:
                            k=self.triangles[t][i]
                            x1=(self.points[self.lines[k][0]][0] + self.points[self.lines[k][1]][0])/2
                            y1=(self.points[self.lines[k][0]][1] + self.points[self.lines[k][1]][1])/2
                            d1=d+sqrt((x-x1)*(x-x1) + (y-y1)*(y-y1))
                            if a.get(k)==None or a.get(k)[0]>d1:
                                a[k]=(d1,l,t)
                                a[k^1]=(d1,l,t)
                                q.put((d1,k^1))
        path=[-1]
        m=1000000
        m1=0
        for j in range (len(s2)):
            l=self.triangles[s2[j][0]][(s2[j][1]+1)%3+3]
            if a.get(l)!=None:
                if a[l][0]<m:
                    path[0]=(s2[j][0],l)
                    m=a[l][0]
                    m1=l
        while m1!=-1:
            path.append((a[m1][2],a[m1][1]))
            m1=a[m1][1]
        path.reverse()
        print(path)
        fp=self.vert_p[self.connect[0]] #first point in triangle
        for i in range (0,len(path)-1):
            x=self.nextPoint(fp,path[i][0],path[i+1][1]^1)
            np=len(self.points) #new point
            self.points.append(x)
            t=len(self.triangles)
            self.add_line(fp,np,t,path[i][0],True)
            j=0
            while self.triangles[path[i][0]][j]!=fp:
                j+=1
            j=(j+2)%3
            op=self.triangles[path[i][0]][j] #old point
            self.triangles[path[i][0]][j]=np
            ol=self.triangles[path[i][0]][j+3] #old line
            self.triangles[path[i][0]][j+3]=self.lines_num-1
            self.lines[path[i+1][1]^1][1]=np
            self.lines[path[i+1][1]][0]=np
            self.lines[ol][2]=t
            self.triangles.append([fp,np,op,self.lines_num-2,self.lines_num,ol,self.triangles[path[0][0]][6]])
            self.add_line(np,op,t,t+1,False)
            j=0
            while self.triangles[path[i+1][0]][j]!=op:
                j+=1
            self.triangles[path[i+1][0]][j]=np
            j1=(j+2)%3
            ol=self.triangles[path[i+1][0]][j1+3]
            self.triangles[path[i+1][0]][j1+3]=self.lines_num
            if i<len(path)-2:
                self.add_line(self.triangles[path[i+1][0]][j1],np,path[i+1][0],t+1,False)
            else:
                self.add_line(self.triangles[path[i+1][0]][j1],np,path[i+1][0],t+1,True)
            self.triangles.append([np,self.triangles[path[i+1][0]][j1],op,self.lines_num-1,ol,self.lines_num-3])
            self.lines[ol][2]=t+1
            fp=np
            if i<len(path)-2 and ol==path[i+2][1]^1:
                path[i+1]=(t+1,-1)
        self.connect=[]


    def nextPoint(self,pp,t,l):
        a=self.points[self.lines[l][0]]
        b=self.points[self.lines[l][1]]
        u=((self.points[pp][0]-a[0])*(b[0]-a[0])+(self.points[pp][1]-a[1])*(b[1]-a[1]))/((b[0]-a[0])*(b[0]-a[0])+(b[1]-a[1])*(b[1]-a[1]))
        eps=0.5 #relative difference to other points
        u=min(max(u,eps),1-eps) # maybe sometihng better?
        return (a[0]+u*(b[0]-a[0]),a[1]+u*(b[1]-a[1]))
        
    


    def triangleList(self,p,t0):
        a=[]
        t=t0
        for i in range (3):
                if self.triangles[t][i]==self.vert_p[p]:
                    a.append((t,i))
                    i0=i
        l=self.triangles[t][i0+3]^1
        if not self.lines[l][3]:
            t=self.lines[l][2]
        while t!=t0:
            for i in range (3):
                if self.triangles[t][i]==self.vert_p[p]:
                    a.append((t,i))
                    l=self.triangles[t][i+3]^1
            if self.lines[l][3]:
                break
            else:
                t=self.lines[l][2]
        if t!=t0:
            t=t0
            l=self.triangles[t][(i0-1)%3 +3]^1
            if not self.lines[l][3]:
                t=self.lines[l][2]
            while t!=t0:
                for i in range (3):
                    if self.triangles[t][i]==self.vert_p[p]:
                        a.append((t,i))
                        l=self.triangles[t][(i-1)%3+3]^1
                if self.lines[l][3]:
                    break
                else:
                    t=self.lines[l][2]
        return a
        

    '''def newEdge(self,event=0):
        s1=self.entry.get()
        s=s1.split(',')
        for i in range (len(s)):
            try:
                s[i]=int(s[i].strip())
                if s[i]>=len(self.graph.vert_e):
                    raise
            except:
                print('Wrong Input')
                return None
        if len(s)==2:
            self.entry.delete(0, 'end')
            p=self.path(s) #gets path
            if p==None:
                print('Cannot connect')
                return None
            if len(p)==1:
                s1=self.vert_p[s[0]]
                s2=self.vert_p[s[1]]
                j=0
                l=0
                while j<3:
                    if self.triangles[p[0][0]][j]==s1 and self.triangles[p[0][0]][(j+1)%3]==s2:
                        l=self.triangles[p[0][0]][3+j]
                        break
                    if self.triangles[p[0][0]][j]==s2 and self.triangles[p[0][0]][(j+1)%3]==s1:
                        l=self.triangles[p[0][0]][3+j]
                        ss=s1
                        s1=s2
                        s2=ss
                        break
                    j+=1
                if not self.lines[l][3]:
                    self.lines[l][3]=True
                    self.lines[l^1][3]=True #xor shift
                    self.canvas.create_line(self.points[s1][0],self.points[s1][1],self.points[s2][0],self.points[s2][1],fill='red')
            else:
                fp=self.vert_p[s[0]] #first point in triangle
                for i in range (0,len(p)-1):
                    x=self.nextPoint(fp,p[i][0],p[i+1][1]^1)
                    np=len(self.points) #new point
                    self.points.append(x)
                    t=len(self.triangles)
                    self.add_line(fp,np,t,p[i][0],True)
                    j=0
                    while self.triangles[p[i][0]][j]!=fp:
                        j+=1
                    j=(j+2)%3
                    op=self.triangles[p[i][0]][j] #old point
                    self.triangles[p[i][0]][j]=np
                    ol=self.triangles[p[i][0]][j+3] #old line
                    self.triangles[p[i][0]][j+3]=self.lines_num-1
                    self.lines[p[i+1][1]^1][1]=np
                    self.lines[p[i+1][1]][0]=np
                    self.lines[ol][2]=t
                    self.triangles.append([fp,np,op,self.lines_num-2,self.lines_num,ol])
                    self.add_line(np,op,t,t+1,False)
                    j=0
                    while self.triangles[p[i+1][0]][j]!=op:
                        j+=1
                    self.triangles[p[i+1][0]][j]=np
                    j1=(j+2)%3
                    ol=self.triangles[p[i+1][0]][j1+3]
                    self.triangles[p[i+1][0]][j1+3]=self.lines_num
                    if i<len(p)-2:
                        self.add_line(self.triangles[p[i+1][0]][j1],np,p[i+1][0],t+1,False)
                    else:
                        self.add_line(self.triangles[p[i+1][0]][j1],np,p[i+1][0],t+1,True)
                    self.triangles.append([np,self.triangles[p[i+1][0]][j1],op,self.lines_num-1,ol,self.lines_num-3])
                    self.lines[ol][2]=t+1
                    fp=np
                    if i<len(p)-2 and ol==p[i+2][1]^1:
                        p[i+1]=(t+1,-1)
                

    def nextPoint(self,pp,t,l):
        a=self.points[self.lines[l][0]]
        b=self.points[self.lines[l][1]]
        u=((self.points[pp][0]-a[0])*(b[0]-a[0])+(self.points[pp][1]-a[1])*(b[1]-a[1]))/((b[0]-a[0])*(b[0]-a[0])+(b[1]-a[1])*(b[1]-a[1]))
        eps=0.5 #relative difference to other points
        u=min(max(u,eps),1-eps) # maybe sometihng better?
        return (a[0]+u*(b[0]-a[0]),a[1]+u*(b[1]-a[1]))


    def path(self,s): #calculates shortest path with BFS
        x=[]
        y=[]
        p=-1
        for i in range (len(self.triangles)):
            x1=0
            if self.triangles[i][0]==self.vert_p[s[0]] or self.triangles[i][1]==self.vert_p[s[0]] or self.triangles[i][2]==self.vert_p[s[0]]:
                x1=1
                y.append(i)
            if self.triangles[i][0]==self.vert_p[s[1]] or self.triangles[i][1]==self.vert_p[s[1]] or self.triangles[i][2]==self.vert_p[s[1]]:
                if x1==1:
                    return [(i,-1)]
                x1=-1
            x.append([x1,0,-1])
        en=-1
        while p<len(y)-1:
            p+=1
            for i in range (3,6):
                l=self.triangles[y[p]][i]
                l=l^1  #xor shift
                t1=self.lines[l][2]
                if t1!=None and x[t1][0]==0 and (not self.lines[l][3]):
                    x[t1][0]=x[y[p]][0]+1
                    x[t1][1]=y[p]
                    x[t1][2]=l
                    y.append(t1)
                if t1!=None and x[t1][0]==-1 and (not self.lines[l][3]):
                    en=t1
                    x[t1][0]=x[y[p]][0]+1
                    x[t1][1]=y[p]
                    p=len(y)-1
                    x[t1][2]=l
                    break
        if en==-1:
            return None
        path=[]
        while x[en][0]>1:
            path.append((en,x[en][2]))
            en=x[en][1]
        path.append((en,x[en][2]))
        path.reverse()
        return path'''
                
        
        
            

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
