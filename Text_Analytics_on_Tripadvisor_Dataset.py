# -*- coding: utf-8 -*-
"""Untitled10.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15SKz3P79ab8tDKwr9dpT3zaGiWzEmcQW
"""

from google.colab import drive
drive.mount('/content/drive')

"""**Getting the dataset**"""

import pandas as pd
file_path = '/content/drive/MyDrive/Dataset/tripadvisor_hotel_reviews.csv'
df = pd.read_csv(file_path)
df.head()

"""**Importing necessary packages**"""

import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk import ngrams
from string import punctuation
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
import numpy as np
import torch.nn as nn
# Oversamplers
from imblearn.over_sampling import (
    RandomOverSampler,
    SMOTE,
    BorderlineSMOTE,
    SVMSMOTE,
    KMeansSMOTE,
    ADASYN,
    SMOTEN
)

# Undersamplers
from imblearn.under_sampling import (
    RandomUnderSampler,
    TomekLinks,
    NearMiss,
    EditedNearestNeighbours,
    RepeatedEditedNearestNeighbours,
    AllKNN,
    InstanceHardnessThreshold,
    ClusterCentroids,
    CondensedNearestNeighbour,
    OneSidedSelection,
    NeighbourhoodCleaningRule
)

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('movie_reviews')
nltk.download('sentiwordnet')
nltk.download('wordnet')
nltk.download('punkt_tab')

"""**Data preprocessing**"""

# Sentence tokenization
df['Review'] = df['Review'].apply(sent_tokenize)

# Word tokenization
df['Review'] = df['Review'].apply(lambda sents: [word_tokenize(sent) for sent in sents])

# Flatten sentence-level tokens into one list of tokens per review
df['Review'] = df['Review'].apply(lambda list_of_lists: [word for sent in list_of_lists for word in sent])

# Clean tokens: remove stopwords, punctuation, and digits
eng_stopwords = set(stopwords.words('english'))
df['Review'] = df['Review'].apply(
    lambda words: [w for w in words if w.lower() not in eng_stopwords and w not in punctuation and not w.isdigit()]
)

stemmer = PorterStemmer()
df['Review'] = df['Review'].apply(
    lambda words: [stemmer.stem(w) for w in words]
)


lemmatizer = WordNetLemmatizer()
df['Review'] = df['Review'].apply(
    lambda words: [lemmatizer.lemmatize(w) for w in words]
)

df3=df.copy()
df4=df.copy()

