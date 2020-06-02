import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 1000000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Iterate over all pages and add to output dict
    output = {}
    for page1 in corpus:
        output[page1] = 0

    # Probability per page for all pages that it will be randomly picked as per the dampening factor
    prob_random = (1 - damping_factor) / len(corpus)
    for page1 in corpus:
        output[page1] += prob_random

    # Probability per page for linked pages it will be picked
    if len(corpus[page]) != 0:
        prob_linked = damping_factor / len(corpus[page])
        # Iterate over linked pages
        for linkedpage in corpus[page]:
            output[linkedpage] += prob_linked

    # Normalize outputs
    # Get sum of all rank values in output
    sum = 0
    for page1 in output:
        sum += output[page1]
    # Divide all rank values in output by the sum to normalize
    for page1 in output:
        output[page1] /= sum
    
    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Create copy of corpus called output to store pageranks
    output = {}
    for page in corpus:
        output[page] = 0

    # Pick first page at random and increment pagerank
    page = random.choice(list(corpus))
    output[page] += 1

    # Loop n times. Each time pick new page based on transition model and increment pagerank
    for _ in range(n):
        # Pick next page using a random weighted method
        model = transition_model(corpus, page, damping_factor)
        pages = []
        weights = []
        for page in model:
            pages.append(page)
            weights.append(model[page])
        page = random.choices(pages, weights)
        page = page[0]
        output[page] += 1
    
    # Normalize outputs
    # Get sum of all rank values in output
    sum = 0
    for page in output:
        sum += output[page]
    # Divide all rank values in output by the sum to normalize
    for page in output:
        output[page] /= sum
    
    return output


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Create a copy of corpus with empty values to store pageranks
    pageRanks = {}
    for page1 in corpus:
        pageRanks[page1] = 1 / len(corpus)

    d = damping_factor
    n = len(corpus)

    # Create dict of pages to keep track of when each pagerank value changes by less than 0.001
    pageRanks_change = {}
    for p in pageRanks:
        pageRanks_change[p] = 0

    flag = True
    change = float("inf")
    while flag:
        for p in pageRanks:
            if change <= 0.001:
                pageRanks_change[p] = 1

            if all(c == 1 for c in pageRanks_change.values()):
                flag = False

            sigma = 0
            for i in link_sources(corpus, p):
                sigma += pageRanks[i] / numLinks(corpus, i)

            old_pageRank = pageRanks[p]

            pageRanks[p] = (1-d)/n + d * sigma

            change = abs(old_pageRank - pageRanks[p])

    # Normalize outputs
    # Get sum of all rank values in output
    sum = 0
    for page in pageRanks:
        sum += pageRanks[page]
    # Divide all rank values in output by the sum to normalize
    for page in pageRanks:
        pageRanks[page] /= sum

    return pageRanks


def link_sources(corpus, p):
    # Create a list of all pages i that point to page p
    link_sources = []
    # Iterate over all pages i within corpus
    for i in corpus:
        # If page p linked to by page i, add to link_sources
        if p in corpus[i]:
            link_sources.append(i)
    
    return link_sources


def numLinks(corpus, i):
    # If page has no links, return count of all links
    if len(corpus[i]) == 0:
        return len(corpus)

    return len(corpus[i])


if __name__ == "__main__":
    main()
