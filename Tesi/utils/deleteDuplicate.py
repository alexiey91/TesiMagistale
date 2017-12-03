import pandas as pd

toclean = pd.read_csv('TestTweetCsv.csv')
deduped = toclean.drop_duplicates(['Filtro','Sample'])
deduped.to_csv('myfilewithoutduplicates.csv')