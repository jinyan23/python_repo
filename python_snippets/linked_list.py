# %%
# List of nodes linked together

class Node():
    
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data

class LinkedList():
    
    # init: class object initialization
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            
            # Pops upon assignment (inplace)
            node = Node(data=nodes.pop(0))      
            self.head = node
            
            for elem in nodes:
                
                # Point to next node
                node.next = Node(data=elem)     
                
                # Reassign current node
                node = node.next                
    
    
    # method: Add node to the beginning of linked list
    def add_first(self, node):
        node.next = self.head
        self.head = node
        
    # method: Add node to the end of linked list
    def add_last(self, node):
        if self.head is None:
            self.head = node
            return
        for current_node in self:
            pass
        current_node.next = node
    
    # method: Add node before target node
    def add_before(self, target_node_data, new_node):
        if self.head is None:
            raise Exception("Linked list is empty.")
        
        # If adding before first node in list, use add_first()
        if self.head.data == target_node_data:
            return self.add_first(new_node)
        
        
        prev_node = self.head
        for node in self:
            if node.data == target_node_data:
                prev_node.next = new_node
                new_node.next = node
                return
            prev_node = node
        
        raise Exception("Node with data '%s' not found." % target_node_data)

    # method: Add node after target node
    def add_after(self, target_node_data, new_node):
        
        if self.head is None:
            raise Exception("Linked list is empty.")
        
        for node in self:
            if node.data == target_node_data:
                new_node.next = node.next
                node.next = new_node
                return
        
        raise Exception("Node with data '%s' not found." % target_node_data)
            
    # method: Print node Nth position from last node
    def printNthFromLast(self, N):
        
        length_of_list = self.__len__()
        
        node = self.head
        for i in range(0, length_of_list - N):
            node = node.next
        
        return node.data
    
    
    # attr: Convert linked list into a iterable 
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next
    
    # attr: Get the length of linked list
    def __len__(self):
        length = 0
        
        # Make use of the defined __iter__
        for current_node in self:
            length += 1
        return length
         
    # attr: String representation of class object
    def __repr__(self):
        
        node = self.head
        nodes = []
        
        while node is not None:
            
            # Append node to list
            nodes.append(node.data)
            
            # Moves to the next node
            node = node.next
            
        nodes.append("None")
        
        return " -> ".join(str(n) for n in nodes)

