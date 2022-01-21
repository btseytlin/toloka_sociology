import os

import pandas as pd

if __name__ == '__main__':
    df = pd.read_excel('data/raw_answers/male_29.xlsx')
    question_col = 'Согласны ли вы с утверждением: Религия играет важную роль в моей жизни.'
    df[question_col] = df[question_col].str.replace('согласнен', 'согласен')
    bad_column = '"Насколько вы согласны с утверждением (1 - полностью НЕ согласен, \n10 - полностью согласен)"" / Религия играет важную роль в моей жизни'
    correct_column = '"Насколько вы согласны с утверждением (1 - полностью НЕ согласен, \n10 - полностью согласен)"" / Религия НЕ играет важную роль в моей жизни'

    df = df.rename(columns={bad_column: correct_column})
    df[correct_column] = 11 - df[correct_column]

    df.to_csv('data/intermediate/male_29.csv', index=False)

    for entry in os.scandir('data/raw_answers'):
        if entry.name.endswith('male_29.xlsx'):
            continue

        if entry.name.endswith('.xlsx'):
            df = pd.read_excel(entry.path)
            basename = entry.name.split('.')[0]
            df.to_csv(f'data/intermediate/{basename}.csv', index=False)
