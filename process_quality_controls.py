import pandas as pd
import numpy as np
import os

INPUT_DIR = 'data/intermediate'

ages_expected = {
    'male_29': 'до 29',
    'female_29': 'до 29',
    'male_30_49': '30-49',
    'female_30_49': '30-49',
    'male_50': 'более 50',
    'female_50': 'более 50',
}

sexes_expected = {
    'male_29': 'Мужской',
    'female_29': 'Женский',
    'male_30_49': 'Мужской',
    'female_30_49': 'Женский',
    'male_50': 'Мужской',
    'female_50': 'Женский',
}


def control_sex_preference(df):
    # Map raw_answers to numbers from 0 to 4
    # 0 - uncertain
    # 1 - full female preference
    # 4 - full male preference
    question_col = 'Согласны ли вы с утверждением: В целом, из мужчин получаются более хорошие политические лидеры, чем из женщин?'
    reverse_question_col = 'Согласны ли вы с утверждением: Среди политических лидеров женщины более компетентны, чем мужчины'
    range_question_col = '"Насколько вы согласны с утверждением (1 - полностью НЕ согласен, \n10 - полностью согласен)"" / Мужчины лучше справляются с ответственными должностями'

    question_answers = ['Затрудняюсь ответить', 'Полностью не согласен', 'Скорее не согласен', 'Скорее согласен',
                        'Полностью согласен', ]
    question_to_male_preference = {k: i for i, k in enumerate(question_answers)}
    reverse_question_answers = ['Затрудняюсь ответить', 'Абсолютно не согласен', 'Скорее не согласен',
                                'Скорее согласен', 'Абсолютно согласен']
    reverse_question_to_male_preference = {k: 5 - i for i, k in enumerate(reverse_question_answers)}
    reverse_question_to_male_preference['Затрудняюсь ответить'] = 0
    range_question_to_male_pereference = df[range_question_col] // 3 + 1

    male_preference_question = df[question_col].apply(lambda x: question_to_male_preference[x])
    male_preference_reverse_question = df[reverse_question_col].apply(lambda x: reverse_question_to_male_preference[x])
    male_preference_range = range_question_to_male_pereference

    is_uncertain_question = (df[question_col] == 'Затрудняюсь ответить')
    is_uncertain_reverse_question = (df[reverse_question_col] == 'Затрудняюсь ответить')

    # Control fails if person prefers one sex in one question, but other sex in another question
    # If the person is uncertain then we can't control

    sexism_control_df = df[[question_col, reverse_question_col, range_question_col]].copy()
    sexism_control_df['male_preference_question'] = male_preference_question
    sexism_control_df['male_preference_reverse_question'] = male_preference_reverse_question
    sexism_control_df['male_preference_range'] = male_preference_range
    sexism_control_df['is_uncertain_question'] = is_uncertain_question
    sexism_control_df['is_uncertain_reverse_question'] = is_uncertain_reverse_question
    sexism_control_df['distance_questions'] = (male_preference_question - male_preference_reverse_question).abs()
    sexism_control_df['distance_range'] = (male_preference_question - male_preference_range).abs()
    sexism_control_df['fails_uncertanity'] = (is_uncertain_question != is_uncertain_reverse_question)
    sexism_control_df['fails_question'] = sexism_control_df['distance_questions'] > 2
    sexism_control_df['fails_range'] = (~is_uncertain_question) & (sexism_control_df['distance_range'] > 2)
    sexism_control_df['fails_sexism'] = sexism_control_df['fails_uncertanity'] | sexism_control_df['fails_question'] | \
                                        sexism_control_df['fails_range']
    return sexism_control_df


def control_religion(df):
    # Map raw_answers to numbers from 0 to 4
    # 0 - uncertain
    # 1 - no religious preference
    # 4 - full religious preference
    question_col = 'Согласны ли вы с утверждением: Религия играет важную роль в моей жизни.'
    question_answers = ['Затрудняюсь ответить', 'Абсолютно не согласен', 'Скорее не согласен',
                        'Скорее согласен', 'Абсолютно согласен']

    question_answers_to_religion_preference = {k: i for i, k in enumerate(question_answers)}
    religion_preference_question = df[question_col].apply(lambda x: question_answers_to_religion_preference[x])

    range_question_col = '"Насколько вы согласны с утверждением (1 - полностью НЕ согласен, \n10 - полностью согласен)"" / Религия НЕ играет важную роль в моей жизни'
    religion_preference_range = 5 - (df[range_question_col] // 3 + 1)

    is_uncertain_question = (df[question_col] == 'Затрудняюсь ответить')

    religion_control_df = df[[question_col, range_question_col]].copy()
    religion_control_df['religion_preference_question'] = religion_preference_question
    religion_control_df['religion_preference_range'] = religion_preference_range
    religion_control_df['is_uncertain_question'] = is_uncertain_question
    religion_control_df['distance_range'] = (religion_preference_question - religion_preference_range).abs()
    religion_control_df['fails_question'] = (~is_uncertain_question) & (religion_control_df['distance_range'] > 1)
    religion_control_df['fails_uncertanity'] = (is_uncertain_question) & ((religion_preference_range - 2.5).abs() >= 1)
    religion_control_df['fails_religion'] = religion_control_df['fails_question'] | religion_control_df[
        'fails_uncertanity']

    return religion_control_df


def process_controls():
    for entry in os.scandir(INPUT_DIR):
        if entry.name.endswith('.csv'):
            fpath = entry.path
            group_name = entry.name.replace('.csv', '')
            age_expected = ages_expected[group_name]
            sex_expected = sexes_expected[group_name]

            df = pd.read_csv(fpath)
            df = df[df['Источник ответов'] == group_name]

            sexism_control_df = control_sex_preference(df)

            religion_control_df = control_religion(df)

            df['failed_sexism_check'] = sexism_control_df.fails_sexism
            df['failed_religion_check'] = religion_control_df.fails_religion
            df['invalid_age'] = (df['Сколько вам лет?'] != age_expected)
            df['invalid_sex'] = (df['Ваш пол'] != sex_expected)
            df['failed_control'] = df['failed_sexism_check'] | df['failed_religion_check']

            print('Group', group_name)
            print('\tTotal', df.shape[0])
            print('\tFailed sexism check', df['failed_sexism_check'].sum())
            print('\tFailed religion check', df['failed_religion_check'].sum())
            print('\tFailed any control', df['failed_control'].sum())
            print('\tInvalid age', df['invalid_age'].sum())
            print('\tInvalid sex', df['invalid_sex'].sum())
            print('\tAny issue', (df['invalid_sex'] | df['invalid_age'] | df['failed_control']).sum())
            print('\tPassed controls', df.shape[0] - df['failed_control'].sum(), f"{round(100*(df.shape[0] - df['failed_control'].sum())/df.shape[0], 1)}%")

            df.to_csv(f'data/processed/{group_name}.csv', index=False)


if __name__ == '__main__':
    process_controls()
