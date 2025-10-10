#!/usr/bin/env python3
"""
CodeForces Problem #548: Dragons and Princesses
"""

import sys
import yaml
import argparse

class Dragon:
    """Represents a dragon with coins that can be defeated."""
    def __init__(self, index, coins):
        self._index = index
        self._coins = coins

    @property
    def index(self):
        return self._index

    @property
    def coins(self):
        return self._coins

    def __str__(self):
        return f"Dragon, index={self.index}, coins={self.coins}"


class Princess:
    """Represents a princess with beauty level."""
    def __init__(self, index, beauty):
        self._index = index
        self._beauty = beauty

    @property
    def index(self):
        return self._index

    @property
    def beauty(self):
        return self._beauty

    def __str__(self):
        return f"Princess, index={self.index}, beauty={self.beauty}"


class Knight:
    """Represents the player character who fights dragons and saves princesses."""
    def __init__(self, n):
        self._married = False
        self._d_killed = 0
        self._coins = 0
        self._goal_p = n

    @property
    def married(self):
        return self._married

    @property
    def d_killed(self):
        return self._d_killed

    @property
    def coins(self):
        return self._coins

    @property
    def goal_p(self):
        return self._goal_p

    def kill_d(self, d):
        """Add dragon's coins to knight's wealth and increment kill count."""
        self._coins += d.coins
        self._d_killed += 1

    def __str__(self):
        return f"Knight, married={self.married}, dragons killed={self.d_killed}, coins={self.coins}, goal princess={self.goal_p}"


class Solution:
    """Handles the dragon-princess game logic and solution."""
    def __init__(self, input_file):
        self.n = 0
        self.world = []
        self.knight = None
        self.dragons_to_kill = []

        self.build_world_from_yaml(input_file)
        self.status = self.choose_dragons()
        if self.status != -1:
            for d_i in self.dragons_to_kill:
                self.knight.kill_d(self.world[d_i-2])
        self.print_output()

    def print_world(self):
        """Display current state of the world and knight."""
        print("\nWorld State:")
        for being in self.world:
            print(being)
        print(self.knight)

    def choose_dragons(self):
        """Main logic to determine which dragons to kill."""
        i = 0
        last_beauty = -1
        d_section = []

        # world consists of one princess only
        if len(self.world) == 1 and self.world[0].beauty > 0:
            return -1

        while i < len(self.world):
            being = self.world[i]
            if isinstance(being, Princess):
                if d_section and self.handle_section(d_section, last_beauty - being.beauty) == -1:
                    return -1
                last_beauty = being.beauty
                d_section = []
            else:
                d_section.append(being)
            i += 1

        if d_section and self.handle_section(d_section, last_beauty) == -1:
            return -1

        self.world.reverse()
        return 0

    def handle_section(self, d_section, beauty_diff):
        """Handle a section of dragons between princesses."""
        if len(d_section) == beauty_diff:
            self.dragons_to_kill += [d.index for d in d_section] # extend
            return 0
        elif len(d_section) > beauty_diff:
            for _ in range(beauty_diff):
                max_d_index = max(d_section, key=lambda d: d.coins).index
                self.dragons_to_kill.append(max_d_index)
                d_section = [d for d in d_section if d.index != max_d_index]
            return 0
        else:
            return -1

    def load_yaml(self, input_file):
        """Load data from YAML file"""
        try:
            with open(input_file, 'r') as f:
                data = yaml.safe_load(f)
                if not isinstance(data, dict) or 'n' not in data or 'world' not in data:
                    raise ValueError("Invalid YAML input file")
                return data
        except (yaml.YAMLError, FileNotFoundError, ValueError) as e:
            print(f"Error: {str(e)}")
            sys.exit(1)

    def build_world_from_yaml(self, input_file):
        """Initialize game world from input file."""
        data = self.load_yaml(input_file)

        self.n = data['n']
        world = data['world']
        assert type(self.n) == int
        assert self.n - 1 == len(world)

        for i, being in enumerate(world):
            self.add_being(being['type'], being['value'], i)

        self.knight = Knight(self.n)
        self.world.reverse()

    def add_being(self, being_type, worth, i):
        """Add a new being (dragon or princess) to the world."""
        assert type(worth) == int and worth >= 0
        assert being_type in ('d', 'p')

        if being_type == 'd':
            d = Dragon(i+2, worth)
            self.world.append(d)
        else:
            worth = worth-1 if i+2 != self.n else worth
            self.world.append(Princess(i+2, worth))

    def print_output(self):
        """Display final game result."""
        if self.status == -1:
            print(-1)
            return

        kill_indexes = [str(d) for d in self.dragons_to_kill]
        kill_indexes.reverse()
        out_str = f"{self.knight.coins}\n{len(self.dragons_to_kill)}\n{' '.join(kill_indexes)}"
        print(out_str)


def main():
    parser = argparse.ArgumentParser(description='Dragons and Princesses game solver')
    parser.add_argument('input_file', help='Path to YAML input file')
    args = parser.parse_args()

    Solution(args.input_file)


if __name__ == '__main__':
    main()
