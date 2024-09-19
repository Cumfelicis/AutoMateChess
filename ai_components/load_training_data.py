import pandas as pd
import json
import concurrent.futures
import numpy as np


def to_array(string):
    return json.loads(string)


def load_data(index):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        df = pd.read_csv(f'D:/csv/{index}.csv')
        df['position'] = list(executor.map(to_array, df['position']))
        df['time_control'] = list(executor.map(to_array, df['time_control']))
        '''
        df['remaining_times'] = list(executor.map(lambda e: np.array(np.float32(e)), df['remaining_times']))
        df['elo'] = list(executor.map(lambda e: np.float32(e), df['elo']))
        df['time_spent'] = list(executor.map(lambda e: np.float32(e), df['time_spent']))
        '''
        df['other'] = df.apply(lambda row: np.append(row['time_control'], (row['elo'], row['remaining_times'])), axis=1)
    positions = np.array(list(df['position']))
    other = np.array(list(df['other']))
    time = np.array(list(df['time_spent']))

    return positions, other, time


if __name__ == '__main__':
    load_data(0)
