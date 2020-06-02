import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    geneData = {
        person: {
            "gene": None,
            "trait": None,
            "parents": None,
            "probability": None
        }
        for person in people
    }

    # Add data to geneData
    for person in people:
        # Add gene count
        if person in one_gene:
            geneData[person]["gene"] = 1
        elif person in two_genes:
            geneData[person]["gene"] = 2
        else:
            geneData[person]["gene"] = 0

        # Add trait
        if person in have_trait:
            geneData[person]["trait"] = True
        else:
            geneData[person]["trait"] = False

        # Add parents if listed, else leave as None
        if people[person]["mother"] != None:
            geneData[person]["parents"] = [
                people[person]["mother"], people[person]["father"]]

    # Compute probabilities
    for person in geneData:
        person = geneData[person]
        # No parents
        if person["parents"] == None:
            person["probability"] = probability_noParent(
                person["gene"], person["trait"])
        # Has parents
        else:
            person["probability"] = probability_withParent(
                geneData, person["parents"], person["gene"], person["trait"])

    # Compute joint probability
    output = 1
    for person in geneData:
        output *= geneData[person]["probability"]

    return output


def probability_noParent(gene_count, have_trait):
    # Probability of having x number of genes * probability of trait status
    return PROBS["gene"][gene_count] * PROBS["trait"][gene_count][have_trait]


def probability_withParent(geneData, parents, gene_count, have_trait):
    # Probability of getting one copy of the gene from mother
    # Number of genes from mother
    m_count = geneData[parents[0]]["gene"]
    if m_count == 0:
        m_prob = PROBS["mutation"]
    elif m_count == 1:
        m_prob = 1/2
    else:
        m_prob = 1 - PROBS["mutation"]

    # Probability of getting one copy of the gene from father
    # Number of genes from father
    f_count = geneData[parents[1]]["gene"]
    if f_count == 0:
        f_prob = PROBS["mutation"]
    elif f_count == 1:
        f_prob = 1/2
    else:
        f_prob = 1 - PROBS["mutation"]

    # Probability of the child having x copies of the gene. Apply conditional probability rules/formulas.
    # ¬A and ¬B : (1 - P(A)) * (1 - P(B))
    if gene_count == 0:  
        gene_prob = (1 - m_prob) * (1 - f_prob)
    # XOR : (P(A) ||  P(B)) && ¬(P(A) && P(B))
    elif gene_count == 1:
        gene_prob = (m_prob + f_prob - (m_prob * f_prob)) * (1 - (m_prob * f_prob))
    # and : P(A) * P(B)  
    else:
        gene_prob = m_prob * f_prob

    # Probability of trait status
    trait_prob = PROBS["trait"][gene_count][have_trait]

    return gene_prob * trait_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # Update gene
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        # Update trait
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        person = probabilities[person]

        # Normalize gene probabilities
        sum = 0
        for value in person["gene"]:
            sum += person["gene"][value]
        for value in person["gene"]:
            person["gene"][value] /= sum
        
        # Normalize trait probabilities
        sum = 0
        for value in person["trait"]:
            sum += person["trait"][value]
        for value in person["trait"]:
            person["trait"][value] /= sum


if __name__ == "__main__":
    main()
