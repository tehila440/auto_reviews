#basic data cleaning preprocessing
#
#can comment out functions not using after loading

#import libraries for function
from textblob import TextBlob, Word

def basic_preprocess(df,feature):
    #remove URLs
    def remove_URL(text):
        url = re.compile(r'https?://\S+|www\.\S+')
        return url.sub(r'',text)
    df[feature] = df[feature].apply(lambda x: remove_URL(x))

    #remove HTML tags
    def remove_html(text):
        html = re.compile(r'<.*?>')
        return html.sub(r'',text)
    df[feature] = df[feature].apply(lambda x: remove_html(x))

    #remove Emojis
    def remove_emoji(text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
    df[feature] = df[feature].apply(lambda x: remove_emoji(x))

    #transform to lower case
    df[feature] = df[feature].apply(lambda x: ' '.join(x.lower() for x in x.split()))

    #remove characters, symbols
    df[feature] = df[feature].str.replace(r"[^a-zA-Z0-9]"," ")

    # remove characters, symbols,and numbers
    df[feature] = df[feature].str.replace(r"[^a-zA-Z#]", " ")

    #remove stop words
    stop = stopwords.words('english')
    df[feature] = df[feature].apply(lambda x: ' '.join(x for x in x.split() if x not in stop))

    #remove 10 most frequently occuring words
    freq = pd.Series(' '.join(df[feature]).split()).value_counts()[:10]
    print('Most commonly used words','\n', freq)
    freq = list(freq.index)
    df[feature] = df[feature].apply(lambda x: ' '.join(x for x in x.split() if x not in freq))

    #remove rare words
    freq = pd.Series(' '.join(df[feature]).split()).value_counts()[-10:]
    print('Rare words', '\n', freq)
    freq = list(freq.index)
    df[feature] = df[feature].apply(lambda x: ' '.join(x for x in x.split() if x not in freq))

    # remove short words (length < 3)
    df[feature] = df[feature].apply(lambda x: ' '.join([w for w in x.split() if len(w) > 2]))

    #skip spelling corrections for now
    #can use TextBlob to tokenize

    #will use Lemmatization instead of Stemming
    df[feature] = df[feature].apply(lambda x: ' '.join([Word(word).lemmatize() for word in x.split()]))

    # function to lemmatize and filter by noun and adjective
    nlp = spacy.load('en', disable=['parser', 'ner'])

    return df
def lemmatization(texts, tags=['NOUN', 'ADJ']):  # filter noun and adjective
    output = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        output.append([token.lemma_ for token in doc if token.pos_ in tags])
    return output
    #df[feature] = df[feature].apply(lambda x: )


