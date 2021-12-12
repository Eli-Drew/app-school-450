from analysis.Analysis import Analysis
from textblob import TextBlob

class Thematic_Analysis(Analysis):

    """
    ===================================================================
    Description:
        Iterates through all noun phrases from the user's responses and
        creates a dictionary of those topics seen and their count
        of occurrences
    Paramaters:
        responses: a list of string responses
    Returns:
        Dictionary with all topics and their count of occurrences
    ===================================================================
    """
    @classmethod
    def pre_process(cls, responses):
        
        topics_dict = {}

        for resp in responses:

            for noun_phrase in TextBlob(resp).noun_phrases:

                stripped_noun_phrase_list = []
                for pos_tag in TextBlob(noun_phrase).tags:
                    if pos_tag[1] in ['JJ', 'JJR', 'JJS']:
                        continue
                    else:
                        stripped_noun_phrase_list.append(pos_tag[0])

                if 1 <= len(stripped_noun_phrase_list) <= 2:
                    stripped_noun_phrase = ' '.join(stripped_noun_phrase_list)
                    if noun_phrase not in topics_dict:
                        topics_dict[stripped_noun_phrase] = 1
                    else:
                        topics_dict[stripped_noun_phrase] += 1

        return topics_dict


    """
    ===================================================================
    Description:
        Takes the topics_dict returned by pre_process() and finds the
        top 5 topics with the highest counts
    Paramaters:
        topics_dict: dictionary with all topics and their count of occurrences
    Returns:
        Dictionary of the top 5 topics and their counts
    ===================================================================
    """
    @classmethod
    def analyze(cls, topics_dict):

        top_topics_dict = {
            "topic1" : 0,
            "topic2" : 0,
            "topic3" : 0,
            "topic4" : 0,
            "topic5" : 0
        }

        min_top_topic = "topic1"
        min_top_count = 0

        # Find the top 5 topics with the highest counts
        for topic, count in topics_dict.items():

            if count > min_top_count:
                del top_topics_dict[min_top_topic]
                top_topics_dict[topic] = count
                min_top_topic = topic
                min_top_count = count

                # Find the current minimum topic/count entry in top_topics_dict
                for top_topic, top_count in top_topics_dict.items():
                    if top_count < min_top_count:
                        min_top_topic = top_topic
                        min_top_count = top_count

        # Find and remove any topics from top_topics_dict if any entry at initialization is still present
        # This is a very rare case
        remove_topics = []
        for topic, count in top_topics_dict.items():
            if count == 0:
                remove_topics.append(topic)
        for topic in remove_topics:
            del top_topics_dict[topic]

        return top_topics_dict


    """
    ===================================================================
    Description:
        Sorts top_topics_dict based on value from greatest to least
    Paramaters:
        top_topics_dict: Dictionary of the top 5 topics and their counts
            returned by analyze()
    Returns:
        Dictionary of the top 5 topics and their counts sorted from
        greatest to least
    ===================================================================
    """
    @classmethod
    def format_results(cls, top_topics_dict):

        sorted_top_topics_dict = {}
        max_count_topic = ""
        max_count = 0
        
        for i in range(len(top_topics_dict)):

            for topic, count in top_topics_dict.items():
                if count > max_count:
                    max_count = count
                    max_count_topic = topic

            capitalized_max_count_topic = ""
            for word in max_count_topic.split():
                capitalized_max_count_topic += word.capitalize() + " "

            sorted_top_topics_dict[capitalized_max_count_topic.rstrip()] = max_count
            
            del top_topics_dict[max_count_topic]
            max_count_topic = ""
            max_count = 0

        return sorted_top_topics_dict

    
    """
    ===================================================================
    Description:
        Prints the top 5 topics and their count of occurrences
    Paramaters:
        sorted_topics_dict: Dictionary of the top 5 topics and their counts
            sorted from greatest to least
    Returns:
        N/A
    ===================================================================
    """
    @classmethod
    def print_top_themes(cls, sorted_top_topics_dict):
        print("\nTop {} Topics:".format(len(sorted_top_topics_dict)))
        for topic, count in sorted_top_topics_dict.items():
            print("{}: {}".format(topic, count))
