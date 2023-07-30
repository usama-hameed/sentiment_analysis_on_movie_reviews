from sentiment_analysis import analyze_sentiment, text_cleaning
import json


def test_sentiment_analysis():

    input = ['Barbie is a bad movie']
    cleaned_data = text_cleaning(json.dumps(input))

    sentiments = analyze_sentiment(cleaned_data)

    assert 'NEUTRAL' == sentiments
