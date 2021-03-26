import copy
import graphviz
import itertools
import random
from typing import Iterable


def invert_dictionary(indict: {str: [str]}) -> {str: [str]}:
    '''
    Inverts the input dictionary.

    Example:
    >>> indict = {'evens':[2,4,6,8,10], 'odds':[1,3,5,7,9], 'primes':[2,3,5,7]}
    >>> outdict = invert_dictionary(indict)
    >>> print('\n'.join(map(str, outdict.items())))
    (2, ['evens', 'primes'])
    (4, ['evens'])
    (6, ['evens'])
    (8, ['evens'])
    (10, ['evens'])
    (1, ['odds'])
    (3, ['odds', 'primes'])
    (5, ['odds', 'primes'])
    (7, ['odds', 'primes'])
    (9, ['odds'])

    Parameters:
    - indict: the dictionary to invert.

    Return:
    the inverted dictionary of indict.
    '''
    outdict = {}
    for key, values in indict.items():
        for value in values:
            outdict[value] = outdict.get(value, []) + [key]
    return outdict


def assign_pairs(team_choices: {str: [str]}) -> {str: (str, str)}:
    '''
    Assigns pairs of teams to data structures according to team_choices.

    Parameters:
    - team_choices: contains the choice of data structures for each team.

    Returns:
    An assignment of data structure to a pair of teams.
    '''
    # Set up iteration variables to track:
    # - the paired teams so far
    # - successful pairing in an iteration
    struct_pairs, paired_teams = dict(), set()
    successful_pairing = True
    struct_teams = invert_dictionary(team_choices)
    # Iterate until pairing introduces no change.
    while successful_pairing:
        successful_pairing = False
        # Group teams by their choice of data structure.
        for struct, teams in struct_teams.items():
            # Can't make a pair with 1 team.
            if len(teams) < 2:
                continue
            # Check possible pairs for this structure. Assign the first
            # qualifying pair and move to the next structure.
            for pair in itertools.combinations(teams, 2):
                # Disqualify pair if a contained team is already paired.
                if set(pair) & paired_teams:
                    continue
                # Pair qualified: update variables and do not consider any more
                # pairs.
                struct_pairs[struct] = struct_pairs.get(struct, []) + [pair]
                paired_teams.update(pair)
                successful_pairing = True
                break
    return struct_pairs


##########
# Read student preference data from file.
##########
team_choices: [str] = open('projecttopics.txt').readlines()
team_choices: [str] = [line.strip() for line in team_choices]
team_choices: [[str]] = [line.split() for line in team_choices]
team_choices: {str: [str]} = {team: choices for team, *choices in team_choices}
# POST: a key in team_choices is a team name, the value is a list containing the
# structures that the team has indicated.

##########
# Assign pairs of teams for each data structure as per team choices. Select a
# pairing which covers the most number of teams and data structures.
##########
# PRE: team_choices contains information of all teams.
max_teams = 0
max_structures = 0
max_pairs = []
# Iterate many times.
for _ in range(5000):
    # Shuffle the order of keys in team choices.
    team_choices = list(team_choices.items())
    random.shuffle(team_choices)
    team_choices = dict(team_choices)
    # Get pairings and save if they improve on the number of assigned teams and
    # number of covered data structures so far.
    new_pairs = assign_pairs(team_choices)
    num_teams = 2 * sum(map(len, new_pairs.values()))
    num_structures = len(new_pairs)
    if (num_teams, num_structures) > (max_assigned_teams, max_structures):
        max_teams, max_structures = num_teams, num_structures
        max_pairs = new_pairs
# POST: max_pairs contains the pairings that maximize number of teams and
# covered data structures.

# Output information.
print(f'{max_teams} teams assigned to {max_structures} data structures')
for struct, pairs in max_pairs.items():
    for pair in pairs:
        print(struct, pair[0], pair[1], sep='\t')
