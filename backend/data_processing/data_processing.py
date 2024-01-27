import data_files.data_file_names as df 
from data_files.data_file_names import vaccination_percentage_list_shorthands as vps
import data_files.load_from_files as lff
from typing import List, Dict
import pandas as pd

"""

"""
def convert_date_col_to_datetime(dataframe_in: pd.DataFrame) -> pd.DataFrame:
    dataframe_in['date'] = pd.to_datetime(dataframe_in['date'])
    return dataframe_in


def create_pandas_time_series_for_earliest_to_latest_dates(list_of_data_frames: List, name_of_date_col: str) -> List:
    earliest_date = min(
        [x[name_of_date_col].min() for x in list_of_data_frames]
    )

    latest_date = max(
        [x[name_of_date_col].max() for x in list_of_data_frames]
    )

    return pd.date_range(
        start=earliest_date, 
        end=latest_date
    ).astype(str).to_list()

"""
Purpose:
    Prepare a pandas dataframe of vaccination percentages for a stacked line chart.
    Indicate what remainder of people have had a first vaccination, but not a second,
    and what remainder of people have had a second vaccination, but not a third. 

Input:
    A pandas dataframe, where the names of the columns are the same as the values
    in the vaccination_percentage_list_shorthands dict.

Output:
    A list of lists. Each list represents values in the column.
    The percentage of second vaccinations is subtracted from the first,
    The percentage of third vaccinations is subtracted from the second.

Note:
    ffill is used to write over unknown, future values. I assume here that a constant
    proportion of the population retains a vaccination status after it has been achieved
    (i.e. if 30% of the population received the third vaccination, then I assume that 
    continues to be the case into the future).
    For improvements, these values should decline based on the deaths of those with and 
    without a given number of vaccinations. I rely on Public Health England to have made
    these adjustments.
"""
def get_vaccination_data_as_dataframe(path_to_data_files: str, country_name: str) -> pd.DataFrame:
    vaccination_dataframe = convert_date_col_to_datetime(
        lff.load_JSON_file_as_pd_dataframe(
            f'{path_to_data_files}{df.vaccination_data_files[country_name]}'
        )
    )

    vaccination_dataframe.sort_values(
        by=['date'], 
        ascending=True, 
        inplace=True
    )
    vaccination_dataframe = vaccination_dataframe.reset_index(drop=True)

    vaccination_dataframe = vaccination_dataframe.replace('null', pd.NA).ffill()
    vaccination_dataframe = remove_double_counting_for_vaccination_figures(vaccination_dataframe)

    vaccination_dataframe['date'] = vaccination_dataframe['date'].astype(str)
    
    col_rename_mapper = {
        "percentage_first_vaccinations": country_name + " First Vaccination",
        "percentage_second_vaccinations": country_name + " Second Vaccination",
        "percentage_third_vaccinations": country_name + " Third Vaccination"
    }
    vaccination_dataframe.rename(mapper=col_rename_mapper, axis='columns', inplace=True)

    return vaccination_dataframe

def remove_double_counting_for_vaccination_figures(vac_data_frame):
    vac_data_frame[vps['f']] = vac_data_frame[vps['f']]\
        .sub(vac_data_frame[vps['s']], fill_value=0)
    vac_data_frame[vps['s']] = vac_data_frame[vps['s']]\
        .sub(vac_data_frame[vps['t']], fill_value=0)

    return vac_data_frame

def get_vaccine_data_without_double_counting():
    england_data: pd.DataFrame = get_vaccination_data_as_dataframe(
        './data_files/', 'England'
    )
    scotland_data: pd.DataFrame = get_vaccination_data_as_dataframe(
        './data_files/', 'Scotland'
    )
    wales_data: pd.DataFrame = get_vaccination_data_as_dataframe(
        './data_files/', 'Wales'
    )

    date_values = create_pandas_time_series_for_earliest_to_latest_dates(
        [
            england_data,
            scotland_data,
            wales_data
        ],
        'date'
    )
    
    json_to_return = {
        'date_values': date_values,
        'data': {
            'england': england_data.to_json(orient='records'),
            'scotland': scotland_data.to_json(orient='records'),
            'wales': wales_data.to_json(orient='records')
        }
    }

    return json_to_return

def get_transmission_data_and_ffill(path_to_file, country_name):
    transmission_df: pd.DataFrame = convert_date_col_to_datetime(
        lff.load_JSON_file_as_pd_dataframe(
            f'{path_to_file}{df.transmission_data_files[country_name]}'
        )
    )

    col_rename_mapper: Dict = {
        'transmission_min_growth_rate': country_name + ' min',
        'transmission_max_growth_rate': country_name + ' max'
    }

    transmission_df.rename(
        mapper=col_rename_mapper, 
        axis='columns', 
        inplace=True
    )

    transmission_df.sort_values(by=['date'], ascending=True, inplace=True)

    transmission_df[country_name + ' min'].fillna(
        value=transmission_df[country_name +' max'], 
        inplace=True
    )
    transmission_df[country_name + ' max'].fillna(
        value=transmission_df[country_name + ' min'], 
        inplace=True
    )

    transmission_df.ffill(inplace=True)

    return transmission_df

def get_transmission_data() -> Dict:
    england_data: pd.DataFrame = get_transmission_data_and_ffill(
            './data_files/', 'England'
    )
    
    scotland_data: pd.DataFrame = get_transmission_data_and_ffill(
            './data_files/', 'Scotland'
    )

    wales_data: pd.DataFrame = get_transmission_data_and_ffill(
            './data_files/', 'Wales'
    )
    
    date_values = create_pandas_time_series_for_earliest_to_latest_dates(
        [
            england_data,
            scotland_data,
            wales_data
        ],
        'date'
    )
    
    england_data['date'] = england_data['date'].astype(str)
    scotland_data['date'] = scotland_data['date'].astype(str)
    wales_data['date'] = wales_data['date'].astype(str)

    data_to_return = {
        "date_values": date_values,
        "data": {
            "england": england_data.to_json(orient='records'),
            "scotland": scotland_data.to_json(orient='records'),
            "wales": wales_data.to_json(orient='records')
        }
    }

    return data_to_return

def get_json_utla_cumulative_death_data() -> Dict:
    utla_df = lff.load_dataframe_from_pickle(df.path_to_data_files + df.utla_pickle_file_name)
    utla_df['date'] = utla_df.index.astype('str')
    utla_df = utla_df[utla_df.columns.to_list()[-1:] + utla_df.columns.to_list()[:-1]]

    data_to_return = {
        "date_values": utla_df['date'].to_list(),
        "data": {
            "series": utla_df.to_json(orient='records')
        }
    }
    
    return data_to_return
