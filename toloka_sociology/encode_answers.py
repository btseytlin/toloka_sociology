import os
import pandas as pd


def unwanted_neighbor(row):
    if pd.isnull(row):
        a = 2
    else:
        a = 1
    return a


def male_preference(value):
    preference_map = {
        'Полностью согласен': 1,
        'Скорее согласен': 2,
        'Скорее не согласен': 3,
        'Полностью не согласен': 4,
        'Затрудняюсь ответить': -1,
    }

    return preference_map[value]


def homosexual_couples(value):
    answer_map = {
        'Полностью согласен': 1,
        'Скорее согласен': 2,
        'Ни согласен, ни несогласен': 3,
        'Скорее не согласен': 4,
        'Полностью не согласен': 5,
        'Затрудняюсь ответить': -1,
    }
    return answer_map[value]


def strike(value):
    answer_map = {
        'Уже посещал': 1,
        'Мог бы посетить': 2,
        'Никогда бы не посетил': 3,
        'Затрудняюсь ответить': -1,
    }
    return answer_map[value]


def institution_trust(value):
    answer_map = {
        'Полностью доверяю': 1,
        'Скорее доверяю': 2,
        'Скорее не доверяю': 3,
        'Полностью не доверяю': 4,
        'Затрудняюсь ответить': -1,
        'Абсолютно доверяю': 1,
        'Абсолютно не доверяю': 4
    }
    return answer_map[value]


def election_fraud(value):
    answer_map = {
        'Очень часто': 1,
        'Скорее часто': 2,
        'Не очень часто': 3,
        'Совсем не часто': 4,
        'Затрудняюсь ответить': -1,
    }
    return answer_map[value]


def immigration(value):
    answer_map = {
        'Мы должны пускать всех желающих': 1,
        'Пускать всех желающих до тех пор, пока есть рабочие места': 2,
        'Установить жесткие ограничения на количество иностранцев, которые могут сюда приехать': 3,
        'Запретить приезжать сюда из других стран': 4,
        'Затрудняюсь ответить': -1,
    }
    return answer_map[value]


def party(value):
    if value == 'Единая Россия':
        encoded = 1
    else:
        encoded = 0
    return encoded


def encode_answers(input_dir_path, output_dir_path):
    for entry in os.scandir(input_dir_path):
        if entry.name.endswith('.csv'):
            fpath = entry.path
            group_name = entry.name.replace('.csv', '')
            df = pd.read_csv(fpath)
            df = df[df['Источник ответов'] == group_name]

            df['Q18: Neighbors: Drug addicts'] = df[
                'Кого бы вы НЕ хотели видеть своим соседом? / Наркозависимого'].apply(unwanted_neighbor)
            df['Q19: Neighbors: People of a different race'] = df[
                'Кого бы вы НЕ хотели видеть своим соседом? / Человека другой расы'].apply(unwanted_neighbor)
            df['Q22: Neighbors: Homosexuals'] = df['Кого бы вы НЕ хотели видеть своим соседом? / Гомосексуала'].apply(
                unwanted_neighbor)
            df['Q21: Neighbors: Immigrants/foreign workers'] = df[
                'Кого бы вы НЕ хотели видеть своим соседом? / Иммигранта'].apply(unwanted_neighbor)
            df['Q23: Neighbors: People of a different religion'] = df[
                'Кого бы вы НЕ хотели видеть своим соседом? / Человека другой религии'].apply(unwanted_neighbor)

            df['Q29: Men make better political leaders than women do'] = df[
                'Согласны ли вы с утверждением: В целом, из мужчин получаются более хорошие политические лидеры, чем из женщин?'].apply(
                male_preference)

            df['Q36: Homosexual couples are as good parents as other couples'] = df[
                'Согласны ли вы с утверждением: Гомосексуальные пары такие же хорошие родители, как и другие пары?'].apply(
                homosexual_couples)

            df['Q212: Political action: Joining unofficial strikes'] = df[
                'Могли бы вы посетить несанкционированный политический митинг?'].apply(strike)

            df['Q71: Confidence: The Government'] = df['Доверяете ли вы Правительству?'].apply(institution_trust)
            df['Q69: Confidence: The Police'] = df['Доверяете ли вы полиции?'].apply(institution_trust)
            df['Q80: Confidence: The Women´s Movement'] = df['Доверяете ли вы движениям за женские права?'].apply(institution_trust)

            df['Q227: How often in country´s elections: Voters are bribed'] = df[
                'По вашему мнению, как часто в вашей стране фальсифицируют выборы?'].apply(election_fraud)

            df['Q130: Immigration policy preference'] = df[
                'По вашему мнению, какой должна быть иммиграционная политика?'].apply(immigration)

            df['Q223: Which party would you vote for if there were a national election tomorrow'] = df[
                'За какую партию вы бы проголосовали, если бы выборы были бы завтра?'].apply(party)

            column_map = {
                'Насколько вы согласны с утверждением (1 - полностью НЕ согласен, \n10 - полностью согласен) / Для мужчины оправдано ударить свою жену': 'Q189: Justifiable: For a man to beat his wife',
                'Насколько вы согласны с утверждением (1 - полностью НЕ согласен, \n10 - полностью согласен) / Гомосексуализм - это норма': 'Q182: Justifiable: Homosexuality',
                'Насколько вы согласны с утверждением (1 - полностью НЕ согласен, \n10 - полностью согласен) / Проституция может быть оправдана': 'Q183: Justifiable: Prostitution',
                'Насколько вы согласны с утверждением (1 - полностью НЕ согласен, \n10 - полностью согласен) / Аборт может быть оправдан': 'Q184: Justifiable: Abortion',
                'Насколько вы согласны с утверждением (1 - полностью НЕ согласен, \n10 - полностью согласен) / Родители могут ударить своего ребёнка': 'Q190: Justifiable: Parents beating children',
                'Насколько вы согласны с утверждением (1 - полностью НЕ согласен, \n10 - полностью согласен) / Секс до брака - это норма': 'Q186: Justifiable: Sex before marriage',
                'Насколько вы согласны с утверждением (1 - полностью НЕ согласен, \n10 - полностью согласен) / Самоубийство может быть оправдано': 'Q187: Justifiable: Suicide',
                'Насколько вы согласны с утверждением (1 - полностью НЕ согласен, \n10 - полностью согласен) / Эвтаназия может быть оправдана': 'Q188: Justifiable: Euthanasia',
                'Насколько вы согласны с утверждением (1 - полностью НЕ согласен, \n10 - полностью согласен) / Случайные половые связи могут быть оправданы': 'Q193: Justifiable: Having casual sex'
            }

            for new_name, original_name in column_map.items():
                df[original_name] = df[new_name]

            df.to_csv(f'{output_dir_path}/{group_name}.csv', index=False)


if __name__ == '__main__':
    encode_answers('./data/processed', './data/encoded')
