# Example using OpenAI GPT-4 (Note: This is a hypothetical example, and GPT-4 might not be available at the time of this response)

#import openai
#You need to sign up for OpenAI's GPT-4 API and obtain an API key to use this service

# openai.api_key = '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'

# def generate_article_summary(article_text):
#     response = openai.Completion.create(
#       engine="text-davinci-002",  # Choose the appropriate engine
#       prompt=article_text,
#       max_tokens=150,  # Adjust as needed
#       temperature=0.7  # Adjust as needed
#     )
    
#     return response.choices[0].text.strip()

# # Usage
# article_text = "The full text of the article..."
# summary = generate_article_summary(article_text)
# print(summary)

import pandas as pd
from bertopic import BERTopic
from scipy.linalg import eigh

# Example dataset
data = {'ArticleID': [1, 2, 3],
        'Title': ['Article 1', 'Article 2', 'Article 3'],
        'Content': ['Content of article 1 about technology.',
                    'Article 2 discusses science and research.',
                    'Sports news in article 3.']}

df = pd.DataFrame(data)

# Create BERTopic model with dense matrices
topic_model = BERTopic(embedding_model="dense")

# Fit the model on article content
topics, _ = topic_model.fit_transform(df['Content'])
df['Topic'] = topics

# Example user's selected themes
user_themes = ['technology', 'science']

# Filter articles based on user's selected themes
suggested_articles = df[df['Topic'].isin(user_themes)]

# Display suggested articles
for index, row in suggested_articles.iterrows():
    print(f"Title: {row['Title']}")
    print(f"Content: {row['Content']}")
    print("------------")


