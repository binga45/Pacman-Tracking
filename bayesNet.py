# bayesNet.py

import itertools
import util

class CPT():
    """
    A table that represents the conditional probabilities.
    This has two components, the dependencyList and the probTable.
    dependencyList is a list of nodes that the CPT depends on.
    probTable is a table of length 2^n where n is the length of dependencyList.
    It represents the probability values of the truth table created by the dependencyList as the boolean values, in the same order.
    That is to say is the depencyList contains A and B then probTable will have 4 values corresponding to (A, B) = (0, 0), (0, 1), (1, 0), (1, 1) in that order.
    """
    def __init__(self, dependencies, probabilities):
        self.dependencyList = dependencies
        self.probTable = probabilities

class BayesNetwork():
    """
    A network represented as a dictionary of nodes and CPTs
    """
    def __init__(self, network):
        """
        Constructor for the BayesNetwork class. By default it only takes in the network
        Feel free to add things to this if you think they will help.
        """
        self.network = network

        "*** YOUR CODE HERE ***"

    def singleInference(self, A, B):
        """
        Return the probability of A given B using the Bayes Network. Here B is a tuple of (node, boolean).
        """
        "*** YOUR CODE HERE ***"
        return self.enumeration(A,B)
    
    def contains(self, newev, Y):
        counter=0
        for (a,b) in newev:
            if Y == a:
                return True,counter,b
            counter+=1
        
    def enumerateAll(self, dept, newev):
        if(dept is None or len(dept) == 0):
            return 1
        #print(dept)
        Y = dept.pop(0)
        print("Y:",Y)
        Ydep = self.network[Y].dependencyList #parents
        #print(newev)
        Yprob = self.network[Y].probTable
        #print(Yprob)
        result = "" # to construct the bits of the dependent variables.
        print("Ydep",Ydep)
        result = []
        #flag,counter,value = self.contains(newev, Y)
        counter=0
        comp=0
        val = None
        flag = None
        print("newev:",newev)
        for (a,b) in newev: #checking if Y is present in evidence
            if Y == a:
                flag=True
                val = b
                break
            counter+=1
        for temp in Ydep:
            for (dep, value) in newev:
                if dep == temp:
                    result.insert(0,int(value==True))
        for s in range(len(result)):
            comp += pow(2,s)*int(result[s])
        comp = int(comp)
        if flag:
            print(comp)
            if val == True:
                print("prob",Y,":",Yprob[comp])
                tt = Yprob[comp]*self.enumerateAll(dept,newev)
                print("return",Y,":",tt)
                dept.insert(0,Y)
                return tt   
            else:
                if(Y == 'C'): print('hello')
                print("prob",Y,":",1-Yprob[comp])
                tt = (1-Yprob[comp])*self.enumerateAll(dept,newev)
                print("return",Y,":",tt)
                dept.insert(0,Y)
                return tt
        else:
            print(comp)
            print("Yprobin:",Yprob)
            print("newev:", newev)
            newev1 = newev.copy()
            newev2 = newev.copy()
            newev1.append((Y,True))
            newev2.append((Y,False))
            rs1 = Yprob[comp]*self.enumerateAll(dept,newev1)
            print("rs1",Y,":",Yprob[comp])
            print("obsrs1",Y,":",rs1)
            rs2 =  (1-Yprob[comp])*self.enumerateAll(dept,newev2)
            print("dept",Y,":",dept)
            print("newev2",Y,":",newev2)
            print("rs2",Y,":",1-Yprob[comp])
            print("obsrs2",Y,":",rs2)
            dept.insert(0,Y)
            return rs1+rs2
            
    def enumeration(self, A, B):
        q = dict()
        cpt = self.network[A]
        
        dept = list(self.network.keys())
        prob = cpt.probTable
        
        newev = []
        
        newev.append(B)
        newev.append((A,True))
        result = self.enumerateAll(dept,newev)
        #return result
        newev = []
        
        newev.append(B)
        newev.append((A,False))
        temp = self.enumerateAll(dept,newev)
        return result/(result+temp)

    def enumerateAll1(self, dept, newev):
        if(dept is None or len(dept) == 0):
            return 1
        #print(dept)
        Y = dept.pop(0)
        print("Y:",Y)
        Ydep = self.network[Y].dependencyList #parents
        #print(newev)
        Yprob = self.network[Y].probTable
        #print(Yprob)
        result = "" # to construct the bits of the dependent variables.
        print("Ydep",Ydep)
        result = []
        #flag,counter,value = self.contains(newev, Y)
        counter=0
        comp=0
        val = None
        flag = None
        print("newev:",newev)
        for a in range(0,len(newev),2): #checking if Y is present in evidence
            if Y == newev[a]:
                flag=True
                val = newev[a+1]
                break
            counter+=1
        for temp in Ydep:
            #for (dep, value) in newev:
            for a in range(0,len(newev),2):
                if newev[a] == temp:
                    result.insert(0,int(newev[a+1]==True))
        for s in range(len(result)):
            comp += pow(2,s)*int(result[s])
        comp = int(comp)
        if flag:
            print(comp)
            if val == True:
                print("prob",Y,":",Yprob[comp])
                tt = Yprob[comp]*self.enumerateAll1(dept,newev)
                print("return",Y,":",tt)
                dept.insert(0,Y)
                return tt      
            else:
                if(Y == 'C'): print('hello')
                print("prob",Y,":",1-Yprob[comp])
                tt = (1-Yprob[comp])*self.enumerateAll1(dept,newev)
                print("return",Y,":",tt)
                dept.insert(0,Y)
                return tt
        else:
            print(comp)
            print("Yprobin:",Yprob)
            print("newev:", newev)
            newev1 = newev.copy()
            newev2 = newev.copy()
            newev1.append(Y)
            newev1.append(True)
            newev2.append(Y)
            newev2.append(False)
            rs1 = Yprob[comp]*self.enumerateAll1(dept,newev1)
            print("rs1",Y,":",Yprob[comp])
            print("obsrs1",Y,":",rs1)
            rs2 =  (1-Yprob[comp])*self.enumerateAll1(dept,newev2)
            print("dept",Y,":",dept)
            print("newev2",Y,":",newev2)
            print("rs2",Y,":",1-Yprob[comp])
            print("obsrs2",Y,":",rs2)
            dept.insert(0,Y)
            return rs1+rs2

    def multipleInference(self, A, observations):
        """
        Return the probability of A given the list of observations.Observations is a list of tuples.
        """
        "*** YOUR CODE HERE ***"
        #return .2364
        return self.enumeration1(A,observations)
    
    def enumeration1(self, A, observations):
        q = dict()
        cpt = self.network[A]
        
        dept = list(self.network.keys())
        prob = cpt.probTable
        newev = observations.copy()
        newev.append(A)
        newev.append(True)
        result = self.enumerateAll1(dept,newev)
        # if(result == 0.23280000000000003):
        #     return result
        #return result
        newev = observations.copy()
        newev.append(A)
        newev.append(False)
        
        # newev.append(B)
        # newev.append((A,False))
        temp = self.enumerateAll1(dept,newev)
        fin = result/(result+temp)
        print(fin)
        return fin