text =' '.join(df['Review'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Text Data')
plt.show()

words = ' '.join(df['Review'].dropna().astype(str)).lower().split()

common_words = Counter(words).most_common(30)
words_df = pd.DataFrame(common_words, columns=['Word', 'Frequency'])

sns.barplot(data=words_df, x='Frequency', y='Word')
plt.title('Top 30 Frequent Words')
plt.show()

df2=df['Review'].apply(lambda x: len(str(x).split()))
plt.figure(figsize=(10,5))
plt.plot(df2,marker='o')
plt.title('Sentence Length')
plt.xlabel('Index')
plt.ylabel('Length (in words)')
plt.grid(True)
plt.show()

all_words = [word for review in df['Review'] for word in review]

# Step 2: Calculate counts
total_words = len(all_words)
unique_words = len(set(all_words))

# Step 3: Print the counts
print(f"Total words: {total_words}")
print(f"Unique words: {unique_words}")

# Step 4: Plot
plt.figure(figsize=(6, 4))
plt.bar(['Total Words', 'Unique Words'], [total_words, unique_words], color=['cornflowerblue', 'seagreen'])
plt.title('Total vs Unique Words in Preprocessed Corpus')
plt.ylabel('Count')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

"""**Uniq word for review**"""

unique_words_per_review = df['Review'].apply(lambda x: len(set(x)))
print(unique_words_per_review.head())
plt.figure(figsize=(8,5))
plt.hist(unique_words_per_review, bins=30, color='mediumseagreen', edgecolor='black')
plt.title('Distribution of Unique Words per Review')
plt.xlabel('Unique Words')
plt.ylabel('Number of Reviews')
plt.show()

"""**Most Common N-grams**"""

all_bigrams = []
for review in df['Review']:
    all_bigrams.extend(list(ngrams(review, 2)))

bigram_counts = Counter(all_bigrams)
top_bigrams = bigram_counts.most_common(20)

bigrams, counts = zip(*top_bigrams)
bigrams = [' '.join(bigram) for bigram in bigrams]

plt.figure(figsize=(10,6))
plt.bar(bigrams, counts, color='orchid')
plt.xticks(rotation=45)
plt.title('Top 20 Most Frequent Bigrams')
plt.ylabel('Frequency')
plt.show()

# Character counts (convert list of words back to string)
df["char_count"] = df["Review"].map(lambda x: len(" ".join(x)))

# Word counts
df["word_count"] = df["Review"].map(lambda x: len(x))

# Sentence counts (reconstruct text to count sentences)
df["sent_count"] = df["Review"].map(lambda x: len(sent_tokenize(" ".join(x))))

# Hashtag counts
df["hashtag_count"] = df["Review"].map(lambda x: x.count("#"))

# Average word length
df["avg_word_len"] = df["Review"].map(lambda x: np.mean([len(w) for w in x]) if x else 0)

# Average sentence length
df["avg_sent_len"] = df["Review"].map(lambda x: np.mean([len(sent.split()) for sent in sent_tokenize(" ".join(x))]) if x else 0)

features = [
    "char_count",
    "word_count",
    "sent_count",
    "hashtag_count",
    "avg_word_len",
    "avg_sent_len"
]

target = "Rating"

for feature in features:
    # Histogram
    sns.histplot(data=df, x=feature, hue=target, palette="Set2", multiple="stack")
    plt.title(f"Histogram of {feature} by {target}")
    plt.xlabel(feature)
    plt.ylabel("Count")
    plt.show()

    # KDE Plot
    sns.kdeplot(data=df, x=feature, hue=target, palette="Set1")
    plt.title(f"KDE Plot of {feature} by {target}")
    plt.xlabel(feature)
    plt.ylabel("Density")
    plt.show()

    # Boxplot
    sns.boxplot(data=df, x=target, y=feature, palette="pastel")
    plt.title(f"Boxplot of {feature} across {target}")
    plt.xlabel(target)
    plt.ylabel(feature)
    plt.show()

# Function to get n-grams from list of token lists
def get_ngrams(token_lists, n):
    ngram_list = []
    for tokens in token_lists:
        ngram_list.extend(list(ngrams(tokens, n)))
    return ngram_list

# Function to plot n-gram frequencies with readable labels
def plot_ngram_freq(ngram_counts, title, color):
    ngrams_, counts = zip(*ngram_counts)
    # Join tuple of words into string
    ngram_labels = [' '.join(ngram) for ngram in ngrams_]

    plt.figure(figsize=(12, 6))
    plt.bar(ngram_labels, counts, color=color)
    plt.xticks(rotation=45, ha='right')
    plt.title(title)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

# Prepare tokens for negative and positive reviews
neg_tokens = df3[df3['Rating'] <= 2]['Review'].tolist()
pos_tokens = df3[df3['Rating'] >= 4]['Review'].tolist()

N = 20  # top N n-grams to plot

# --- Unigrams ---
neg_unigrams = [word for tokens in neg_tokens for word in tokens]
pos_unigrams = [word for tokens in pos_tokens for word in tokens]

neg_unigram_counts = Counter(neg_unigrams).most_common(N)
pos_unigram_counts = Counter(pos_unigrams).most_common(N)

plot_ngram_freq(neg_unigram_counts, "Top Unigrams in Negative Reviews (Rating 1 or 2)", "salmon")
plot_ngram_freq(pos_unigram_counts, "Top Unigrams in Positive Reviews (Rating 4 or 5)", "seagreen")

# --- Bigrams ---
neg_bigrams = get_ngrams(neg_tokens, 2)
pos_bigrams = get_ngrams(pos_tokens, 2)

neg_bigram_counts = Counter(neg_bigrams).most_common(N)
pos_bigram_counts = Counter(pos_bigrams).most_common(N)

plot_ngram_freq(neg_bigram_counts, "Top Bigrams in Negative Reviews (Rating 1 or 2)", "tomato")
plot_ngram_freq(pos_bigram_counts, "Top Bigrams in Positive Reviews (Rating 4 or 5)", "forestgreen")

# --- Trigrams ---
neg_trigrams = get_ngrams(neg_tokens, 3)
pos_trigrams = get_ngrams(pos_tokens, 3)

neg_trigram_counts = Counter(neg_trigrams).most_common(N)
pos_trigram_counts = Counter(pos_trigrams).most_common(N)

plot_ngram_freq(neg_trigram_counts, "Top Trigrams in Negative Reviews (Rating 1 or 2)", "lightcoral")
plot_ngram_freq(pos_trigram_counts, "Top Trigrams in Positive Reviews (Rating 4 or 5)", "mediumseagreen")

# import pandas as pd
# from nltk.sentiment import SentimentIntensityAnalyzer
# from textblob import TextBlob
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch
# from collections import Counter

# # Initialize VADER
# vader = SentimentIntensityAnalyzer()

# # Initialize RoBERTa
# tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
# model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
# model.eval()
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)
# labels_roberta = ['negative', 'neutral', 'positive']

# # Classifiers
# def classify_vader(text):
#     score = vader.polarity_scores(text)['compound']
#     if score >= 0.05:
#         return 'positive'
#     elif score <= -0.05:
#         return 'negative'
#     else:
#         return 'neutral'

# def classify_textblob(text):
#     polarity = TextBlob(text).sentiment.polarity
#     if polarity > 0:
#         return 'positive'
#     elif polarity < 0:
#         return 'negative'
#     else:
#         return 'neutral'

# def classify_roberta_batch(texts, batch_size=16):
#     all_preds = []
#     for i in range(0, len(texts), batch_size):
#         batch = texts[i:i+batch_size]
#         inputs = tokenizer(batch, return_tensors="pt", truncation=True, padding=True, max_length=512)
#         inputs = {k:v.to(device) for k,v in inputs.items()}
#         with torch.no_grad():
#             logits = model(**inputs).logits
#         probs = torch.softmax(logits, dim=1)
#         preds = torch.argmax(probs, dim=1).cpu().tolist()
#         all_preds.extend([labels_roberta[p] for p in preds])
#     return all_preds

# def majority_vote(labels):
#     return Counter(labels).most_common(1)[0][0]

# # Prepare review texts (make sure they're strings)
# reviews = df3['Review'].astype(str).tolist()

# # Get RoBERTa predictions in batch
# roberta_preds = classify_roberta_batch(reviews)

# # Combine predictions and get final label by majority voting
# final_labels = []
# for i, review in enumerate(reviews):
#     votes = [
#         classify_vader(review),
#         classify_textblob(review),
#         roberta_preds[i]
#     ]
#     final_labels.append(majority_vote(votes))

# df3['Predicted_Sentiment'] = final_labels

# print(df3[['Review', 'Predicted_Sentiment']])

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

df4['Review'] = df4['Review'].apply(lambda tokens: ' '.join(tokens) if isinstance(tokens, list) else tokens)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df4['Review'])

