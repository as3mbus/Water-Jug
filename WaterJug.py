"""
Universal Solution To WaterJug Problem.
"""

class WaterJug:

    def __init__(self,fileptr): #constructor
        self.num=int(fileptr.readline()) #number of glass
        self.vol=[]
        self.states=[]
        self.aim=[] #goal state
        self.connecter=' '
        volstr=fileptr.readline()[:-1] #read start state

        for i in volstr:
            if(i!=" "):
                self.vol.append(int(i)) #assign vol of each glass
                self.states.append(0) #assign state of 0 to each glass

        self.aim=fileptr.readline()[:-1] #assign goal state

        self.startState=self.joinStates(self.states,self.connecter) # make string with start state "0 0"
        self.mem={self.startState:[]} #make dictionary with keys "0 0" with value empty array
        self.bestPath=[] #make empty array for best state

        self.compleetSearch()

    def findSuccessfullPaths(self,path):
        #print path
        if path[-1]==self.aim and (len(path)<=len(self.bestPath) or len(self.bestPath)==0): #if current path edge is the target and current path is shorter than best path or the best path is still empty
            print path; #print path
            self.bestPath=path[:] #assign best path to current path
        else:
            for each in self.mem[path[-1]]:  # iterate through state from end to start
                if each not in path and (len(path)<=len(self.bestPath) or len(self.bestPath)==0) : #if state not in path and path length is shorter than best path or best path length is 0
                    path.append(each) #add state to path
                    self.findSuccessfullPaths(path) #reccursive
                    path.pop() #pop

    def performOperation(self,cur_stat,stat): #add stat to mem dictionary
        self.mem[cur_stat].append(self.joinStates(stat,self.connecter)) #add new stat in mem[cur_stat]
        statstr=self.joinStates(stat,self.connecter) #create string with "new stat"
        if statstr not in self.mem[cur_stat]: #if statstr is not in memory current stat keys add it
            self.mem[cur_stat].append(statstr)
        if statstr not in self.mem: #if there r no key with name statstr make new key with it having empty array
            self.mem[statstr]=[]

    def compleetSearch(self): #search all possible state
        cur_stat=self.joinStates(self.states,self.connecter) # make string of "0 0"
        for i in range(0,self.num): # iterate through glass (0 ~ number of glass -1)
            #print i
            if self.states[i]==0: #if glass i is empty (Rule 1 & 2)
                stat=self.states[:] # copy string
                stat[i]=self.vol[i] # fill glass i to the brim (vol[i])
                self.performOperation(cur_stat,stat)

            elif self.states[i]==self.vol[i]: #if glass i is full (Rule 3 & 4)
               stat=self.states[:] #
               stat[i]=0 #empty glass i
               self.performOperation(cur_stat,stat) #add new stat to mem

            for j in range(0,self.num): #iterate again through glasses
                if self.states[i]!=0 and i!=j and self.states[j]<self.vol[j]: #if glass i not empty and i != j and glass j is not full
                    stat=self.states[:] #
                    volChg=self.vol[j]-stat[j] #calculate how many volume to fill glass j
                    if volChg<=stat[i]:  #if current glass i volume bigger or equal the volume to fill glass j
                        stat[j]+=volChg  #fill up glass j with content of glass i
                        stat[i]-=volChg  #reduce glass i content to fill glass j
                    else:
                        stat[j]+=stat[i] #fill glass j with glass i content
                        stat[i]=0        #fill it till glass i is emptied out

                    self.performOperation(cur_stat,stat) #add new stat to mem

        for elment in self.mem[cur_stat]: #iterate through child of key current stat
            if self.mem[elment]==[]: #if mem with key "elmt" doesnt hav any value
                self.states=self.splitStates(elment,self.connecter) #reassign glass state
                self.compleetSearch() #re search

    def splitStates(self,elment,elm): #split state to list of glass state
        tmplst=[]
        for i in elment.split(self.connecter): #split to glass state
            tmplst.append(int(i))  #append glass state

        return tmplst #return glass state

    def joinStates(self,stat,elm): #combine state list to become a string containing glass state's
        st=[]
        for each in stat:
            st.append(str(each)) #add stat element (string) in array

        return self.connecter.join(st)  #return string with each item separated by self.connecter " "


if __name__=="__main__": #jika python script is being run. not imported
    fileptr=open("more_sample_io/WaterJug5.in",'r') #open file to read
    outptr=open("more_sample_io/WaterJug5.out",'w') #open file to write
    N=int(fileptr.readline()) #read line 1 Test count
    for i in range(0,N): #for eeach test
        store=WaterJug(fileptr)  #do stuff in function
        store.compleetSearch()
        print "Sorted Breadth first:",store.mem #print all possible state and state change
    #print "all Successfull Paths:"
        store.findSuccessfullPaths([store.startState]) # find best state
        outptr.write("Case "+str(i)+":"+str(store.bestPath)+'\n') #write best state to file
