from integer_container import IntegerContainer


class IntegerContainerImpl(IntegerContainer):

    def __init__(self):
        # TODO: implement
        self.arr=[]

    # TODO: implement interface methods here
    def add(self,value: int) -> int:
        self.arr.append(value)
        return len(self.arr)
        
    def delete(self,value: int) -> int:
        if value in self.arr :
            self.arr.remove(value)
            return True
        return False
            
        
        
