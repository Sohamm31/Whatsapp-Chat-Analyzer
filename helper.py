def fetch_stats(selected_user,df):
    if selected_user != "Overall":
        df = df[df["Username"] == selected_user]

    num_messages = df.shape[0]
    words = []
    for messages in df["Message"]:
        words.extend(messages.split())

    num_media_messages = df[df["Message"].str.contains("image omitted|video omitted", na=False)].shape[0]

    doc_messages = df[df["Message"].str.contains("document omitted", na=False)].shape[0]

    return num_messages, len(words),num_media_messages,doc_messages


def most_busy_users(df):
    x = df["Username"].value_counts().head()
    df = round(df["Username"].value_counts()/df.shape[0]*100,2).reset_index().rename(columns = {"index":"Name","Username":"Percent"})
    return x,df

