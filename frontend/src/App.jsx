import './App.css'
import VaccinationTimeSeriesChartReportBlock from './components/VaccineTimeSeriesReportBlock'
import TransmissionTimeSeriesChartReportBlock from './components/TransmissionTimeSeriesReportBlock'
import UTLACumulativeDeathsTimeSeriesChartReportBlock from './components/UTLACumulativeDeathsReportBlock'

function App() {
  return (
    <div>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossOrigin="anonymous"></link>
      
      <h1>
        DIY Covid-19 Dashboard
      </h1>

      <div className='grid gap-3'>
      
        <hr />

        <TransmissionTimeSeriesChartReportBlock />

        <hr />
        
        <VaccinationTimeSeriesChartReportBlock />

        <hr />

        <UTLACumulativeDeathsTimeSeriesChartReportBlock />
      
      </div>
      
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossOrigin="anonymous"></script>

    </div>
  )
}

export default App

// Echarts needs some sense of how large the container is.
// In prototyping, a <div style={{width: 500, height: 500}}>
// will work well-enough.
// With a CSS-framework like Bootstrap, this is unnecessary.
// See: https://github.com/apache/echarts/issues/10478
