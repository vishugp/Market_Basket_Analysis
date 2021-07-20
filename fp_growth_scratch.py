class Node:
    def __init__(self, item_name = None,parent=None ,item_count = 0,link=None):
        self.name = item_name
        self.count = item_count
        self.link = link
        self.parent = parent
        self.children = {}
        

class FPtree:
    def __init__(self,data,minsup):
        self.data = data
        self.minsup = minsup
        
        self.root = Node(item_name="NULL")
        
        
        self.item_dict = {}
        self.item_dict_sort = {}
        self.item_order = {}
        self.heads_table = []
        self.item_row_sort = []
        self.construct(data)
#         self.cond_tree_tran()
        
    def construct(self, data):
        for transaction in data:
            for item in transaction:
                if item in self.item_dict.keys():
                    self.item_dict[item]+=1
                else:
                    self.item_dict[item]=1
        
        itemlist = list(self.item_dict.keys())
        
        ## Deleting Items with lesser supportcount than minsup
        for items in itemlist:
            if self.item_dict[item]<self.minsup:
                del self.item_dict[item]
        
        self.item_dict_sort = dict(sorted(self.item_dict.items(), key=lambda x: x[1], reverse = True))
#         print(self.item_dict_sort)
        
        ## Node Head Linkage Table
        rank = 0
        for i in self.item_dict_sort:
#             print(i)
            item = i
            count = self.item_dict_sort[i]
            self.item_order[item] = rank
            rank+=1
            
            item_info = {'item_name':item,
                        'item_count':count,
                        'link_node':None}
            
            self.heads_table.append(item_info)
            print(item_info)

            
        ## Starting to Build the Trie
        for transaction in data:
            itemsup = []
            for item in transaction:
                if item in self.item_dict.keys():
                    itemsup.append(item)
            
            if len(itemsup)>0:
                sorted_row = sorted(itemsup, key=lambda k: self.item_dict_sort[k],reverse=True)
                self.item_row_sort.append(sorted_row)
#                 print(self.item_row_sort)
                
                node = self.root
                print(sorted_row)
                
                for i in sorted_row:
                                    
                    if i in node.children.keys():
                        node.children[i].count+=1
                        node = node.children[i]
                    else:
                        node.children[i] = Node(item_name=i,item_count=1,parent=node, link=None)
                        node = node.children[i]
                        
                        for item_info in self.heads_table:
                            if item_info["item_name"] == node.item:
                                if item_info["link_node"] is None:
                                    item_info["link_node"] = node
                                else:
                                    iter_node = item_info["link_node"]
                                    while(iter_node.link is not None):
                                        iter_node = iter_node.link
                                    iter_node.link = node
                                    
                        
    def print_table(self):
        for row in self.heads_table:
            print("\nITEM NAME: {}".format(row["item_name"]))
            print("ITEM COUNT: {}".format(row["item_count"]))
            i=0
            print("NODE CHILDREN:-")
            dummy_node = row["link_node"]
            while(dummy_node.link is not None):
                print("{}) {}".format(i,dummy_node.link))
                dummy_node = dummy_node.link
                i+=1
                
    def cond_tree_tran (self,node):
        if node.parent is None:
            return None
        
        cond_tree = []
        while node is not None:
            tran = []
            node_parent = node.parent
            while node_parent.parent is not None:
                tran.append(node_parent.item)
                node_parent = node_parent.parent
            
            #reverse order
            tran = tran[::-1]
#             for i in range(node.count):
            cond_tree.append({tran:node.count})
            #move to next linknode
            node = node.link
        print(node.item,cond_tree)
        return cond_tree
    
    def find_fqt(self, parent_node = None):
        if len(list(self.root.children.keys()))==0:
            return None
        result = []
        sup = self.minsup
        
        revtable = self.heads_table[::-1]
        for n in revtable:
            fqset = [set(),0]
            
            if (parent_node == None):
                fqset[0] = {n['item_name'],}
            else:
                fqset[0] = {n['item_name']}.union(parent_node[0])
            
            fqset[1] = n['item_count']
            result.append(fqset)
            cond_tran = self.cond_tree_tran(n['link_node'])
            
            cond_tree = FPtree(cond_tran, sup)
            cond_items = cond_tree.find_fqt(fqset)
            
            if cond_items is not None:
                for items in cond_items:
                    result.append(items)
        
        return result
    
#check if tree hight is larger than 1 
    def checkheight(self):
        if len(list(self.root.children.keys()))==0:
            return False
        else:
            return True    
        
