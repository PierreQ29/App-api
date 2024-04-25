import re
import streamlit as st
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.tracer import Tracer
from opencensus.trace.samplers import ProbabilitySampler


# Fonction pour étendre les contractions
def expand_contractions(text: str) -> str:
    """
    Étend les contractions dans une chaîne de texte.
    Args:
        text (str): Texte d'entrée.
    Return:
        str: Texte avec contractions étendues.
    """
    flags = re.IGNORECASE | re.MULTILINE

    text = re.sub(r'`', "'", text, flags=flags)

    ## starts / ends with '
    text = re.sub(
        r"(\s|^)'(aight|cause)(\s|$)",
        '\g<1>\g<2>\g<3>',
        text, flags=flags
    )

    text = re.sub(
        r"(\s|^)'t(was|is)(\s|$)", r'\g<1>it \g<2>\g<3>',
        text,
        flags=flags
    )

    text = re.sub(
        r"(\s|^)ol'(\s|$)",
        '\g<1>old\g<2>',
        text, flags=flags
    )

    ## expand words without '
    text = re.sub(r"\b(aight)\b", 'alright', text, flags=flags)
    text = re.sub(r'\bcause\b', 'because', text, flags=flags)
    text = re.sub(r'\b(finna|gonna)\b', 'going to', text, flags=flags)
    text = re.sub(r'\bgimme\b', 'give me', text, flags=flags)
    text = re.sub(r"\bgive'n\b", 'given', text, flags=flags)
    text = re.sub(r"\bhowdy\b", 'how do you do', text, flags=flags)
    text = re.sub(r"\bgotta\b", 'got to', text, flags=flags)
    text = re.sub(r"\binnit\b", 'is it not', text, flags=flags)
    text = re.sub(r"\b(can)(not)\b", r'\g<1> \g<2>', text, flags=flags)
    text = re.sub(r"\bwanna\b", 'want to', text, flags=flags)
    text = re.sub(r"\bmethinks\b", 'me thinks', text, flags=flags)

    ## one offs,
    text = re.sub(r"\bo'er\b", r'over', text, flags=flags)
    text = re.sub(r"\bne'er\b", r'never', text, flags=flags)
    text = re.sub(r"\bo'?clock\b", 'of the clock', text, flags=flags)
    text = re.sub(r"\bma'am\b", 'madam', text, flags=flags)
    text = re.sub(r"\bgiv'n\b", 'given', text, flags=flags)
    text = re.sub(r"\be'er\b", 'ever', text, flags=flags)
    text = re.sub(r"\bd'ye\b", 'do you', text, flags=flags)
    text = re.sub(r"\be'er\b", 'ever', text, flags=flags)
    text = re.sub(r"\bd'ye\b", 'do you', text, flags=flags)
    text = re.sub(r"\bg'?day\b", 'good day', text, flags=flags)
    text = re.sub(r"\b(ain|amn)'?t\b", 'am not', text, flags=flags)
    text = re.sub(r"\b(are|can)'?t\b", r'\g<1> not', text, flags=flags)
    text = re.sub(r"\b(let)'?s\b", r'\g<1> us', text, flags=flags)

    ## major expansions involving smaller,
    text = re.sub(r"\by'all'dn't've'd\b", 'you all would not have had', text, flags=flags)
    text = re.sub(r"\by'all're\b", 'you all are', text, flags=flags)
    text = re.sub(r"\by'all'd've\b", 'you all would have', text, flags=flags)
    text = re.sub(r"(\s)y'all(\s)", r'\g<1>you all\g<2>', text, flags=flags)

    ## minor,
    text = re.sub(r"\b(won)'?t\b", 'will not', text, flags=flags)
    text = re.sub(r"\bhe'd\b", 'he had', text, flags=flags)

    ## major,
    text = re.sub(r"\b(I|we|who)'?d'?ve\b", r'\g<1> would have', text, flags=flags)
    text = re.sub(r"\b(could|would|must|should|would)n'?t'?ve\b", r'\g<1> not have', text, flags=flags)
    text = re.sub(r"\b(he)'?dn'?t'?ve'?d\b", r'\g<1> would not have had', text, flags=flags)
    text = re.sub(r"\b(daren|daresn|dasn)'?t", 'dare not', text, flags=flags)
    text = re.sub(r"\b(he|how|i|it|she|that|there|these|they|we|what|where|which|who|you)'?ll\b", r'\g<1> will', text,
                  flags=flags)
    text = re.sub(
        r"\b(everybody|everyone|he|how|it|she|somebody|someone|something|that|there|this|what|when|where|which|who|why)'?s\b",
        r'\g<1> is', text, flags=flags)
    text = re.sub(r"\b(I)'?m'a\b", r'\g<1> am about to', text, flags=flags)
    text = re.sub(r"\b(I)'?m'o\b", r'\g<1> am going to', text, flags=flags)
    text = re.sub(r"\b(I)'?m\b", r'\g<1> am', text, flags=flags)
    text = re.sub(r"\bshan't\b", 'shall not', text, flags=flags)
    text = re.sub(
        r"\b(are|could|did|does|do|go|had|has|have|is|may|might|must|need|ought|shall|should|was|were|would)n'?t\b",
        r'\g<1> not', text, flags=flags)
    text = re.sub(
        r"\b(could|had|he|i|may|might|must|should|these|they|those|to|we|what|where|which|who|would|you)'?ve\b",
        r'\g<1> have', text, flags=flags)
    text = re.sub(r"\b(how|so|that|there|these|they|those|we|what|where|which|who|why|you)'?re\b", r'\g<1> are', text,
                  flags=flags)
    text = re.sub(r"\b(I|it|she|that|there|they|we|which|you)'?d\b", r'\g<1> had', text, flags=flags)
    text = re.sub(r"\b(how|what|where|who|why)'?d\b", r'\g<1> did', text, flags=flags)

    return text

def process_text(doc, rejoin=False):
    # lower
    doc = doc.lower().strip()

    # tokenize
    tokenizer = RegexpTokenizer(r"\w+")
    raw_tokens_list = tokenizer.tokenize(doc)

    # only alpha chars
    alpha_tokens = [w for w in raw_tokens_list if w.isalpha()]

    # Lemmatize
    trans = WordNetLemmatizer()
    trans_text = [trans.lemmatize(i) for i in alpha_tokens]

    # manage return type
    if rejoin:
        return " ".join(trans_text)

    return trans_text

# Charger le modèle
with open('Model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Charger le vectoriseur
with open('Model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)


# Créer une instance FastAPI
app = FastAPI()

# Définir un modèle Pydantic pour le corps de la requête
class Tweet(BaseModel):
    text: str


@app.post("/predict")
async def predict_sentiment(tweet: Tweet):
    # Prétraiter le tweet
    tweet = process_text(tweet.text, rejoin=True)

    # Transformer le texte avec le vectoriseur
    tweet_vec = vectorizer.transform([tweet])

    # Prédire le sentiment du tweet
    prediction = model.predict(tweet_vec)

    # Interpréter la prédiction
    sentiment = 'positif' if prediction[0] > 0.5 else 'négatif'

    return {"sentiment": sentiment}

# Programmation des traces envoyé à Azure Application Insights

exporter = AzureExporter(instrumentation_key='0acfd902-d17e-46de-8131-cd05fb331e9d')
tracer = Tracer(exporter=exporter, sampler=ProbabilitySampler(1.0))

with tracer.span(name='mytask'):
    tracer.add_attribute('tweet', 'le texte du tweet')
    tracer.add_attribute('prediction', 'la prédiction')