features = X
target = df4['Rating']

def evaluate_models(X_train, Y_train, X_val, Y_val):
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
        'Multinomial Naive Bayes': MultinomialNB(),
        'Decision Tree': DecisionTreeClassifier(random_state=2)
    }

    for name, model in models.items():
        try:
            model.fit(X_train, Y_train)
            val_preds = model.predict(X_val)

            print(f'{name}:')
            print('Validation F1 Score:', metrics.f1_score(Y_val, val_preds, average='weighted'))
            print('Validation Precision:', metrics.precision_score(Y_val, val_preds, average='weighted'))
            print('Validation Balanced Accuracy:', metrics.balanced_accuracy_score(Y_val, val_preds))
            print()
        except ValueError as e:
            print(f'{name} failed due to: {e}\n')

X_train, X_val, Y_train, Y_val = train_test_split(
    features, target, test_size=0.2, stratify=target, random_state=2
)

print("Evaluating on raw data:")
evaluate_models(X_train, Y_train, X_val, Y_val)

# Oversampled train data only
smote = SMOTE(random_state=2)
X_train_os, Y_train_os = smote.fit_resample(X_train, Y_train)

print("Evaluating on oversampled training data:")
evaluate_models(X_train_os, Y_train_os, X_val, Y_val)

# smote_bs = BorderlineSMOTE(random_state=2)
# X_train_bs, Y_train_bs = smote_bs.fit_resample(X_train, Y_train)

