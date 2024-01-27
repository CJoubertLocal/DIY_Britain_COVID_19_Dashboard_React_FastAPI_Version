import { useState, useEffect, useRef } from 'react'
import EchartCreator from './lineEchartHelper'
import services from '../services/services'
import UpdateDatasetsButton from './UpdateDatasetsButton'
import UpdateDatasets from '../services/updateDatasets'

const UTLACumulativeDeathsTimeSeriesChartReportBlock = () => {
  const [utlaDeathData, setUtlaDeathData] = useState({
    column_names: [],
    data: []
  });

  const [htmlWriteUp, setHtmlWriteUp] = useState("")
  useEffect(() => {
    services.getUTLAWriteUp().then(res => setHtmlWriteUp(res))
  })

  const s = useRef(0);

  return (
  <>
    <div class="container text-start">
        <div class="row">

          <div class="col">
            {/* WARNING! dangerouslySetInnerHTML in use. */}
            <div dangerouslySetInnerHTML={{__html: htmlWriteUp}} />
          </div>

          <div class="col">
            {EchartCreator(
              s,
              utlaDeathData,
              setUtlaDeathData,
              services.getUTLACumulativeDeathData,
              'Cumulative Death by UTLA Region',
              'Date',
              'Total Number of Deaths',
              1,
              false
            )}

            {UpdateDatasetsButton(
              "WARNING: The button to update the UTLA datasets takes a significant amount of time to run. Please only use this if needed.", 
              UpdateDatasets.UpdateUTLACumulativeDeathData, 
              setUtlaDeathData, 
              "Update UTLA Data", 
              "btn btn-outline-danger"
            )}
          </div>
        
        </div>
      </div>
    </>
  )
}

export default UTLACumulativeDeathsTimeSeriesChartReportBlock
