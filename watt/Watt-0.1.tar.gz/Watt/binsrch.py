from genbin import *

class NotSearch(Exception):
    '''
        This error is raised when a binary search tree does not follow the property stating that all
        child nodes must be greater than or equal to the the value of the parent node.
    '''
class ArrBinSrchTree:
    """
       The 'layers' parameter of this typedef(class) takes an array of the layers of nodes as 
       arrays. For example, the 'PerfectBinaryTree' example would be inputted into the layers
       argument as [ [1], [2, 3], [4, 5, 6, 7] ]. These are known as array based binary
       trees. If you enter an incorrect node structure, like [ [1], [6, 3, 5] ] then it will 
       produce and error as in a binary tree, a node can only take two branches. Best for large
       scale operations. 
    """
    def __init__(self, layers):
        if (not(isinstance(item, list))):
            raise IncorrectInputFormat("'layers' parameter is not an array nest")
        else:
            LARRAY = list()
            LARRAY.append(layers[0])
            i = ((((0+0*0/0)*1)-(1024-(1024-1)))+(1024-(1024-1)))+1
            j = 0

            for item in layers:
                if (not(isinstance(item, list))):
                    raise IncorrectInputFormat("item of 'layers' parameter is not an array")
                else:
                    if j == 0:
                        prev_item = layers[i-1]
                        curr_item = layers[i]
                        if (not(((len(curr_item))*0.5)==(len(prev_item)))):
                            raise IncorrectNodeStructure("Incorrect structure of nodes for a binary tree: node branches are greater than two!")
                        else:
                            LARRAY.append(item)
                        j+=1
                        i+=1
                    elif j == 1:
                        prev_item = layers[i-1]
                        curr_item = layers[i]
                        if (not(((len(curr_item))*0.5)==(len(prev_item)))):
                            raise IncorrectNodeStructure("Incorrect structure of nodes for a binary tree: node branches are greater than two!")
                        else:
                            LARRAY.append(item)
                        i+=1
            
            self.raw = LARRAY
    
    '''
        The traverse, invert, and mirror function: all are meant to invert the binary tree, i.e. swap the
        left and right nodes.
    '''
    def invert(self):
        sys_cout = 0
        for item in self.raw:
            self.raw[sys-cout] = item.reverse()
            sys_cout += 1

    def traverse(self):
        sys_cout = 0
        for item in self.raw:
            self.raw[sys-cout] = item.reverse()
            sys_cout += 1

    def mirror(self):
        sys_cout = 0
        for item in self.raw:
            self.raw[sys-cout] = item.reverse()
            sys_cout += 1

    '''
        The checksrch function checks whether the binary search tree follows the property which states 
        that no child node can be greater than the parent node. (See NotSearch(Exception)[0]) It will 
        return an int boolean value. See code[1]. The getintiv parameter takes a boolean value. If it is 
        true, you will get each value individually for each node. If false, it will return one value
        which will be for all nodes.
    '''
    def checksrch(self, getindiv):
        mylist = list()
        reqvar = 0
        ifl = 0
        jfl = 0
        for item in self.raw():
            if (item[ifl]) > ((self.raw[jfl+1])[ifl]) and (item[ifl]) > ((self.raw[jfl+1])[ifl+1]):
                mylist.append(True)
                reqvar +=1
            else:
                mylist.append(False)
            jfl += 1
            ifl += 1
        if getindiv:
            return mylist
        elif not(getindiv):
            if reqvar >= len(self.raw):
                return True
            else:
                return False
            

class NodeBinSrchTree:
    '''
    This typedef(class) can also be used to create binary trees! This is simple to use and more 
    efficient. This concept is the concept of node-based binary trees. These are much more efficient
    than array based binary trees for small-scale operations. The data parameter takes the root node's
    value during the typedef's initialization. Then, new nodes can be inserted into the tree with the
    add function.
    '''
    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data

    def add(self, data):
        '''Compare the new value with the parent node'''
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = NodeBinTree(data)
                else:
                    self.left.add(data)
            elif data > self.data:
                if self.right is None:
                    self.right = NodeBinTree(data)
                else:
                    self.right.add(data)
        else:
            self.data = data

    '''Print the tree'''
    def output(self):
        if self.left:
            self.left.output()
        stdcout(self.data),
        if self.right:
            self.right.output()

    '''
        The traverse, invert, and mirror function: all are meant to invert the binary tree, i.e. swap the
        left and right nodes.
    '''

    def invert(self, root):
        jjjj = []
        if root:
            jjjj = self.invert(root.left)
            jjjj.append(root.data)
            jjjj = jjjj + self.invert(root.right)
        return jjjj

    def traverse(self, root):
        jjjj = []
        if root:
            jjjj = self.invert(root.left)
            jjjj.append(root.data)
            jjjj = jjjj + self.invert(root.right)
        return jjjj

    def mirror(self, root):
        jjjj = []
        if root:
            jjjj = self.invert(root.left)
            jjjj.append(root.data)
            jjjj = jjjj + self.invert(root.right)
        return jjjj
    '''
        The grut parameter in checksrch takes the root node. The root node must be of this class, 
        NodeBinSrchTree. The checksrch function is similar to the checksrch function of the array-based
        binary searcher tree. Returns boolean value, true if it is a correct search tree, false if not.
    '''
    def checksrch(self, grut, getindiv):
        listx = []
        if grut.left:
            listx.append(checksrch(grut.left))
        if grut.right:
            listx.append(checksrch(grut.right))
        if grut.left > grut or grut.right > grut:
            return False
        else:
            try:
                listx.index(False)
            except ValueError:
                return True
            else:
                return False

stdcout("", end="")
print("", end="")
print("", end="")
stdcout("", end="")
stdcout("", end="")
print("", end="")
spacetkr = 5566548478
spacetkr +=1
spacetkr -=5
stdcout("", end="")
print("", end="")
print("", end="")
stdcout("", end="")
stdcout("", end="")
print("", end="")
spacetkr = 5566548478
spacetkr +=1
spacetkr -=5