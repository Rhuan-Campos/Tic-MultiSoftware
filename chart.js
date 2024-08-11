const chartCache = {}; // Armazena os gráficos

function generateColors(numColors) {
    const colors = [];
    for (let i = 0; i < numColors; i++) {
        colors.push(`hsl(${i * 360 / numColors}, 70%, 50%)`);
    }
    return colors;
}

function createChart(container, type, categories = [], data = [], color = "#00E396") {

    function aggregateData(categories, data) {
        let aggregated = {};
        categories.forEach((category, index) => {
            if (!aggregated[category]) {
                aggregated[category] = 0;
            }
            aggregated[category] += data[index];
        });
        return aggregated;
    }

    let options = {
        chart: {
            type: type,
            height: 350
        },
        series: [],
        colors: [color]
    };

    if (type === "customAngleCircle") {
        options.chart.type = 'radialBar';
        const total = data.reduce((acc, val) => acc + val, 0);
        const percentages = data.map(val => (val / total) * 100);

        options.series = percentages;
        options.labels = categories;
        options.colors = generateColors(data.length); 
        options.plotOptions = {
            radialBar: {
                startAngle: -135,
                endAngle: 225,
                hollow: {
                    margin: 5,
                    size: '30%',
                    background: 'transparent',
                    image: undefined
                },
                dataLabels: {
                    name: {
                        show: true,
                        fontSize: '16px',
                    },
                    value: {
                        show: true,
                        fontSize: '30px',
                        formatter: function (val, opts) {
                            if (opts.w.globals.hoveredSeriesIndex !== undefined) {
                                const hoveredIndex = opts.w.globals.hoveredSeriesIndex;
                                return `${categories[hoveredIndex]}: ${data[hoveredIndex]}`;
                            }
                            return opts.w.config.series[opts.seriesIndex];
                        }
                    },
                    total: {
                        show: true,
                        label: 'Total',
                        formatter: function (w) {
                            return data.reduce((a, b) => a + b, 0);
                        }
                    }
                }
            }
        };

        options.tooltip = {
            enabled: true,
            custom: function({ series, seriesIndex, dataPointIndex, w }) {
                return `
                    <div style="padding: 5px;">
                        <strong>${categories[seriesIndex]}</strong><br>
                        ${series[seriesIndex]}
                    </div>
                `;
            }
        };
    } else {
        
        if (type === "line") {
            options.series = [{ name: "Quantidade", data: data }];
            options.xaxis = { categories: categories };
        } else if (type === "area") {
            options.series = [{ name: "Quantidade", data: data }];
            options.xaxis = { categories: categories };
            options.stroke = { curve: 'smooth' };
        } else if (type === "bar") {
            options.series = [{ name: "Quantidade", data: data }];
            options.xaxis = { categories: categories };
            options.plotOptions = { bar: { horizontal: false } };
        } else if (type === "pie") {
            options.series = data;
            options.labels = categories;
            options.colors = generateColors(data.length);
        } else if (type === "donut") {
            options.series = data;
            options.labels = categories;
            options.colors = generateColors(data.length);
        } else if (type === "radialBar") {
            options.series = data;
            options.labels = categories;
            options.plotOptions = {
                radialBar: {
                    dataLabels: {
                        total: {
                            show: true,
                            label: 'Total'
                        }
                    }
                }
            };
        } else if (type === "scatter") {

        
            const mean = data.reduce((acc, val) => acc + val, 0) / data.length;
            const stdDev = Math.sqrt(data.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / data.length);
            const threshold = 3; 

            const allPoints = categories.map((category, index) => {
                const y = data[index];
                const isOutlier = Math.abs(y - mean) > threshold * stdDev;
                return {
                    x: category,
                    y: parseFloat(y.toFixed(2)),
                    marker: {
                        size: 8,
                        fillColor: isOutlier ? '#FF0000' : '#008FFB'
                    }
                };
            });

            const meanLine = categories.map(category => ({ x: category, y: parseFloat(mean.toFixed(2)) }));


            options.series = [
                {
                    name: "Valores",
                    data: allPoints,
                    type: 'scatter'
                },
                {
                    name: "Média",
                    data: meanLine,
                    type: 'line',
                    color: '#FF4560',
                    marker: {
                        size: 0 
                    }
                }
            ];

         
            options.chart = {
                type: 'line',
                height: 350
            };

            options.xaxis = {
                type: 'category'
            };

        
            options.yaxis = {
                title: {
                    text: 'Quantidade'
                },
                labels: {
                    formatter: function(value) {
                        return value.toFixed(2);
                    }
                },
                min: mean - 3 * stdDev,
                max: mean + 3 * stdDev
            };

            options.tooltip = {
                enabled: true,
                shared: false,
                intersect: true,
                custom: function({ series, seriesIndex, dataPointIndex, w }) {
                    const point = w.globals.series[seriesIndex][dataPointIndex];
                    return `
                        <div style="padding: 5px;">
                            <strong>${point.x}</strong><br>
                            Quantidade: ${point.y.toFixed(2)}
                        </div>
                    `;
                }
            };
        } else if (type === "boxPlot") {
            options.series = [
                {
                    type: "boxPlot",
                    data: data
                }
            ];
        } else {
            console.error("Tipo de gráfico não suportado");
            return;
        }

        const chart = new ApexCharts(container, options);
        chart.render();
        chartCache[container.id] = chart;
    }
}

function updateChart(containerId, type, categories, data, color) {
    if (chartCache[containerId]) {
        chartCache[containerId].destroy();
    }
    const container = document.getElementById(containerId);
    createChart(container, type, categories, data, color);
}
