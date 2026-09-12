import pandas as pd

def load_data():
    df = pd.read_csv("data/diseases.csv")
    return df

def search_data(df, query):
    query = query.lower()
    words = query.split()
    
    mask = df["content"].str.lower().str.contains("", regex=False)
    mask[:] = False

    for word in words:
        if len(word) > 3:  # skip tiny words like "the", "are"
            mask = mask | df["content"].str.lower().str.contains(word) | \
                          df["condition"].str.lower().str.contains(word) | \
                          df["topic"].str.lower().str.contains(word)
    
    return df[mask]

if __name__ == "__main__":
    df = load_data()
    print("Loaded", len(df), "rows")
    print(df)

    results = search_data(df, "diabetes")
    print("\nSearch results for 'diabetes':")
    print(results)