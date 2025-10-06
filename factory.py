class Princess:
    def __init__(self,beauty:int) -> None:
        if not isinstance(beauty, (int, float)):
            raise Exception(f"bad input for princesse's beauty, should be a number but instead it is \"{beauty}\" ")
        elif beauty<0:
            raise Exception(f"bad input, received negative princess beauty value:{beauty}")
        self.beauty=beauty

    def can_marry(self,knights_gold:int)->bool:
        return self.beauty<=knights_gold

    def __str__(self):
        return f"Princess(beauty={self.beauty})"

class Dragon:
    def __init__(self,gold:int) -> None:
        if not isinstance(gold, (int, float)):
            raise Exception(f"bad input for dragons's gold, should be a number but instead it is \"{gold}\" ")
        elif gold<0:
            raise Exception(f"bad input, received negative dragon gold value:{gold}")
        self.gold=gold

    def __str__(self):
        return f"Dragon(gold={self.gold})"

def type_factory(input:str) -> Princess|Dragon|None:
    if not input:
        raise Exception("Empty input not allowed")
    input_args=input.split()
    if len(input_args)!=2:
        raise Exception("A cell must contain 2 arguments")
    if input_args[0]=='p':
        return Princess(int(input_args[1]))
    elif input_args[0]=='d':
        return Dragon(int(input_args[1]))
    else:
        raise Exception(f"Invalid Type:\"{input_args[0]}\"")


        
        
