import numpy as np
class Graph:
    def __init__(self,src_file):
        self.src_file=src_file
        self.placeholder=None
    def readFile(self):
        with open(self.src_file,'r') as fRead:
            lines=fRead.readlines()
            return lines
    def onSplitAndCount(self,lines):
        array=[line[line.find("A"):line.find("\n")].rsplit("=>") for line in lines if (line.find("NULL_PATH")==-1) and (line.find("Frame") == -1)]
        count=[array.count(array[item]) for item in range(len(array))]
        return array,count
    def onAppend(self,array,count):
        size=max([len(item) for item in array])+1
        for part in array:
            for i in range(len(part),size):
                part.append(self.placeholder)
        array,count=np.array(array),np.array(count)
        array[:,-1]=count[:]
        return array.tolist()
    def onDuplicateRemoval(self,array):
        removalArray=[]
        for item in array:
            if item not in removalArray:
                removalArray.append(item)
        return np.array(removalArray)

    def onSplitStartAndEnd(self,ndArray):
        end_set=set(ndArray[:,ndArray.shape[1]-2])
        placeholder_set=set([self.placeholder])
        start,end=ndArray[0,0],(end_set-placeholder_set).pop()
        return start,end,ndArray
    def generateKeys(self,start,end,ndArray):
        key_set=set(ndArray[:,:ndArray.shape[1]-2].flatten())
        key_set.remove(self.placeholder)
        key_set=key_set.difference(set([start,end]))
        key_array=list(key_set)
        key_array=key_array[::-1]
        key_array.append(start)
        key_array=key_array[::-1]
        key_array.append(end)
        key_array.append('weight')
        return key_array
    def generateMatrix(self,keyArray,originalArray):
        matrix=np.zeros((originalArray.shape[0],len(keyArray)),dtype=np.int64)
        matrix[:,matrix.shape[1]-1]=originalArray[:,originalArray.shape[1]-1]
        adjacencyMatrix=np.zeros((matrix.shape[1]-1,matrix.shape[1]-1),dtype=np.int64)

        for bunch in range(originalArray.shape[0]):
            order=1
            sequence=[]
            for node in originalArray[bunch]:
                try:
                    index=keyArray.index(node)
                except Exception as e:
                    index=None
                finally:
                    if index!=None:
                        sequence.append(index)
                        matrix[bunch,index]=order
                        order+=1
            sequence.sort()
            for i in range(len(sequence)-1):
                adjacencyMatrix[sequence[i],sequence[i+1]]=1
            del sequence
        return matrix,adjacencyMatrix

    def calcLeastMatrix(self,adjacencyMatrix):
        originalMatrix=adjacencyMatrix
        path=-1*np.ones((originalMatrix.shape[0],originalMatrix.shape[1]),dtype=np.int64)
        for k in range(0,originalMatrix.shape[0]):
            for i in range(0,originalMatrix.shape[0]):
                for j in range(0,originalMatrix.shape[1]):
                    if originalMatrix[i,j]>(originalMatrix[i,k]+originalMatrix[k,j]):
                        originalMatrix[i,j]=originalMatrix[i,k]+originalMatrix[k,j]
                        path[i,j]=k
        return originalMatrix,path


    def onMapping(self):
        lines=self.readFile()
        array,count=self.onSplitAndCount(lines)
        array=self.onAppend(array,count)
        array=self.onDuplicateRemoval(array)
        start,end,main_array=self.onSplitStartAndEnd(array)
        key_array=self.generateKeys(start,end,main_array)
        matrix,adjacencyMatrix=self.generateMatrix(key_array,main_array)
        print(main_array)
        least,least_path=self.calcLeastMatrix(adjacencyMatrix)
        if least.any() or least_path.any():
            return least,least_path
        else:
            return False

if __name__=='__main__':
    graph=Graph('./PSNPath-A_V4-A_Q27.frame')
    matrix,adjacencyMatrix=graph.onMapping()
    print(matrix)
    print(adjacencyMatrix)