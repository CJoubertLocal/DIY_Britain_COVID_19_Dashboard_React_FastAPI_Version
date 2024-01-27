import data_processing.data_processing as dp
import data_files.load_from_files as lff
import phe_api_caller.phe_api_caller as pac
from json import dumps as json_dumps
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/transmission-data")
def get_transmission_chart_data_from_json_files():
    return json_dumps(dp.get_transmission_data())

@app.get("/transmission-write-up")
def get_transmission_write_up_html():
    return json_dumps(lff.get_html_from_file('./data_files/transmission_write_up.html'))

@app.get("/vaccination-chart-data")
def get_vaccination_chart_data_from_json_files():
    return json_dumps(dp.get_vaccine_data_without_double_counting())
    
@app.get("/vaccination-write-up")
def get_vaccination_write_up_html():
    return json_dumps(lff.get_html_from_file('./data_files/vaccination_write_up.html'))

@app.get("/utla-cumulative-death-data")
def get_utla_cumulative_death_data():
    return json_dumps(dp.
    get_json_utla_cumulative_death_data())

@app.get("/utla-cumulative-death-write-up")
def get_utla_cumulative_death_write_up_html():
    return json_dumps(lff.get_html_from_file('./data_files/utla_cumulative_death_write_up.html'))

@app.get("/update-transmission-datasets")
def update_transmission_datasets():
    res = pac.update_PHE_transmission_datasets()
    if res:
        return json_dumps("Update succeeded!")
    else:
        return json_dumps("Update failed!")
    
@app.get("/update-vaccination-datasets")
def update_vaccination_datasets():
    res = pac.update_PHE_vaccination_datasets()
    if res:
        return json_dumps("Update succeeded!")
    else:
        return json_dumps("Update failed!")

@app.get("/update-utla-datasets")
def update_utla_datasets():
    print("updating utla data")
    res = pac.update_utla_death_data()
    if res:
        return json_dumps("Update succeeded!")
    else:
        return json_dumps("Update failed!")