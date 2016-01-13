import os
import sys
from random import choice
import twitter


def open_and_read_file(file_path, current_text=None):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    text_file = open(file_path)
    text = text_file.read().replace('\n', ' ').strip()
    if current_text:
        text = ' '.join((current_text, text))
    text_file.close()
    return text


def make_chains(text_string, gram_len):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('mary', 'hi'): ['there'], ('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi']}

    """

    chains = {}

    text_list = text_string.split(" ")
    gram = tuple(text_list[:gram_len])
    
    # for index in range(len(text_list) - gram_len):
    #     if chains.has_key(gram):
    #         chains[gram].append(text_list[index+gram_len])
    #     else:
    #         chains[gram] = [text_list[index+gram_len]]

    #     gram = tuple(text_list[index+1:index+gram_len+1])


    for word in text_list[gram_len:]:
        if word == '':
            continue
        if chains.has_key(gram):
            chains[gram].append(word)
        else:
            chains[gram] = [word]

        gram = gram[1:] + tuple([word])

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    text = ""
    first_pair = choice(chains.keys())
    text = ' '.join(first_pair)
    text = text[0].capitalize() + text[1:]


    while chains.has_key((first_pair)):
        # if not text[-1].isalpha() and not text[-1].isdigit():
        #     break
        if text[-1] in '!.?':
            if len(text) <= (140 - 13): #added hashtag
                return text
            else:
                break
        next_word = choice(chains[first_pair])
        text += ' {}'.format(next_word)
        
        first_pair = (first_pair[1], next_word)

    return make_text(chains)


def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
    user_creds = api.VerifyCredentials()
    statuses = api.GetUserTimeline(screen_name=user_creds.screen_name)
    print statuses[0].text #statuses[0].coordinates

    status = api.PostUpdate(make_text(chains) + ' #Hack13right')


# print make_text(make_chains(open_and_read_file('gettysburg.txt')))
input_path = sys.argv[1]
input_path2 = sys.argv[2]

try:
    n = int(sys.argv[3])
    # Open the file and turn it into one long string
    input_text = open_and_read_file(input_path)
    input_text = open_and_read_file(input_path2, current_text=input_text)

    # Get a Markov chain
    chains = make_chains(input_text , n)

    # Produce random text
    #random_text = make_text(chains)
    while True:
        tweet(chains)
        again = raw_input("Do you want to tweet again? C for 'Continue' or q for 'quit'").lower()
        if again == 'c':
            continue
        elif again == 'q':
            print "Goodbye!"
            break
        else:
            print "That was not a valid option! Goodbye!"
            break

    # print random_text
    
except ValueError:
   print "Oops!  That was no valid number.  Try again..."


