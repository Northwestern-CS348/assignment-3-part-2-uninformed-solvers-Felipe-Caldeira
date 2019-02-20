from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        #breakpoint() 
        pegs = [[], [], []]
        disks_on_pegs_q = self.kb.kb_ask(parse_input("fact: (on ?d ?p)"))
         

        for disk_peg in disks_on_pegs_q:
            disk = int(disk_peg.bindings_dict["?d"][4])
            peg = int(disk_peg.bindings_dict["?p"][3])
            pegs[peg - 1].append(disk)

        for lst in pegs: lst.sort()
        return tuple(tuple(lst) for lst in pegs)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        disk = movable_statement.terms[0]
        pegX = movable_statement.terms[1]
        pegY = movable_statement.terms[2]


        removed_facts = [
                "fact: (on {} {})".format(disk, pegX),
                "fact: (topmost {} {})".format(pegX, disk)
                ]

        added_facts = [
                "fact: (on {} {})".format(disk, pegY),
                "fact: (topmost {} {})".format(pegY, disk)
                ]

        disk_under_q = self.kb.kb_ask(parse_input("fact: (under ?x {})".format(disk)))
        if disk_under_q:
            disk_under = disk_under_q[0].bindings_dict["?x"]
            removed_facts.append("fact: (under {} {})".format(disk_under, disk))
            added_facts.append("fact: (topmost {} {})".format(pegX, disk_under))
        else:
            added_facts.append("fact: (empty {})".format(pegX))
        
        disk_dest_q = self.kb.kb_ask(parse_input("fact: (topmost {} ?x".format(pegY)))
        if disk_dest_q:
            disk_dest = disk_dest_q[0].bindings_dict["?x"]
            removed_facts.append("fact: (topmost {} {}".format(pegY, disk_dest))
            added_facts.append("fact: (under {} {})".format(disk_dest, disk))
        else:
            removed_facts.append("fact: (empty {})".format(pegY))

        
        for fact in removed_facts: self.kb.kb_retract(parse_input(fact)) 
        for fact in added_facts: self.kb.kb_assert(parse_input(fact)) 


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        rows = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        tiles_in_pos_q = self.kb.kb_ask(parse_input("fact: (pos ?t ?x ?y)"))
        #breakpoint() 
		
        for tile_x_y in tiles_in_pos_q:
            tile = ord(tile_x_y.bindings_dict["?t"][4]) - ord('0')
            x = int(tile_x_y.bindings_dict["?x"][3])
            y = int(tile_x_y.bindings_dict["?y"][3])
            rows[y - 1][x - 1] = tile if tile < 9 else -1

        return tuple(tuple(lst) for lst in rows)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        tile = movable_statement.terms[0]
        x1 = movable_statement.terms[1]
        y1 = movable_statement.terms[2]
        x2 = movable_statement.terms[3]
        y2 = movable_statement.terms[4]


        removed_facts = [
                "fact: (pos {} {} {})".format(tile, x1, y1),
                "fact: (pos {} {} {})".format("empty", x2, y2)
                ]

        added_facts = [
                "fact: (pos {} {} {})".format(tile, x2, y2),
                "fact: (pos {} {} {})".format("empty", x1, y1)
                ]
        
        for fact in removed_facts: self.kb.kb_retract(parse_input(fact)) 
        for fact in added_facts: self.kb.kb_assert(parse_input(fact)) 

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
