import pandas as pd
import numpy as np
import csv
import sys

users = {}
knn = 10

#Function definition

#analysis string and construct user arrays
#normalize user arrays - normize sum to 1
def nor(raw):
    norm = [float(i)/sum(raw) for i in raw]
    return norm

#convert list to vector
def listToVector(myList):
    myarray = np.asarray(myList)
    return myarray;

#find similiarity through dot product of two arrays
def sim(x,y):
    x = nor(x)
    y = nor(y)
    a = listToVector(x)
    b = listToVector(y)
    return np.inner(a, b)

#find n most similiar vectors
def findKNN(matrix):
    return matrix.sort_values(['sim'],ascending=[0]).head(knn)

file_path = './data/sets/0/test.csv'
count = 0
similiarUsers = {}
user = []
uidInput = ""
if len(sys.argv) == 1:
    print "User ID expected"
    quit
else:
    print 'User inputted:', str(sys.argv[1])
    uidInput = str(sys.argv[1])
    #read in data
    f=csv.reader(open(file_path))
    dt = pd.DataFrame(columns=('pid','uid','r'))
    for row in f:
        count += 1
        if count == 1:
            continue
        else:
            dt.loc[count-1] = [row[0],row[1],row[3]]

    #pivot the table to be a matrix, index is uid and column is pid
    ot = pd.pivot_table(dt,values='r',index=['uid'],columns=['pid'], aggfunc = 'sum').fillna(0)
    if not uidInput in ot.index:
        #if the input parameter, which is uid, doesn't exist in the system
        #meaning is a new user, user array set to normized array with value of 3
        print "New user found: ", uidInput
        ot.loc[str(sys.argv(1))] = 3
    #user selected
    user = ot.ix[uidInput].tolist()
    user = map(int, user)

    #for each user who is not the selected user, calculate its similiarity
    finalMatrix = pd.DataFrame(0, index = ot.index.values, columns = ['sim']);
    for row in ot.iterrows():
        userToCompare = []
        index, data =  row
        if(index == uidInput):
            continue
        userToCompare = map(int,data.tolist())
        finalMatrix.loc[index, 'sim'] = sim(user, userToCompare)
     
    #make sure the similiar user list doesn't contain the original user
    #finalMatrix = finalMatrix[finalMatrix.sim != 0]
    print findKNN(finalMatrix)
        
    
