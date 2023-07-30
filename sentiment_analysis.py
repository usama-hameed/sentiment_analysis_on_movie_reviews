import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from celery_config import celery_app
import json

nlp = spacy.load('en_core_web_sm')


@celery_app.task
def text_cleaning(reviews):
    cleaned_text = []
    for review in json.loads(reviews):
        raw_reviews = nlp(review)
        new_review_text = " ".join(token.text for token in raw_reviews if not token.is_stop)
        raw_reviews = nlp(new_review_text)
        cleaned_text.append(" ".join(token.lemma_ for token in raw_reviews if not token.is_stop))
    return json.dumps(cleaned_text)


@celery_app.task
def analyze_sentiment(texts):
    analyzer = SentimentIntensityAnalyzer()
    for text in texts:
        doc = nlp(text)
        preprocessed_text = " ".join(token.lemma_ for token in doc if not token.is_stop)

        sentiment_scores = analyzer.polarity_scores(preprocessed_text)
        compound_score = sentiment_scores['compound']

        if compound_score >= 0.05:
            return "POSITIVE"
        elif compound_score <= -0.05:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
