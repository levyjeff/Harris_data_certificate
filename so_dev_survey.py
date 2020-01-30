import os
import pandas as pd

#https://insights.stackoverflow.com/survey
path = r'C:\Users\Jeff Levy\Downloads\developer_survey_2019\survey_results_public.csv'
df = pd.read_csv(path)

languages = ['R', 'Python']
df[languages] = df['LanguageWorkedWith'].str.get_dummies(sep=';')[languages]
df['Both languages']   = df[languages].apply(lambda row: 1 if sum(row) == len(languages) else 0, axis=1)
df['Neither language'] = df[languages].apply(lambda row: 1 if sum(row) == 0              else 0, axis=1)

data_devs = ['Academic researcher', 'Data or business analyst',
             'Data scientist or machine learning specialist', 'Engineer, data']
df[data_devs] = df['DevType'].str.get_dummies(sep=';')[data_devs]
df['Data career'] = df[data_devs].apply(lambda row: 1 if sum(row) > 0 else 0, axis=1)

df['In US'] = df['Country'].map(lambda c: 1 if c == 'United States' else 0)

results = df.groupby('Data career').sum()[languages+['Both languages', 'Neither language']]
results['Sample size'] = results[languages+['Neither language']].sum(axis=1) - results['Both languages']

summary = pd.concat([results.applymap(lambda v: f'{v:,}'),
                     results.apply(lambda row: row / row['Sample size'], axis=1).applymap(lambda v: f'{v:.1%}')
                     ]).sort_index(ascending=False)

summary.index = summary.index.map(lambda i: 'Yes' if i == 1 else 'No')

# In [8]: summary
# Out[8]:
#                  R  Python Both languages Neither language Sample size
# Data career
# Yes          3,133  10,473          2,483            6,012      17,135
# Yes          18.3%   61.1%          14.5%            35.1%      100.0%
# No           1,915  25,970          1,367           45,230      71,748
# No            2.7%   36.2%           1.9%            63.0%      100.0%

# In [12]: df[(df['Neither language'] == 1) & (df['Data career'] == 1)]['LanguageWorkedWith'
#     ...: ].str.get_dummies(sep=';').sum().sort_values(ascending=False)
# Out[12]:
# SQL                      3766
# JavaScript               3722
# HTML/CSS                 3657
# Java                     2359
# C#                       2206
# Bash/Shell/PowerShell    1769
# PHP                      1695
# C++                      1244
# TypeScript               1120
# C                        1102
# Other(s):                 789
# VBA                       657
# Assembly                  392
# Swift                     294
# Ruby                      292
# Go                        278
# Kotlin                    263
# Scala                     261
# Objective-C               245
# Rust                       99
# Clojure                    86
# Dart                       81
# Elixir                     73
# WebAssembly                68
# Erlang                     60
# F#                         58
# dtype: int64
