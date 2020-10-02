from static import country_mappings_df
import pandas as pd


def concat_df_with_new_column_value(df, columns, new_value):
    df_copy = df.copy()
    df[columns]=new_value
    return pd.concat([df, df_copy])

def transform_to_combined_dateindex(df, dates):
    grouped_df = df.groupby(['EVENT_START', 'EVENT_END', 'COUNTRY', 'EVENT_TYPE', 'UNIT_TYPE_DESCRIPTION'])\
                            .agg({"CAPACITY_OFFLINE": "sum"}).reset_index();

    grouped_df = grouped_df.merge(country_mappings_df, how='left', left_on='COUNTRY', right_on='COUNTRY')
    grouped_df = concat_df_with_new_column_value(grouped_df, ['COUNTRY','REGION'], 'GLOBAL')
    grouped_df = concat_df_with_new_column_value(grouped_df, 'EVENT_TYPE', 'All')

    start_df = pd.pivot_table(grouped_df, index='EVENT_START', values='CAPACITY_OFFLINE',
                              columns=['REGION','EVENT_TYPE','UNIT_TYPE_DESCRIPTION'],
                              aggfunc='sum').reindex(dates).fillna(0)
    end_df = pd.pivot_table(grouped_df, index='EVENT_END', values='CAPACITY_OFFLINE',
                            columns=['REGION','EVENT_TYPE','UNIT_TYPE_DESCRIPTION'],
                            aggfunc='sum').reindex(dates).fillna(0) * -1

    comb_df = start_df.add(end_df).cumsum()

    comb_df_m = comb_df.resample('M').mean()
    comb_df_m['MONTH'] = comb_df_m.index.month
    comb_df_m['YEAR'] = comb_df_m.index.year
    comb_df_m = comb_df_m.set_index(['YEAR', 'MONTH'])
    return comb_df_m
