#!/Users/Pedram/venv3/bin/python

import sys
import argparse
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def generate_wordcloud(output_path, exclusions, min_length):
    # Read text from stdin
    text = sys.stdin.read()

    # Define a set of stopwords to exclude from the word cloud
    custom_stopwords = set(STOPWORDS)

    # Add any additional stopwords from the exclusions list
    if exclusions:
        additional_stopwords = set(exclusions.split(','))
        custom_stopwords.update(additional_stopwords)

    # Filter words by length if min_length is specified
    if min_length:
        custom_stopwords.update({word for word in text.split() if len(word) <= min_length})

    # Generate the word cloud with stopwords
    wordcloud = WordCloud(width=4000, height=2000, background_color='black', stopwords=custom_stopwords).generate(text)

    # Save the word cloud image
    wordcloud.to_file(output_path)

if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Generate a word cloud from stdin and save it to a specified file, with optional exclusions and word length filtering.")
    parser.add_argument("output_path", help="The path to save the output PNG file.")
    parser.add_argument("--exclusions", help="A comma-separated list of words to exclude.", default="")
    parser.add_argument("--filter", type=int, help="Minimum length of words to be included in the word cloud.", default=0)

    # Parse the command line arguments
    args = parser.parse_args()

    generate_wordcloud(args.output_path, args.exclusions, args.filter)
