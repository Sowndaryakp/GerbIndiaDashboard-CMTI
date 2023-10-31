<template>
  <CanvasJSChart :options="options" :style="styleOptions" @chart-ref="chartInstance" />
</template>

<script>
export default {
  data() {
    let updateInterval = 1000; // Update interval in milliseconds (1 second)
    let initialNumberOfDataPoints = 50;
    let dataPoints1 = [];
    let dataPoints2 = [];
    let yValue1 = 320;
    let yValue2 = 32;
    let xValue = new Date().getTime() - updateInterval * initialNumberOfDataPoints;

    for (let i = 0; i < initialNumberOfDataPoints; i++) {
      yValue1 += Math.round(2 + Math.random() * (-2 - 2));
      yValue2 += Math.round(2 + Math.random() * (-2 - 2));

      // pushing the new values
      dataPoints1.push({
        x: xValue,
        y: yValue1,
      });
      dataPoints2.push({
        x: xValue,
        y: yValue2,
      });
      xValue += updateInterval;
    }

    return {
      chart: null,
      timeout: null,
      dataPoints1: dataPoints1,
      dataPoints2: dataPoints2,
      yValue1: yValue1,
      yValue2: yValue2,
      xValue: xValue,
      updateInterval: updateInterval,
      options: {
        zoomEnabled: true,
        exportEnabled: true,
        theme: "light2",
        title: {
          text: "Live Chart Consumption of Current vs Voltage",
        },
        subtitles: [
          {
            text: "Chart updates every 1 second",
          },
        ],
        axisX: {
          valueFormatString: "H:mm:ss TT",
        },
        axisY: {
          valueFormatString: "##A/V", // Default value format for the axisY (Current in Amps)
        },
        toolTip: {
          shared: true,
        },
        legend: {
          cursor: "pointer",
          fontColor: "dimGrey",
          itemclick: this.toggleDataSeries,
        },
        data: [
          {
            type: "spline",
            name: "Current in Amps",
            color: "#00796B",
            xValueType: "dateTime",
            yValueFormatString: "#,### amps",
            xValueFormatString: "hh:mm:ss TT",
            showInLegend: true,
            legendText: "{name} " + yValue1 + " Amps",
            dataPoints: dataPoints1,
          },
          {
            type: "spline",
            name: "Voltage in Volts",
            color: "#FBC02D",
            xValueType: "dateTime",
            yValueFormatString: "#,### volts",
            showInLegend: true,
            legendText: "{name} " + yValue2 + " Volts",
            dataPoints: dataPoints2,
          },
        ],
      },
      styleOptions: {
        width: "100%",
        height: "360px",
      },
    };
  },
  methods: {
    toggleDataSeries(e) {
      if (typeof e.dataSeries.visible === "undefined" || e.dataSeries.visible) {
        e.dataSeries.visible = false;
      } else {
        e.dataSeries.visible = true;
      }

      // Update axisY value format based on selected data series
      if (e.dataSeriesIndex === 0) {
        this.chart.options.axisY.valueFormatString = "##V"; // Set value format to "##A" for Current in Amps
      } else if (e.dataSeriesIndex === 1) {
        this.chart.options.axisY.valueFormatString = "##A"; // Set value format to "##V" for Voltage in Volts
      }

      e.chart.render();
    },
    updateChart() {
      this.xValue += this.updateInterval;
      // adding random value
      this.yValue1 += Math.round(2 + Math.random() * (-2 - 2));
      this.yValue2 += Math.round(2 + Math.random() * (-2 - 2));

      // pushing the new values
      this.dataPoints1.push({
        x: this.xValue,
        y: this.yValue1,
      });
      this.dataPoints2.push({
        x: this.xValue,
        y: this.yValue2,
      });

      // updating legend text with updated with y Value
      this.chart.options.data[0].legendText = "Current in Amps - " + this.yValue1 + " amps";
      this.chart.options.data[1].legendText = "Voltage in Volts - " + this.yValue2 + " volts";

      this.chart.render();
      this.timeout = setTimeout(this.updateChart, this.updateInterval);
    },
    chartInstance(chart) {
      this.chart = chart;
      this.timeout = setTimeout(this.updateChart, this.updateInterval);
    },
  },
  unmounted() {
    clearTimeout(this.timeout);
  },
};
</script>
