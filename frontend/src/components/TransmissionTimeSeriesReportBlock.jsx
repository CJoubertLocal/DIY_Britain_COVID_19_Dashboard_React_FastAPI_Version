import { useState, useEffect, useRef } from 'react'
import EchartCreator from './lineEchartHelper'
import services from '../services/services'
import UpdateDatasetsButton from './UpdateDatasetsButton'
import UpdateDatasets from '../services/updateDatasets'

const TransmissionTimeSeriesChartReportBlock = () => {
  // Upon setting these variables to contain new data, the echarts reliant on them will
  // be rerendered by react.
  const [transmissionData, setTransmissionData] = useState({
    dateValues: [],
    data: []
  });

  const [htmlWriteUp, setHtmlWriteUp] = useState("")
  useEffect(() => {
    services.getTransmissionWriteUp().then(res => setHtmlWriteUp(res))
  })

  const s = useRef(0);
  
  return (
  <>
    <div class="container text-start">
        <div class="row">

          <div class="col">
            {/* 
              dangerouslySetInnerHTML is only used as I know what the source file is.
              In all other cases, if this is used, sanitise the HTML before rendering.              
            */}

            <div dangerouslySetInnerHTML={{__html: htmlWriteUp}} />
          </div>

          <div class="col">
            {EchartCreator(
              s,
              transmissionData,
              setTransmissionData,
              services.getTransmissionTimeSeries,
              'COVID-19 Transmission Rates',
              'Date',
              'Change in Transmission Rate (% change in number of cases)',
              1,
              false
            )}

            {UpdateDatasetsButton(
              "", 
              UpdateDatasets.UpdateTransmissionDatasets, 
              setTransmissionData, 
              "Update Transmission Data", 
              "btn btn-outline-info"
            )}
          </div>

        </div>
      </div>
    </>
  )
}

export default TransmissionTimeSeriesChartReportBlock