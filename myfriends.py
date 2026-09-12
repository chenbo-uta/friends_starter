"""Assignment 1: Friend of a Friend

Please complete these functions, to answer queries given a dataset of
friendship relations, that meet the specifications of the handout
and docstrings below.

Notes:
- you should create and test your own scenarios to fully test your functions, 
  including testing of "edge cases"
"""

from py_friends.friends import Friends

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

def load_pairs(filename):
    """
    Args:
        filename (str): name of input file

    Returns:
        List of pairs, where each pair is a Tuple of two strings

    Notes:
    - Each non-empty line in the input file contains two strings, that
      are separated by one or more space characters.
    - You should remove whitespace characters, and skip over empty input lines.
    """
    list_of_pairs = []
    with open(filename, 'rt') as infile:

# ------------ BEGIN YOUR CODE ------------
    #loop lines and remove end \n, skip empty lines
    #for non-empty lines, use "spaces" as seperate, seperate into two string and save as tuples

        for line in infile:
            if line.strip() != "":
                # split based on one space
                words = line.strip().split(' ')
                persons = []
                for item in words:
                    if item != "":
                        persons.append(item)
                #edge cases: skip not two persons, skip two person the same
                if len(persons) == 2:
                    list_of_pairs.append(tuple(persons))
                else:
                    print(f"line {line.strip()} has more or less than two persons")

   # ------------ END YOUR CODE ------------

    return list_of_pairs 

def make_friends_directory(pairs):
    """Create a directory of persons, for looking up immediate friends

    Args:
        pairs (List[Tuple[str, str]]): list of pairs

    Returns:
        Dict[str, Set] where each key is a person, with value being the set of 
        related persons given in the input list of pairs

    Notes:
    - you should infer from the input that relationships are two-way: 
      if given a pair (x,y), then assume that y is a friend of x, and x is 
      a friend of y
    - no own-relationships: ignore pairs of the form (x, x)
    """
    directory = dict()

    # ------------ BEGIN YOUR CODE ------------
    for pair in pairs:
        #skip if two person same
        if pair[0] == pair[1]:
            continue

        # ensure each person in the pair is in the director, if not, then add
        for person in pair:
            if person not in directory:
                directory[person] = set()

        # add two each other friend set, note set() will remove duplicate automatic
        # so no need to check if already in or not
        directory[pair[1]].add(pair[0])
        directory[pair[0]].add(pair[1])
    

    # ------------ END YOUR CODE ------------

    return directory


def find_all_number_of_friends(my_dir):
    """List every person in the directory by the number of friends each has

    Returns a sorted (in decreasing order by number of friends) list 
    of 2-tuples, where each tuples has the person's name as the first element,
    the the number of friends as the second element.
    """
    friends_list = []

    # ------------ BEGIN YOUR CODE ------------
    # browse the dict and add tuple(name, number) into list
    for person, friends in my_dir.items():
        pp_friend_count = (person,len(friends))
        friends_list.append(pp_friend_count)

    # sort, first based on the number of friends, then based on ASCII order (regardless of upper or lower cases)
    friends_list.sort(key=lambda x: (-x[1],x[0].lower()))

    # ------------ END YOUR CODE ------------

    return friends_list


def make_team_roster(person, my_dir):
    """Returns str encoding of a person's team of friends of friends
    Args:
        person (str): the team leader's name
        my_dir (Dict): dictionary of all relationships

    Returns:
        str of the form 'A_B_D_G' where the underscore '_' is the
        separator character, and the first substring is the 
        team leader's name, i.e. A.  Subsequent unique substrings are 
        friends of A or friends of friends of A, in ASCII order
        and excluding the team leader's name (i.e. A only appears
        as the first substring)

    Notes:
    - Team is drawn from only within two circles of A -- friends of A, plus 
      their immediate friends only
    """
    assert person in my_dir
    label = person

    # ------------ BEGIN YOUR CODE ------------
    friend_circle = set()
    for friend in my_dir[person]:
        friend_circle.add(friend)
        for friend_friend in my_dir[friend]:
            friend_circle.add(friend_friend)
    friend_circle.discard(person)
    friend_circle_lst = list(friend_circle)
    friend_circle_lst.sort(key=lambda x: x.lower())
    for friend in friend_circle_lst:
        label +="_" + friend.upper()

    # ------------ END YOUR CODE ------------

    return label


def find_smallest_team(my_dir):
    """Find team with smallest size, and return its roster label str
    - if ties, return the team roster label that is first in ASCII order
    """
    smallest_teams = []

    # ------------ BEGIN YOUR CODE
    min_team_length = float('inf')
    for person in my_dir:
        #get person's team roster
        team_label = make_team_roster(person,my_dir)

        #calculate team size
        team = team_label.split("_")
        team_size = len(team)

        if team_size < min_team_length:
            smallest_teams.insert(0,team_label)
            min_team_length = team_size
        elif team_size == min_team_length and team_label<smallest_teams[0]:
            smallest_teams.insert(0, team_label)

    # ------------ END YOUR CODE

    return smallest_teams[0] if smallest_teams else ""

def generate_friends(my_dir):
    """
    Args:
        my_dir: friends_dir Dict[str, Set]

    Returns:
        yielding one pair (as a tuple) at a time in ASCII order

    """

    if my_dir:

        # get person and sort, save in persons list
        persons = sorted(my_dir.keys())
        num = -1

        #loop persons list
        for person in persons:
            # get sorted friends list of the person
            friends = sorted(my_dir[person])

            # yield only friend that sort after peron, to avoid (y,x) case
            for friend in friends:
                if friend>person:
                    num +=1
                    yield num,(person,friend)

    return None




if __name__ == '__main__':
    # To run and examine your function calls

    print('\n1. run load_pairs')
    my_pairs = load_pairs('mytest.txt')
    print(my_pairs)

    print('\n2. run make_friends_directory')
    my_dir = make_friends_directory(my_pairs)
    print(my_dir) 

    print('\n3. run find_all_number_of_friends')
    print(find_all_number_of_friends(my_dir))

    print('\n4. run make_team_roster')
    my_person = 'DARTHVADER'   # test with this person as team leader
    team_roster = make_team_roster(my_person, my_dir)
    print(team_roster) 

    print('\n5. run find_smallest_team')
    print(find_smallest_team(my_dir))

    print('\n6. run Friends iterator')
    friends_iterator = Friends(my_dir)
    for num, pair in enumerate(friends_iterator):
        print(num, pair)
        if num == 10:
            break
    # since index 0 we read 11 elements
    print(len(list(friends_iterator)) + num + 1)


    print('\n7. run generate_friends')
    num = 0
    for num,pair in generate_friends(my_dir):
        print(num,pair)
        if num == 10:
            break
    # different to class object, function will restart, so below is not valid
    print(len(list(generate_friends(my_dir))) )
