from uk_covid19 import Cov19API
import time
import data_files.load_from_files as lff
import phe_api_caller.phe_api_helper as pah
from random import randint
import pandas as pd


# --------------------------------------------------------------------
# Data fetching, saving, and loading functions
# 
# Included below are a list of helper functions used to query PHE for new data, save that
# data to json files or pickles (in the case of UTLA data), convert the data into pandas 
# dataframes, and plot the data.
#
# --------------------------------------------------------------------

"""
Sends a query to the PHE API and returns the JSON data.

This function causes the program to sleep for 1 second after calling the API, to
avoid sending too many individual queries in too short a time frame.

Input:
    The filters used to query for data from PHE,
    The structure of the data to request,
    Please see the documentation: 
        https://coronavirus.data.gov.uk/details/developers-guide/main-api#query-parameters
Output:
    The JSON data from PHE, provided from the API in the python structures:
        dictionary { list [ dictionary{} ] }
"""
def query_public_health_england_API_for_data(
    filters_to_query_with, structure_to_query_with
    ):
    time.sleep(1)
    api = Cov19API(
        filters=filters_to_query_with,
        structure=structure_to_query_with
    )
    data_from_api = api.get_json()
    return data_from_api

def query_PHE_and_save_to_JSON(
    filters_to_query_with, 
    structure_to_query_with, 
    file_name_with_json_extension
    ):

    data_from_api = query_public_health_england_API_for_data(
        filters_to_query_with, 
        structure_to_query_with
    )
    lff.save_dictionary_data_to_JSON_file(
        data_from_api, 
        './data_files/' + file_name_with_json_extension
    )

    return data_from_api

def update_dataset_helper(
        dict_of_file_name_to_filters, 
        structure_for_phe
    ) -> bool:
    for file_name in dict_of_file_name_to_filters:
        try:
            query_PHE_and_save_to_JSON(
                dict_of_file_name_to_filters[file_name],
                structure_for_phe,
                file_name,
            )
            print(f"saved {file_name}")
        
        except BaseException as e:
            print(e)
            return False
    
    return True

def update_PHE_vaccination_datasets() -> bool:
    print("updating vaccination datasets")
    
    vaccination_rate_file_name_to_filters = {
        "england_vaccination_percentages.json": pah.filter_region_nation_england,
        "wales_vaccination_percentages.json": pah.filter_region_nation_wales,
        "scotland_vaccination_percentages.json": pah.filter_region_nation_scotland
    }

    return update_dataset_helper(
        vaccination_rate_file_name_to_filters, 
        pah.vaccination_percentages_structure
    )

"""
This function is used to query PHE for new transmission data in England, Scotland, and Wales.

It responds to a button being pressed, and then runs multiple functions to query PHE.

Data from PHE is then saved to json files, overwriting the current files.

The function sleeps for 1 second between each function call, to avoid sending too many requests to PHE too quickly.

On success, it return 'True', else 'False'.

"""
def update_PHE_transmission_datasets() -> bool:
    print("updating transmission datasets")
    
    transmission_rate_file_name_to_filters = {
        "england_transmission_rates.json": pah.filter_region_nation_england,
        "wales_transmission_rates.json": pah.filter_region_nation_wales,
        "scotland_transmission_rates.json": pah.filter_region_nation_scotland,
    }

    return update_dataset_helper(
        transmission_rate_file_name_to_filters, 
        pah.structure_for_transmission_rates
    )

"""
This function is used to query PHE for new data.
It responds to a button being pressed, and then runs multiple functions to query PHE.
Data from PHE is then saved to json files, overwriting the current files.
The function sleeps for 1 second between each function call, to avoid sending too many requests to PHE too quickly.
"""
def update_PHE_datasets() -> bool:
    print("updating phe datasets")
    res = update_PHE_vaccination_datasets()
    if not res: return False

    res = update_PHE_transmission_datasets()
    if not res: return False

    return True

"""
    WARNING:
        These functions query PHE once for each UTLA area.
        To avoid sending too many queries to PHE too quickly, the function will wait for 1 to 5 seconds between making one query and then making another query.
    """
def fetch_updated_utla_death_rate_data_from_PHE() -> bool:
    print("fetching utla data from phe")

    for utla_region in pah.utla_region_list:
        # Wait for a period of 1 to 5 seconds between queries, to avoid overloading PHE
        time.sleep(randint(1, 5))

        try:
            query_PHE_and_save_to_JSON(
                ["areaType=utla", "areaName=" + utla_region],
                pah.structure_for_utla_death_rates,
                "utla_" + str(utla_region).lower() + "_death_rates.json",
            )
        
        except BaseException as e:
            print(e)
            return False
    
    return True


"""
Removes all NaN values from the UTLA pandas dataframe.

Assumptions:
    All NaN values from before deaths were first recorded are set to 0.0.
    All NaN values afterwards simply carry over the cumulative death count.

Input:
    The UTLA dataframe to be changed.

Output:
    A new pandas dataframe with all NaN values in the original dataframe replaced in line with the assumptions above.
"""
def remove_nan_values_from_ulta_death_frame(utla_deaths_df_in):
    for utla_name in utla_deaths_df_in:
        for date_value in utla_deaths_df_in.index:

            try:
                if pd.isna(utla_deaths_df_in.loc[date_value, utla_name]):
                    if (
                        utla_deaths_df_in.loc[
                            date_value - time.datetime.timedelta(days=1), utla_name
                        ]
                        > 0
                    ):
                        utla_deaths_df_in.loc[
                            date_value, utla_name
                        ] = utla_deaths_df_in.loc[
                            date_value - time.datetime.timedelta(days=1), utla_name
                        ]
                    else:
                        utla_deaths_df_in.loc[date_value, utla_name] = 0.0

            except:
                utla_deaths_df_in.loc[date_value, utla_name] = 0.0

    return utla_deaths_df_in

"""
WARNING: 
    This operation takes a significant amount of time, and should not be used unless necessary.

Data is received from PHE and saved to JSON files, it is then reloaded into memory, wrangled into a pandas dataframe and saved to a pickle.
The purpose of saving this to a pickle is to avoid having to open over 100 json files and wrangle the data within them into a pandas dataframe each time the dashboard is loaded.

TODO: Change this so that it stores data in memory rather than in JSON files.
"""
def update_utla_death_data() -> bool:
    res = fetch_updated_utla_death_rate_data_from_PHE()
    if not res:
        return False

    utla_deaths_df_updated_with_json = (
        lff.load_data_from_utla_files_and_store_in_pandas_dataframe()
    )

    utla_deaths_df_nans_removed = remove_nan_values_from_ulta_death_frame(
        utla_deaths_df_updated_with_json
    )

    lff.save_dataframe_to_pickle(utla_deaths_df_nans_removed, "ulta_deaths_pickle.pkl")

    return True
