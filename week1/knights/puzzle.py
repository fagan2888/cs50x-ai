from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is either a knight or kave. Cannot be both.
    Or(AKnight, AKnave),
    Biconditional(AKnight, Not(AKnave)),

    # If A is a knight, he is both a knight and knave.
    Implication(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A and B are both either knaves or knights. One cannot be both.
    Or(AKnight, AKnave),
    Biconditional(AKnight, Not(AKnave)),
    Or(BKnight, BKnave),
    Biconditional(BKnight, Not(BKnave)),

    # Iff A is a knight, both are knaves
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A and B are both either knaves or knights. One cannot be both.
    Or(AKnight, AKnave),
    Biconditional(AKnight, Not(AKnave)),
    Or(BKnight, BKnave),
    Biconditional(BKnight, Not(BKnave)),

    # Iff A is a knight, A & B are the same kind. 
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # Iff B is a knight, A & B are different kinds.
    Biconditional(BKnight, Or(And(AKnight, Not(BKnight)), And(AKnave, Not(BKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A, B, and C are all either knaves or knights. One cannot be both.
    Or(AKnight, AKnave),
    Biconditional(AKnight, Not(AKnave)),
    Or(BKnight, BKnave),
    Biconditional(BKnight, Not(BKnave)),
    Or(CKnight, CKnave),
    Biconditional(CKnight, Not(CKnave)),

    # Iff B is a knight and Iff A is a knight, then A is a knave
    Biconditional(And(BKnight, AKnight), AKnave),
    # Iff B is a knight, C is a knave
    Biconditional(BKnight, CKnave),
    # Iff C is a knight, A is a knight
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
