import typing
import factory
import reader
import sys

def main():
    if len(sys.argv)<3:
        print("Error, arguments not given correctly.\nCorrect Syntax: python main.py <path to yaml file> <name of game>")
        exit(1)
    path=sys.argv[1]
    name=sys.argv[2]
    data=reader.get_data_from_yaml(path)
    if not data[name] or len(data[name])!=2:
        raise Exception(f"The game \'{name}\' was not found in the given yaml file")

    print(solve(path,name,data))


def solve(path:str, name:str,data)->str:
    if "game" not in data[name][1]:
        raise Exception("Error, game data not found")
    if "number_of_cells" not in data[name][0]:
        raise Exception("Error, number_of_cells property not found")

    game=list(map(lambda x:factory.type_factory(x), data[name][1]["game"]))
    num_of_elements=data[name][0]["number_of_cells"]-1

    if not isinstance(game[num_of_elements-1],factory.Princess):
        raise Exception("Error, no Princess on last cell")

    stack=[]
    ans = []
    max_sum_of_gold= -1

    # This function will use a stack to check possible options in the game, and add valid option to the answer array
    # at the end of running this function, the ans array should contain all options with a maximal amount of gold, and the dragons required to kill to reach said option
    def play(sum_of_gold:int,i:int)->None:
        nonlocal ans
        nonlocal max_sum_of_gold

        if i >= num_of_elements:
            return
        if i==num_of_elements-1 and isinstance(game[i],factory.Princess) and typing.cast(factory.Princess,game[i]).can_marry(len(stack)):
            if sum_of_gold==max_sum_of_gold:
                ans.append(stack.copy())
            elif sum_of_gold>max_sum_of_gold:
                max_sum_of_gold=sum_of_gold
                ans=[stack.copy()]
        elif isinstance(game[i],factory.Princess) and not typing.cast(factory.Princess,game[i]).can_marry(len(stack)):
            play(sum_of_gold,i+1)
        elif isinstance(game[i],factory.Dragon):
            stack.append(i)
            # Check the option of killing the dragon
            play(sum_of_gold+typing.cast(factory.Dragon,game[i]).gold,i+1)
            stack.pop()
            # Check the option of not killing the dragon
            play(sum_of_gold,i+1)

    play(0,0)
    if not ans:
        return "-1"
    else:
        output=printer(ans,max_sum_of_gold)
        return output

def printer(options:list[list[int]],sum)->str:
    ans=[]
    for option in options:
        ans.append(str(sum))
        ans.append(str(len(option)))

        dragons_to_kill=[]
        for i in option:
            dragons_to_kill.append(str(i+2))
        ans.append(" ".join(dragons_to_kill))
        ans.append("\n")
    return "\n".join(ans[:len(ans)-1])

if __name__ == "__main__":
    main()
