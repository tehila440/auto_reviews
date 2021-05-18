# function to plot most freq terms
def freq_words(x, terms=30):
    all_words = ' '.join([text for text in x])
    all_words = all_words.split()

    fdist = FreqDist(all_words)
    words_df = pd.DataFrame({'word': list(fdist.keys()), 'count': list(fdist.values())})

    # select top 20 most freq words
    d = words_df.nlargest(columns='count', n=terms)
    plt.figure(figsize=(20, 5))
    ax = sns.barplot(data=d, x='word', y='count')
    ax.set(ylabel='Count')
    plt.show()