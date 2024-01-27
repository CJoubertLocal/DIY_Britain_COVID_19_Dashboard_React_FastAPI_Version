import { useState, useEffect, useRef } from 'react'
import services from '../services/services'
import EchartCreator from './lineEchartHelper'
import UpdateDatasetsButton from './UpdateDatasetsButton'
import updateData from '../services/updateDatasets'

const VaccinationTimeSeriesChartReportBlock = () => {
  const [vaccinationData, setVaccinationData] = useState({
    column_names: [],
    date_values: [],
    data: []
  });
  
  const [htmlWriteUp, setHtmlWriteUp] = useState("")
  useEffect(() => {
    services.getVaccinationWriteUp().then(res => setHtmlWriteUp(res))
  })

  const s = useRef(0);

  return (
  <>
  <div class="container text-start">
        <div class="row">

          <div class="col">
            {EchartCreator(
              s,
              vaccinationData,
              setVaccinationData,
              services.getVaccinationTimeSeries,
              'Percentage of Population Vaccinationed',
              'Date',
              'Percentage of Population (%)',
              3,
              true
            )}

            {UpdateDatasetsButton(
              "", 
              updateData.UpdateVaccinationDatasets, 
              setVaccinationData, 
              "Update Vaccination Data", 
              "btn btn-outline-info"
            )}
          </div>

          <div class="col">
            {/* WARNING! dangerouslySetInnerHTML in use. */}
            <div dangerouslySetInnerHTML={{__html: htmlWriteUp}} />
          </div>

        </div>
      </div>
    </>
  )
}

export default VaccinationTimeSeriesChartReportBlock
