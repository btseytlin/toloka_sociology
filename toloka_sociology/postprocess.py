import os
import pandas as pd

def fix_demographics(df):
    for i, row in enumerate(df.itertuples()):
        if row.invalid_age:
            self_reported_age = row[5]
            if self_reported_age == '30-49' and row.source_age == '29':
                df.at[row.Index, 'source_age'] = '30-49'
                df.at[row.Index, 'invalid_age'] = False
            elif self_reported_age == 'более 50' and row.source_age == '30-49':
                df.at[row.Index, 'source_age'] = '50+'
                df.at[row.Index, 'invalid_age'] = False
    return df


def get_age(row):
    if row.source == 'ours':
        if (row['Источник ответов'] == 'female_50') or (row['Источник ответов'] == 'male_50'):
            return '50+'
        if (row['Источник ответов'] == 'female_30_49') or (row['Источник ответов'] == 'male_30_49'):
            return '30-49'
        if (row['Источник ответов'] == 'female_29') or (row['Источник ответов'] == 'male_29'):
            return '29'
    elif row.source == 'world_values_survey':
        if row['Q262: Age'] <= 29:
            return '29'
        if row['Q262: Age'] <= 49:
            return '30-49'
        return '50+'


def get_sex(row):
    if row.source == 'ours':
        if 'female' in row['Источник ответов']:
            return 'female'
        return 'male'
    elif row.source == 'world_values_survey':
        if row['Q260: Sex'] == 2:
            return 'female'
        return 'male'


def encode_self_reported_age(row):
    encoding = {
        'до 29': '29',
        '30-49': '30-49',
        'более 50': '50+',
    }

    if row.source == 'ours':
        return encoding[row['Сколько вам лет?']]
    elif row.source == 'world_values_survey':
        if row['Q262: Age'] <= 29:
            return '29'
        if row['Q262: Age'] <= 49:
            return '30-49'
        return '50+'


def encode_self_reported_sex(row):
    encoding = {
        'Мужской': 'male',
        'Женский': 'female',
    }

    if row.source == 'ours':
        return encoding[row['Ваш пол']]
    elif row.source == 'world_values_survey':
        if row['Q260: Sex'] == 2:
            return 'female'
        return 'male'


def postprocess(input_dir_path, output_dir_path, wvs_excel_path):
    dfs = []
    for entry in os.scandir(input_dir_path):
        if entry.name.endswith('.csv'):
            group_df = pd.read_csv(entry.path)
            dfs.append(group_df)
    df_our = pd.concat(dfs)

    df_wvs = pd.read_excel(wvs_excel_path)
    df_wvs = df_wvs[df_wvs.columns[1:]]  # Remove unnamed column

    df_our['source'] = 'ours'
    df_wvs['source'] = 'world_values_survey'
    df = pd.concat([df_our, df_wvs])

    df['source_age'] = df.apply(get_age, axis=1)
    df['source_sex'] = df.apply(get_sex, axis=1)

    #df = fix_demographics(df)

    df['self_reported_age'] = df.apply(encode_self_reported_age, axis=1)
    df['self_reported_sex'] = df.apply(encode_self_reported_sex, axis=1)

    df.to_csv(os.path.join(output_dir_path, 'final.csv'), index=False)


if __name__ == '__main__':
    postprocess('./data/encoded', './data/final', './data/world_values_survey_extended.xlsx')