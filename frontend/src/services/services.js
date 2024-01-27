import axios from 'axios'

const baseUrl = 'http://localhost:8080/'

const sendRequest = (urlToPing) => {
  return axios.get(urlToPing).then(response => response.data)
}

const getTransmissionTimeSeries = () => {
  return sendRequest(`${baseUrl}transmission-data`)
    .then(vts => JSON.parse(vts))
}

const getTransmissionWriteUp = () => {
  return sendRequest(`${baseUrl}transmission-write-up`)
    .then(vts => JSON.parse(vts))
}

const getVaccinationTimeSeries = () => {
  return sendRequest(`${baseUrl}vaccination-chart-data`)
    .then(vts => JSON.parse(vts))
}

const getVaccinationWriteUp = () => {
  return sendRequest(`${baseUrl}vaccination-write-up`)
    .then(vts => JSON.parse(vts))
}

const getUTLACumulativeDeathData = () => {
  return sendRequest(`${baseUrl}utla-cumulative-death-data`)
    .then(vts => JSON.parse(vts))
}

const getUTLAWriteUp = () => {
  return sendRequest(`${baseUrl}utla-cumulative-death-write-up`)
    .then(vts => JSON.parse(vts))
}

const updateVaccinationDataset = () => {
  return sendRequest(`${baseUrl}update-vaccination-datasets`)
    .then(res => console.log(res))
}

const updateTransmissionDataset = () => {
  return sendRequest(`${baseUrl}update-transmission-datasets`)
    .then(res => console.log(res))
}

const updateUTLACumulativeDeathsDataset = () => {
  return sendRequest(`${baseUrl}update-utla-datasets`)
    .then(res => console.log(res))
}

export default {
  getTransmissionTimeSeries: getTransmissionTimeSeries,
  getTransmissionWriteUp: getTransmissionWriteUp,
  getVaccinationTimeSeries: getVaccinationTimeSeries,
  getVaccinationWriteUp: getVaccinationWriteUp,
  getUTLACumulativeDeathData: getUTLACumulativeDeathData,
  getUTLAWriteUp: getUTLAWriteUp,
  updateVaccinationDataset: updateVaccinationDataset,
  updateTransmissionDataset: updateTransmissionDataset,
  updateUTLACumulativeDeathsDataset: updateUTLACumulativeDeathsDataset
}