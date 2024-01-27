import { useEffect } from "react";
import updateData from "../services/updateDatasets"
import ReactEChart from 'echarts-for-react'
// https://github.com/hustcc/echarts-for-react

const EchartCreator = (useRefVariable, data, setData, getDataFunc, title, xAxisTitle, yAxisTitle, numChartsToDraw, stackLines) => {

    useEffect(
        () => {
          if (useRefVariable.current === 0) {
            getDataFunc().then(
              res => updateData.ExtractAndSetData(res, setData)
            )
            useRefVariable.current = 1;
          }
        }
    )
    
    // https://react.dev/learn/conditional-rendering
    if (data === undefined) {
      return (<>Sorry I couldn&apos;t get this data. Please try reloading the page.</>)
    }

    const dataOptions = lineChartOptionsGenerator(
        title,
        xAxisTitle,
        yAxisTitle,
        data,
        numChartsToDraw,
        stackLines
      )

    return (
      <div>
        <ReactEChart option={dataOptions}
                    style={{height: '500px', width: '500px'}}/>
      </div>
    )
}
  
// https://apache.github.io/echarts-handbook/en/concepts/dataset/#how-to-reference-several-datasets <- several datasets
// https://echarts.apache.org/examples/en/editor.html?c=area-stack
const lineChartOptionsGenerator = (title, xAxisTitle, yAxisTitle, data, numCharts, stackLines) => {
  var option = {
      title: [
        {
          text: title,
        } 
      ],
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          label: {
            backgroundColor: '#6a7985'
          }
        }
      },
      legend: {
        type: 'scroll',
        top: 30
      },
      xAxis: [],
      yAxis: [],
      dataZoom: [
        {
          show: true,
          realtime: true,
          start: 0,
          end: 100,
          xAxisIndex: [0, 1]
        },
        {
          type: 'inside',
          realtime: true,
          start: 0,
          end: 100,
          xAxisIndex: [0, 1]
        }
      ],
      // https://apache.github.io/echarts-handbook/en/concepts/dataset/#
      dataset: [],
      series: []
    };

    for (let i = 0; i < numCharts; i++) {
      option.xAxis.push({
        type: 'category',
        name: xAxisTitle,
        data: data.dateValues,
        gridIndex: i
      })

      option.yAxis.push({
        type: 'value',
        nameLocation: 'middle',
        // Only add the title to the middle (or near middle) y-axis.
        name: numCharts % 2 === 0 
              ? i === (numCharts / 2) 
                ? yAxisTitle
                : ''
              : i === ((numCharts-1) / 2)
                ? yAxisTitle
                : '',
        nameGap: 35,
        gridIndex: i
      })
    }

    if (numCharts > 1) {
      option['grid'] = []
      const fraction = Math.floor(90 / numCharts)
      
      for (let i = 0; i < numCharts; i++) {
        option.grid.push({})

        if (i > 0) {
          option.grid[i].top = (100 - ((numCharts - i) * fraction)).toString() + '%'
        }

        if (i < (numCharts - 1)) {
          option.grid[i].bottom = (100 - ((i+1) * fraction)).toString() + '%'
        }
      }
    }
  
    for (const property in data.series) {
      option.dataset.push({
        source: data.series[property]
      })
    }
  
    // Add a series for each column of data other than date.
    // Be careful to not add a column for each
    // row of data, as this will make the chart
    // very sluggish.
    var datasetToAddTo = -1
    for (const property in data.series) {
      datasetToAddTo++
  
      for (const colName in data.series[property][0]) {
        if (colName !== 'date') {
      
          var lineOpts = {
            name: colName,
            type: 'line',
            datasetIndex: datasetToAddTo
          }

          if (stackLines) {
            lineOpts['stack'] = property
            lineOpts['areaStyle'] = {}
            lineOpts['xAxisIndex'] = datasetToAddTo,
            lineOpts['yAxisIndex'] = datasetToAddTo
          }
          
          option.series.push(lineOpts)
        }
      }
    }
  
  return option
  }
  

  export default EchartCreator