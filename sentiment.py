import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def classify_sentiment(text):
    score = analyzer.polarity_scores(text)
    compound = score["compound"]
    if compound >=0.05:
        return "Positive", compound
    elif compound <= -0.05:
        return "Negative", compound 
    else:
        return "Neutral", compound

def analyze_reviews():
    df = pd.read_csv("data/reviews.csv")
    results = []
    for review in df["review"]:
        sentiment, score = classify_sentiment(review)
        results.append({"review": review, "sentiment": sentiment, "score": score})
    return pd.DataFrame(results)

def generate_wordcloud(results_df, sentiment_type):
    text = "".join(results_df[results_df["sentiment"] == sentiment_type]["review"])
    if text.strip() == "":
        print(f"No {sentiment_type} reviews to generate word cloud.")
        return
    wc = WordCloud(width=800, height=400, background_color="black", colormap="cool").generate(text)
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"{sentiment_type} Reviews Word Cloud")
    plt.savefig(f"wordcloud_{sentiment_type.lower()}.png")
    print(f"saved wordcloud_{sentiment_type.lower()}.png")
if __name__ == "__main__":
    results = analyze_reviews()
    print(results)
    print("\nSentiment counts:")
    print(results["sentiment"].value_counts())

    generate_wordcloud(results, "Positive")
    generate_wordcloud(results, "Negative")

def get_wordcloud_figure(results_df, sentiment_type):
    text = "".join(results_df[results_df["sentiment"] == sentiment_type]["review"])
    if text.strip() == "":
        return None
    wc = WordCloud(width=800, height=400, background_color="black", colormap="cool").generate(text)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_alpha(0)
    return fig