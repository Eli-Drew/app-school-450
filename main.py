"""
This file is currrently the main driver of the whole application.
"""

from user_input import input
from analysis.henry_model import henry_model
from analysis import analysis

max_word_len = 250

def main():
    # TODO Somehow pull in the model and tokenizer created from the jupyter notebook file
    model, tokenizer = henry_model.create_model(max_word_len)

    data = input.get_input(max_word_len)

    padded_sequences = analysis.pre_process(tokenizer, data, max_word_len)
    sentiments = analysis.feed_tokens_to_graph(padded_sequences, model)

    # Set sentminets to the corresponding response_obj
    for i in range(len(sentiments)):
        input.response_objs[i].set_sentiment_score(sentiments[i][0])

    # Display the response_objs
    for response_obj in input.response_objs:
        print(response_obj)
        print()

if __name__ == "__main__":
    main()