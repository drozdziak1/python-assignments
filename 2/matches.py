#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Stanisław Drozd <drozdziak1@gmail.com>


def player_choose():
    while True:
        choice = int(input("\nEnter 1, 2 or 3 matches to remove: "))
        print('\n')
        if choice in range(1,4):
            return choice

def cpu_choose(matches_left):
    return matches_left % 4 or 1

matches_left = 40

print("There's 40 matches on the table. You and CPU are allowed to remove 1-3\n"
        "matches from the pile each round. The player with no matches left to"
        "take loses!\n")

if (input("Would you like to make the first move? *wink* (Y/n) ") != "n"):
    player_choice = player_choose()
    matches_left -= player_choice
    print("Player: %d, %d left\n" % (player_choice, matches_left))

while matches_left > 0:
    cpu_choice = cpu_choose(matches_left)
    matches_left -= cpu_choice
    print("CPU: %d, %d left" % (cpu_choice, matches_left))

    if matches_left <= 0:
        print("\nCPU wins!")
        exit()

    player_choice = player_choose()
    matches_left -= player_choice
    print("Player: %d, %d left\n" % (player_choice, matches_left))

print("\nPlayer wins!")
