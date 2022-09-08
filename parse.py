from typing import TypedDict

import json
from pathlib import Path

import pandas as pd
from tqdm import tqdm as progress_bar
import click
 

class MetaDoesNotExistException(Exception):
    pass


class MetaInfo(TypedDict):
    provider : str
    wallet : str

columns = {
    "Game Name": "game_name",
    "Game Code": "game_code",
    "GameType": "type",
}

fallback_columns = {
    "Game  Name": "game_name",
    "Game Code": "game_code",
    "GameType": "type",
}


def get_meta_info(df: pd.DataFrame, col_index: int):
    while pd.isna(df.iloc[0][col_index]):
        col_index -=1
        if col_index < 0:
            raise MetaDoesNotExistException()

    return MetaInfo(
        provider=df.iloc[1][col_index],
        wallet=df.iloc[0][col_index],
    )


def process_strings(df: pd.DataFrame) -> pd.DataFrame:
    df['type'] = df['type'].str.lower()
    df['game_code'] = df['game_code'].str.replace('\t', '')
    df['game_name'] = df['game_name'].str.replace('\t', '')
    df['game_name'] = df['game_name'].str.replace('\u00a0', ' ')
    df['game_name'] = df['game_name'].str.replace('\u200b', '')
    df['game_name'] = df['game_name'].str.replace('\u2019S', '`')
    df['game_name'] = df['game_name'].str.replace('\u2019s', '`')
    df['game_name'] = df['game_name'].str.replace('\u2122', '')  # Trade mark
    return df


@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), default=Path('output.json'), show_default=True)
def main(input: Path, output: Path):
    result = { 'data': [] }

    with open(input, 'rb') as input:
        xl = pd.ExcelFile(input)
        for sheet in progress_bar(xl.sheet_names):
            progress_bar.write(sheet)
            meta_df = pd.read_excel(input, sheet, header=None, nrows=2)
            
            last_col_index = meta_df.columns.to_list()[-1]
            meta_info = get_meta_info(meta_df, last_col_index)

            try:
                data_df = pd.read_excel(
                    input, sheet, header=2, usecols=columns.keys()
                ).rename(columns=columns)
            except ValueError:
                data_df = pd.read_excel(
                    input, sheet, header=2, usecols=fallback_columns.keys()
                ).rename(columns=fallback_columns)

            data_df = data_df[data_df['game_code'].notnull()]
            data_df = process_strings(data_df)

            for data_type in data_df['type'].unique():
                if pd.isna(data_type):
                    games = data_df[data_df['type'].isna()]
                else:
                    games = data_df[data_df['type'] == data_type]
                result['data'].append({
                    'provider': meta_info['provider'],
                    'type': "N/A" if pd.isna(data_type) else data_type,
                    'wallet': meta_info['wallet'],
                    'games': games[['game_name', 'game_code']].to_dict('records')
                })

    with open(output, 'w') as output:
        json.dump(result, output, indent=2)


if __name__ == '__main__':
    main()
