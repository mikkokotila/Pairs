class TokenStatistics:
    
    def __init__(self):
        
        _ = ''
    
    def query(self, tokens):

        '''Takes in a list of tokens and returns a dataframe with counts, 
        percentages, and cumulative percentages.

        tokens | list | List of tokens
        '''

        import pandas as pd
        import signs

        # initialize the signs object to be used for analysis
        describe = signs.Describe(tokens)
        counts = describe.get_counts()

        # convert the counts dictionary into a dataframe
        counts_df = pd.DataFrame()
        counts_df['token'] = counts.keys()
        counts_df['count'] = counts.values()

        # add columns for percentages and cumulative percentages
        tokens_with_counts = counts_df
        tokens_with_counts['pct_share'] = ((tokens_with_counts['count'] / tokens_with_counts['count'].sum()) * 100)
        tokens_with_counts['cum_sum'] = tokens_with_counts.pct_share.cumsum().round(1)
        tokens_with_counts['pct_share'] = tokens_with_counts['pct_share'].round(2)

        return tokens_with_counts
