import services from "./services"

/*
  Assumes data = {
    column_names: [],
    date_values: [], 
    data: {
      series_one: [{}],
      series_two: [{}],
      ...
    }
  }
*/
const ExtractAndSetData = (dt, setterFunc) => {
    const temp = {
        dateValues: dt.date_values,
        series: {}
      }
      for (const property in dt.data) {
        temp.series[property] = JSON.parse(dt.data[property])
      }
      setterFunc(temp)
}

// Use async-await to force the app to wait for the datasets to be updated from PHE
// before calling the server for updated data.
const UpdateTransmissionDatasets = async (setTransmissionData) => {
    await services.updateTransmissionDataset()
    services.getTransmissionTimeSeries().then(tr => {
        ExtractAndSetData(tr, setTransmissionData)
    })
}

const UpdateVaccinationDatasets = async (setVaccinationData) => {
    await services.updateVaccinationDataset()
    services.getVaccinationTimeSeries().then(vts => {
        console.log("vts", vts)
        ExtractAndSetData(vts, setVaccinationData)
    })  
}

const UpdateUTLACumulativeDeathData = async (setUtlaDeathData) => {
    await services.updateUTLACumulativeDeathsDataset()
    services.getUTLACumulativeDeathData().then(utlaData => {
        ExtractAndSetData(utlaData, setUtlaDeathData)
      })
}

export default {
    ExtractAndSetData: ExtractAndSetData,
    UpdateTransmissionDatasets: UpdateTransmissionDatasets,
    UpdateVaccinationDatasets: UpdateVaccinationDatasets,
    UpdateUTLACumulativeDeathData: UpdateUTLACumulativeDeathData
}