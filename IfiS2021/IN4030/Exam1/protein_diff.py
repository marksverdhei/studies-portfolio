# Non-standard python modules
import pandas as pd

# Standard python modules
import argparse
from typing import List, Tuple
from collections import namedtuple


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_path", type=str, help="path primary to protein sequence in fasta format")
    parser.add_argument("subject_path", type=str, help="path secondary to protein sequence in fasta format")
    parser.add_argument("--substitution_matrix_path", type=str, default="data/BLOSUM62.txt")
    parser.add_argument("-o", "--opening_penalty", type=int, default=11)
    parser.add_argument("-e", "--extension_penalty", type=int, default=1)
    args = parser.parse_args()
    return args


def read_fasta(filename: str):
    with open(filename, "r", encoding="UTF8") as f:
        data = f.read().split("\n")

    meta, content = data[0], "".join(data[1:])
    return meta, content


def load_substitution_matrix(path):
    """
    Requires whitespace delimiter and comment syntax as #
    Should be ok to use pandas here as it is only for loading blosum62.
    There is no mention that we cannot use libraries for loading the matrix
    """
    return pd.read_csv(path, delim_whitespace=True, comment="#")


def argmax(matrix: List[List[float]]) -> Tuple[int, int]:
    "Exhaustively searches for the highest number in a matrix and outputs it's indices"
    m = len(matrix)
    n = len(matrix[0])
    return max(((i, j) for i in range(m) for j in range(n)), key=lambda t: matrix[t[0]][t[1]])


def zero_matrix(n, m):
    return [[0] * n for _ in range(m)]

# Look at https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm
def optimal_alignment(query: str,
                      subject: str,
                      substitution_matrix: pd.DataFrame,
                      extension_penalty: int = 1,
                      opening_penalty: int = 11):
    """
    Computes the optimal alignment between two nucleotide/amino acid sequences
    using the BLOSUM62 scoring matrix

    It uses an affine gap penalty function with gap opening penalty of 11 and gap
    extension penalty of 1.

    V: scoring matrix
    E: insertion matrix
    F: deletion matrix
    G: alignment matrix
    """
    # opening_penalty -= 1
    m = len(query)
    n = len(subject)

    V = zero_matrix(n, m)
    G = zero_matrix(n, m)
    E = zero_matrix(n, m)
    F = zero_matrix(n, m)
    pointer_matrix = [["END"] * n for _ in range(m)]

    for i in range(1, m):
        V[i][0] = -opening_penalty - i * extension_penalty
        E[i][0] = -2*opening_penalty - (1 + i) * extension_penalty
        F[i][0] = -float("inf")


    for j in range(1, n):
        V[0][j] = -opening_penalty - j * extension_penalty
        E[0][j] = -float("inf")
        F[0][j] = -2*opening_penalty - (1 + i) * extension_penalty


    for i, a1 in enumerate(query[1:], start=1):
        for j, a2 in enumerate(subject[1:], start=1):
            G[i][j] = V[i-1][j-1] + substitution_matrix[a1][a2]
            F[i][j] = max(
                F[i-1][j]-extension_penalty,
                V[i-1][j]-opening_penalty-extension_penalty
            )
            E[i][j] = max(
                E[i][j-1]-extension_penalty,
                V[i][j-1]-opening_penalty-extension_penalty
            )

            directions = {
                "DIAG": G[i][j],
                "UP"  : F[i][j],
                "LEFT": E[i][j],
                "END" : 0
            }

            direction, value = max(directions.items(), key=lambda x:x[1])
            V[i][j] = value
            pointer_matrix[i][j] = direction

    i, j = argmax(V)
    max_score = V[i][j]
    direction = pointer_matrix[i][j]

    # Traceback
    align1, align2 = [], []

    while direction != "END" and (i or j):
        direction = pointer_matrix[i][j]
        if direction == "DIAG":
            i -= 1
            j -= 1
            align1.append(query[i])
            align2.append(subject[j])
        elif direction == "UP":
            i -= 1
            align1.append(query[i])
            align2.append("-")
        elif direction == "LEFT":
            j -= 1
            align1.append("-")
            align2.append(subject[j])


    align1 = "".join(reversed(align1))
    align2 = "".join(reversed(align2))

    return max_score, (align1, align2)


def make_alignment_segments(align1, align2, charlim=70):
    assert len(align1) == len(align2)
    length = len(align1)
    connection = "".join("|" if i == j and i != "-" else " " for i, j in zip(align1, align2))

    for i in range(0, length, charlim):
        yield "\n".join((
            f"From {i} to {min(i+charlim, length)}",
            align1[i:i+charlim],
            connection[i:i+charlim],
            align2[i:i+charlim],
            ""
        ))


def main(args) -> None:
    _, query = read_fasta(args.query_path)
    _, subject = read_fasta(args.subject_path)
    print("Length of query:", len(query))
    print("Length of subject:", len(subject))

    substitution_matrix = load_substitution_matrix(args.substitution_matrix_path)

    score, alignments = optimal_alignment(
        query, subject, substitution_matrix,
        extension_penalty=args.extension_penalty,
        opening_penalty=args.opening_penalty
    )

    alignq, aligns = alignments
    print("Score:", score)
    print("Optimal local alignment")
    for s in make_alignment_segments(alignq, aligns):
        print(s)


if __name__ == '__main__':
    args = parse_args()
    main(args)