# print("Evaluating on borderline training data:")
# evaluate_models(X_train_bs, Y_train_bs, X_val, Y_val)

# from imblearn.under_sampling import RandomUnderSampler

# rus = RandomUnderSampler(random_state=2)
# X_train_rus, Y_train_rus = rus.fit_resample(X_train, Y_train)

# print("Evaluating on undersampled training data (RandomUnderSampler):")
# evaluate_models(X_train_rus, Y_train_rus, X_val, Y_val)

# from imblearn.combine import SMOTETomek

# smote_tomek = SMOTETomek(random_state=2)
# X_train_st, Y_train_st = smote_tomek.fit_resample(X_train, Y_train)

# print("Evaluating on hybrid sampled training data (SMOTETomek):")
# evaluate_models(X_train_st, Y_train_st, X_val, Y_val)

# from imblearn.combine import SMOTEENN

# smote_enn = SMOTEENN(random_state=2)
# X_train_se, Y_train_se = smote_enn.fit_resample(X_train, Y_train)

# print("Evaluating on hybrid sampled training data (SMOTEENN):")
# evaluate_models(X_train_se, Y_train_se, X_val, Y_val)

class MLPModel(nn.Module):

    def __init__(self, input_dim, hidden_dim):
        super(MLPModel, self).__init__()
        self.linear1 = nn.Linear(input_dim, hidden_dim)
        self.linear2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.sigmoid(self.linear1(x))
        x = self.linear2(x)
        return x

num_classes = len(target.value_counts())
    # number of features (len of X cols)
    input_dim = features.shape[1]
    # number of hidden layers
    hidden_dim = 64
    # number of classes (unique of y)
    output_dim = num_classes

import torch
from torch.utils.data import DataLoader, TensorDataset
import torch.optim as optim
from sklearn.preprocessing import LabelEncoder
import numpy as np
le = LabelEncoder()
target = le.fit_transform(df4['Rating'])
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, balanced_accuracy_score
import statistics

f1_list = []
balanced_accuracy_list = []

for seed in range(0, 10):
    np.random.seed(seed)
    torch.manual_seed(seed)
    # sm = SMOTE(random_state=seed)
    # X_res, y_res = sm.fit_resample(features, target)

    rus = RandomUnderSampler(random_state=seed)
    X_res, y_res = rus.fit_resample(features, target)

    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=seed)

    # Convert to PyTorch tensors
    X_train_tensor = torch.tensor(X_train.toarray(), dtype=torch.float32)
    Y_train_tensor = torch.tensor(y_train, dtype=torch.long)
    X_test_tensor = torch.tensor(X_test.toarray(), dtype=torch.float32)
    Y_test_tensor = torch.tensor(y_test, dtype=torch.long)




    # Create DataLoader
    train_dataset = TensorDataset(X_train_tensor, Y_train_tensor)
    test_dataset = TensorDataset(X_test_tensor, Y_test_tensor)
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)
    #MLPModel, LSTMModel, DNNModel, GRUModel, ELMModel
    # Model, loss function, optimizer
    model = MLPModel(input_dim=X_train.shape[1], hidden_dim=hidden_dim)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)


    epochs = 100
    for epoch in range(epochs):
        model.train()
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        print(f'Epoch {epoch+1}/{epochs}, Loss: {loss.item()}')

    # Evaluation
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            all_preds.extend(predicted.numpy())
            all_labels.extend(labels.numpy())

    # Calculate metrics
    f1 = 100*f1_score(all_labels, all_preds, average='micro')
    balanced_accuracy=100*balanced_accuracy_score(all_labels, all_preds)



    print(f'F1-Score of the network for seed {seed} on the test data: {f1:.4f}')
    print(f'Balanced Accuracy of the network for seed {seed} on the test data: {balanced_accuracy: .4f}')




    f1_list.append(f1)
    balanced_accuracy_list.append(balanced_accuracy)

print('F1-Score Mean: ', statistics.mean(f1_list),  ', Std Deviation: ', statistics.stdev(f1_list))
print('Balanced Accuracy Mean: ', statistics.mean(balanced_accuracy_list),  ', Std Deviation: ', statistics.stdev(balanced_accuracy_list))