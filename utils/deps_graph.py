#Project imports
from em.base_classes.registrable import Registrable

#As things are right now, this is kind of overkill,
#but I wanted to make sure that the code was easily expandable
class DepsGraph:
    class Node:
        def __init__(self, _cls):
            self.cls = _cls
            self.edges = {
                #The ones which cls depends on
                'incoming': set(),
                #The ones that depend on cls
                'outgoing': set()
            }
            self.incoming = self.edges['incoming']
            self.outgoing = self.edges['outgoing']
        
        #Syntatic sugar for building a root node for classes without dependencies
        #Having said node allows for easy access to these classes
        @classmethod
        def RootNode(cls):
            return cls(None)

    #__init__ will only consider base classes that are derived from Registrable
    #No two classes should be named equally
    #Improper graphs (circular dependencies) will crash the code
    def __init__(self, classes):

        #Naming seems weird here, because you expect the root to be part of the graph,
        #but you should think of the instance of the DepsGraph class as the actual graph,
        #these are just variable names. 
        self.root = self.Node.RootNode()
        self.graph = {}

        for _cls in classes:
            class_name = _cls.__name__
            node = self.try_set(class_name, _cls)
            bases = [base for base in _cls.__bases__ if Registrable in base.__bases__]
            node.incoming = set([base.__name__ for base in bases])
            
            #If there aren't any base classes, then we say our class 'depends'
            #on 'the root class' (which doesn't exist). We could add None to incoming
            #for consistency but it would be a waste of time.
            if not bases:
                self.root.outgoing.add(class_name)

            for base in bases:
                base_name = base.__name__
                base_node = self.try_set(base_name, base)
                base_node.outgoing.add(class_name)
    
    def try_set(self, class_name, _cls):
        node = None
        if not class_name in self.graph:
            node = self.Node(_cls)
            self.graph[class_name] = node
        if node:
            return node
        return self.graph[class_name]

    #Returns classes in an order suited for registration
    #They should be unregistered in reverse order
    @classmethod
    def Sorted(cls, classes):
        deps_graph = cls(classes)
        
        result = []
        no_dependencies = set(deps_graph.root.outgoing)
        while no_dependencies:
            class_name = no_dependencies.pop()
            class_node = deps_graph.graph[class_name]
            
            for out_name in class_node.outgoing:
                out_node = deps_graph.graph[out_name]
                out_node.incoming.remove(class_name)
                
                if not out_node.incoming:
                    no_dependencies.add(out_name)

            result.append(class_node.cls)
        
        return result