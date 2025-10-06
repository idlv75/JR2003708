import yaml
import os
import heapq

path = "adventure.yml"



def read_yaml(path):
    """ reads yaml file and return its content """
    with open(path) as f:
        data = yaml.safe_load(f)
    return data


def create_road_dict(road_yml):
    """receives a list of {character : amount } ,
    returns a list with tuple (resident type, amount in his cell) """
    road = []
    for cell_dict in road_yml:
        resident, amount = list(cell_dict.items())[0]
        road.append((resident, amount))

    return road


class Solution:
    def __init__(self, path):
        self.data_path = os.getenv("YAML_PATH", path)  # try to load env path
        file_data = Solution.read_yaml(self.data_path)
        unprocessed_road = file_data["road"]
        self.length = file_data["length"]
        self.road = Solution.create_road_dict(unprocessed_road)

    @staticmethod
    def read_yaml(data_path):
        """ reads yaml file and return its content """
        with open(data_path) as f:
            data = yaml.safe_load(f)
        return data

    @staticmethod
    def create_road_dict(unprepared_road):

        """receives a list of {character : amount } ,
        returns a list with tuple (resident type, amount in his cell) """
        road = []
        for cell_dict in unprepared_road:
            resident, amount = list(cell_dict.items())[0]
            road.append((resident, amount))
        return road

    def solve(self):
        """
        road: list of ('d', gold) or ('p', beauty); last tile must be a princess.
        Returns maximum gold you can collect while marrying the last princess,
        if not possible return -1
        plus how many dragons ive killed
        plus where i killed the dragons
        """
        if not self.road or self.road[-1][0] != 'p':
            raise ValueError("Last tile must be a princess.")

        dragon_kill_heap = []  # heap (min) of tuple (gold, idx) for dragons kept
        total_gold = 0

        princess_indexes = [i for i in range(len(self.road)) if self.road[i][0] == 'p']  # indexes of the princesses
        limiting_princesses = set(princess_indexes[:-1])  # princesses i dont want to marry (all but last)

        for i in range(len(self.road)):
            resident, amount = self.road[i]
            if resident == 'd':  # dragon
                heapq.heappush(dragon_kill_heap, (amount, i))
                total_gold += amount
            elif resident == 'p':  # princess
                if i in limiting_princesses:
                    cap = amount - 1  # max kill count

                    while len(dragon_kill_heap) > cap:
                        lower_gold = heapq.heappop(dragon_kill_heap)[0]  # removes the dragons with less gold
                        total_gold -= lower_gold
            else:
                raise ValueError("Unknown creature")

        kill_map = sorted(idx[1] for idx in dragon_kill_heap)
        if len(kill_map) < self.road[-1][1]:  # not enough kills for last queen.
            return -1

        print(total_gold)  # max gold
        print(len(kill_map))  # kill count
        print(" ".join(map(str, kill_map)))  # spaced out indexes of dragon killed

        return total_gold


if __name__ == "__main__":
    solution = Solution(path)
    solution.solve()
