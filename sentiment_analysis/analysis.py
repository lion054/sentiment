from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
import sentiment_analysis.config as config
import itertools
import pprint
import re
import jsonpickle


credentials = CognitiveServicesCredentials(config.key)
client = TextAnalyticsClient(endpoint=config.endpoint,credentials=credentials)


def request_sentiment(documents,inverse_threshold=0.5):
    response = client.sentiment(documents=documents).documents
    if inverse_threshold == 0:
        return response
    return list([a for a in response if a.score < inverse_threshold])


def request_key_phrases(documents):
    response = client.key_phrases(documents=documents).documents
    return response


def request_entities(documents):
    response = client.entities(documents=documents).documents
    return response


def analyse(text_json):
    """
    :param text_json: array of strings
    :return:
    """
    formatted_input = []
    for num,item in enumerate(text_json):
       formatted_input.append({
           "id":num,
           "language": "en",
            "text":item,
       })

    sentiment_results = request_sentiment(documents=formatted_input)
    key_phrases_results = request_key_phrases(documents=formatted_input)
    entities_results = request_entities(documents=formatted_input)
    aggregate = zip(sentiment_results,key_phrases_results,entities_results)
    results = []
    for key,group in itertools.groupby(aggregate,lambda x:x[0].id):
        for a in group:
            results.append({**a[0].__dict__,**a[1].__dict__,**a[2].__dict__})
    return {"entity":provide_entity_matrix(results), "key_phrases":provide_key_word_matrix(results)}


def provide_entity_matrix(result):
    entity_matrix={}
    for analysis in result:
        for entity in analysis["entities"]:
            if re.match("\d",entity.name):
                continue
            if entity.name in entity_matrix:
                statistics = entity_matrix[entity.name]
                statistics["frequency"] += 1
                statistics["avg_sentiment"] = statistics["avg_sentiment"] / statistics["frequency"]
            else:
                entity_matrix[entity.name] = {
                    "frequency":1,
                    "avg_sentiment":analysis["score"]
                }
    return entity_matrix


def provide_key_word_matrix(result):
    key_phrases={}
    for analysis in result:
        for phrase in analysis["key_phrases"]:
            if re.match(".*[0-9].*",phrase,re.MULTILINE):
                continue
            if phrase in key_phrases:
                statistics = key_phrases[phrase]
                statistics["frequency"] += 1
                statistics["avg_sentiment"] = statistics["avg_sentiment"] / statistics["frequency"]
            else:
                key_phrases[phrase] = {
                    "frequency":1,
                    "avg_sentiment":analysis["score"]
                }
    return key_phrases

if __name__ == "__main__":
    test = ["Spain was a fun holiday","Germany is crazy","I love the Mexican border wall"]
    result = analyse(test)
    pprint.pprint(jsonpickle.encode(result,max_depth=10,keys=True),indent=2)
