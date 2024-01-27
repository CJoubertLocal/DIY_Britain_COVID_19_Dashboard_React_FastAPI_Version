import pandas as pd
import json
import typing
from phe_api_caller.phe_api_helper import utla_region_list
from os import listdir as os_listdir

def save_dictionary_data_to_JSON_file(
    dictionary_to_save: typing.Dict, 
    file_name_with_json_extension: str
) -> ():
    with open(file_name_with_json_extension, "wt") as OUTF:
        json.dump(dictionary_to_save, OUTF)

# Returns JSON type
def read_JSON_file(file_name_with_json_extension: str) -> str:
    with open(file_name_with_json_extension, "rt") as INFILE:
        variable_to_return = json.load(INFILE)

    return variable_to_return

def load_JSON_file_as_pd_dataframe(file_name_with_json_extension: str) -> pd.DataFrame:
    return pd.DataFrame.from_dict(
        read_JSON_file(
            file_name_with_json_extension
        )['data']
    )

def save_dataframe_to_pickle(
        dataframe_to_save: pd.DataFrame, 
        name_of_file_to_save_with_file_extension: str) -> ():
    dataframe_to_save.to_pickle(name_of_file_to_save_with_file_extension)

def load_dataframe_from_pickle(file_name_with_extension: str) -> pd.DataFrame:
    return pd.read_pickle(file_name_with_extension)

def get_html_from_file(file_name_with_extension: str) -> str:
    with open(file_name_with_extension) as INFILE:
        html_to_return = INFILE.read()
    return html_to_return


"""
Input:
    A date value as a string, in the format YYYY-MM-DD.
Output:
    A pandas datetime object based on the input date.
"""
def convert_to_pandas_datetime(date_values) -> pd.Timestamp:
    return pd.to_datetime(date_values, format="%Y-%m-%d")

def load_data_from_utla_files_and_store_in_pandas_dataframe():
    list_of_pandas_dates_for_utla_deaths = create_pandas_date_index_for_utla_data()

    utla_deaths_df_to_return = pd.DataFrame(
        columns = utla_region_list, 
        index = list_of_pandas_dates_for_utla_deaths
    )

    list_of_files_in_directory = os_listdir()

    for file_name in list_of_files_in_directory:
        if file_name[0:4] == "utla":
            with open(file_name, "rt") as INFILE:
                utla_file_data = json.load(INFILE)
                try:
                    current_utla_area_name = utla_file_data["data"][0]["area_name"]

                    # Fill in the utla cumulative deaths dataframe
                    for entry in utla_file_data["data"]:
                        date = convert_to_pandas_datetime(entry["date"])

                        if pd.isna(
                            utla_deaths_df_to_return.loc[date, current_utla_area_name]
                        ):
                            # Assume that any instances of None were before any deaths were recorded in that area
                            value = (
                                float(entry["cumulative_deaths_28_days"])
                                if entry["cumulative_deaths_28_days"] != None
                                else 0
                            )
                            utla_deaths_df_to_return.loc[
                                date, current_utla_area_name
                            ] = value

                except:
                    continue

    return utla_deaths_df_to_return

def create_pandas_date_index_for_utla_data() -> typing.List:
    list_of_pandas_dates_for_utla_deaths = (
        generate_pandas_dataframe_with_start_date_and_end_date(
            start_date=pd.to_datetime("2020-02-01", format="%Y-%m-%d"),
            end_date=pd.to_datetime("today").normalize(),
            frequency_to_generate="D",
        )
    )

    return list_of_pandas_dates_for_utla_deaths


"""
Input:
    Preferred start date as a pandas datetime object,
    Preferred end date as a pandas datetime object,
    Desired frequency ('D' for day, 'W' for week, 'M' for month).
Output:
    A series of pandas datetime objects from the start to the end date at the preferred frequency.
"""
def generate_pandas_dataframe_with_start_date_and_end_date(
    start_date: str, end_date: str, frequency_to_generate: str="D"
) -> pd.DataFrame:
    return pd.date_range(start_date, end_date, freq=frequency_to_generate)

# Get list of area names for dataframe
def create_list_of_utla_names() -> typing.List:
    list_of_utla_names = []
    list_of_files_in_directory = os_listdir()
    i = 0
    for file_name in list_of_files_in_directory:
        if file_name[0:4] == "utla" and file_name.find("death_rates") != -1:
            with open(file_name, "rt") as INFILE:
                utla_file_data = json.load(INFILE)
                try:
                    current_utla_area_name = utla_file_data["data"][0]["area_name"]
                    list_of_utla_names.append(current_utla_area_name)
                except:
                    # If a utla json file was created due to the query succeeding, but PHE had no data, then skip.
                    continue

    return list_of_utla_names