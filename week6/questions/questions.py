import nltk
import sys
import os
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    output = {}

    for subdir, dir, files in os.walk(directory):
        for file in files:
            with open(directory + os.sep + file) as f:
                key = file
                value = f.read()
                output[key] = value

    return output


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    token = nltk.word_tokenize(document)

    output = [word.lower() for word in token if (word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"))]

    return output


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = {}

    # Total number of documents
    totalDocuments = len(documents)

    # List of all words
    all_words = []
    for key in documents:
        document = documents[key]
        for word in document:
            if word not in all_words:
                all_words.append(word)
    
    # Compute IDFs
    for word in all_words:
        count = 0
        for key in documents:
            document = documents[key]
            if word in document:
                count += 1
                continue
        idfs[word] = count / totalDocuments
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_idfs = {}

    for filename in files:
        file_idfs[filename] = 0
        for word in query:
            file_idfs[filename] += files[filename].count(word) * idfs[word]

    # Sort descending by value and get first n. Returns a list of (filename, idf) tuples
    file_idfs = sorted(file_idfs.items(), key=lambda x: x[1], reverse=True)[:n]
    
    return [filename for filename, idf in file_idfs]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    rank = []

    for sentence in sentences:
        sentence_values = [sentence, 0, 0]

        for word in query:
            if word in sentences[sentence]:
                # Compute matching word measure. Sum of IDF values.
                sentence_values[1] += idfs[word]
                # Compute query term density. Proportion of words in a sentence that are in the query.
                sentence_values[2] += sentences[sentence].count(
                    word) / len(sentences[sentence])

        rank.append(sentence_values)

    rank = sorted(rank, key=lambda x: (x[1], x[2]), reverse=True)[:n]
    
    return [sentence for sentence, mwm, qtd in rank]


if __name__ == "__main__":
    main()
