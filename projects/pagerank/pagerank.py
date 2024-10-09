import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


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
    current = corpus[page]
    res = {}
    
    rest = 1 - damping_factor
    for_each = rest / len(corpus.keys())

    for key in corpus.keys():
        res[key] = for_each

    if len(current) > 0:
        for_under_current = damping_factor / len(current)

        for p in current:
            res[p] += for_under_current

    return res


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    current_page = random.choice([key for key in corpus.keys()])
    samples_res = {}

    for key in corpus.keys():
        samples_res[key] = 0.00

    for _ in range(n):
        sample = transition_model(corpus, current_page, damping_factor)
        new_page = random.choices([key for key in sample.keys()], [v for v in sample.values()])[0]
        current_page = new_page
        samples_res[new_page] += round(1 / n, 4)

    total = 0

    for v in samples_res.values():
        total += v

    return samples_res


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    keys = corpus.keys()
    n = len(corpus)
    res = {}
    done = set()
    i = 0

    for key in keys:
        res[key] = 1 / n

    while True:
        if len(done) == len(keys):
            break

        new = {}
        for key in keys:
            if key in done:
                continue

            pages = []

            for pkey in keys:
                p = corpus[pkey]
                if key in p or len(p) == 0:
                    pages.append(pkey)

            v = 0.00

            for p in pages:
                l = len(corpus[p])
                if l == 0:
                    l = n
                v += (res[p] / l)

            v = damping_factor * v
            v = ((1-damping_factor)/n) + v

            if i > 0 and abs(v - res[key]) < 0.001:
                done.add(key)

            new[key] = v

        for key in new.keys():
            res[key] = new[key]

        i += 1

    total = 0.00

    for v in res.values():
        total += v

    print(total)

    return res


if __name__ == "__main__":
    main()
