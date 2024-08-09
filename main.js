document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector(".sidebar");
    const sidebarOff = document.querySelector(".sidebar-off");
    const darkModeButton = document.getElementById("dark-mode");
    const lightModeButton = document.getElementById("light-mode");
    const personalizarSection = document.getElementById("personalizar-section");
    const DcloseSidebarButton = document.getElementById("d-close-sidebar");
    const WcloseSidebarButton = document.getElementById("w-close-sidebar");
    const closePersonalizarButton = document.getElementById("close-personalizar");
    const personalizarButton = document.getElementById("personalizar");
    const colorPicker = document.getElementById("colorPicker");
    const colorDisplay = document.getElementById("colorDisplay");
    const dashboardButton = document.getElementById("dashboard");
    const chartsContainer = document.getElementById("charts");
    const searchColumn = document.getElementById("searchColumn");
    const columnSelect = document.getElementById("columnSelect");
    const chartTypeSelect = document.getElementById("chartTypeSelect");
    const addChartButton = document.getElementById("addChartButton");

    let allColumns = [];
    let chartCache = {}; 

    function showPersonalizarSection() {
        personalizarSection.classList.remove("hidden");
    }

    function hidePersonalizarSection() {
        personalizarSection.classList.add("hidden");
    }

    function hideSidebar() {
        sidebar.classList.add("hidden");
        sidebarOff.classList.remove("hidden");
    }

    function showSidebar() {
        sidebar.classList.remove("hidden");
        sidebarOff.classList.add("hidden");
    }

    personalizarButton.addEventListener("click", () => {
        if (personalizarSection.classList.contains("hidden")) {
            showPersonalizarSection();
        } else {
            hidePersonalizarSection();
        }
    });

    closePersonalizarButton.addEventListener("click", hidePersonalizarSection);
    DcloseSidebarButton.addEventListener("click", hideSidebar);
    WcloseSidebarButton.addEventListener("click", hideSidebar);
    sidebarOff.addEventListener("click", showSidebar);

    colorDisplay.addEventListener("click", () => {
        colorPicker.click(); 
    });

    colorPicker.addEventListener("input", () => {
        const selectedColor = colorPicker.value;
        colorDisplay.style.backgroundColor = selectedColor;
    });

    document.addEventListener("click", (event) => {
        if (!personalizarSection.contains(event.target) && !personalizarButton.contains(event.target)) {
            hidePersonalizarSection();
        }
    });

    async function fetchColumns() {
        try {
            const response = await fetch("http://localhost:8000/columns");
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data.columns;
        } catch (error) {
            console.error("Erro ao buscar colunas:", error);
            return [];
        }
    }

    async function fetchUniqueCounts(column) {
        try {
            const response = await fetch(`http://localhost:8000/unique_counts/${column}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data.unique_counts;
        } catch (error) {
            console.error("Erro ao buscar dados:", error);
            return {};
        }
    }

    function generateColors(numColors) {
        const colors = [];
        for (let i = 0; i < numColors; i++) {
            colors.push(`hsl(${i * 360 / numColors}, 70%, 50%)`);
        }
        return colors;
    }

    function createChart(container, type, categories = [], data = [], color = "#00E396") {
        // Função para agrupar dados por categoria e somar os valores
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
            options.colors = generateColors(data.length); // Generate different colors for each segment
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
                                    // Se o mouse está sobre algum segmento, exibe o valor e o nome
                                    const hoveredIndex = opts.w.globals.hoveredSeriesIndex;
                                    return `${categories[hoveredIndex]}: ${data[hoveredIndex]}`;
                                }
                                // Caso contrário, exibe o valor da série
                                return opts.w.config.series[opts.seriesIndex];
                            }
                        },
                        total: {
                            show: true,
                            label: 'Total',
                            formatter: function (w) {
                                // Calcula o total de todas as séries
                                return data.reduce((a, b) => a + b, 0);
                            }
                        }
                    }
                }
            };
        
            options.tooltip = {
                enabled: true,
                custom: function({ series, seriesIndex, dataPointIndex, w }) {
                    // Customiza o tooltip para exibir informações detalhadas
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
            } 
            else if (type === "scatter") {
                // Calcular a média e o desvio padrão dos dados
                const mean = data.reduce((acc, val) => acc + val, 0) / data.length;
                const stdDev = Math.sqrt(data.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / data.length);
                const threshold = 3; // Número de desvios padrão para considerar como fora do desvio padrão
            
                // Pontos de dados com destaque para outliers
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
            
                // Linha representando a média
                const meanLine = categories.map(category => ({ x: category, y: parseFloat(mean.toFixed(2)) }));
            
                // Configuração das séries para o gráfico
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
                            size: 0 // Remove os marcadores da linha
                        }
                    }
                ];
            
                // Configuração do gráfico
                options.chart = {
                    type: 'line',
                    height: 350
                };
            
                // Configuração do eixo X
                options.xaxis = {
                    type: 'category'
                };
            
                // Configuração do eixo Y
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
            
                // Configuração do tooltip
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
            }
            
            
            
             else if (type === "boxPlot") {
                options.series = [
                    {
                        type: "boxPlot",
                        data: categories.map((category, index) => ({
                            x: category,
                            y: [data[index] * 0.9, data[index] * 0.95, data[index], data[index] * 1.05, data[index] * 1.1]
                        }))
                    }
                ];
            } else if (type === "radar") {
                options.series = [{ name: "Quantidade", data: data }];
                options.labels = categories;
            } else if (type === "polarArea") {
                options.series = data;
                options.labels = categories;
                options.colors = generateColors(data.length);
            } else if (type === "rangeBar") {
                options.series = [
                    {
                        name: "Range",
                        data: categories.map((category, index) => ({
                            x: category,
                            y: [data[index] - 10, data[index] + 10]
                        }))
                    }
                ];
            } else if (type === "semiCircleGauge") {
                // Semi Circle Gauge
                options.series = data;
                options.plotOptions = {
                    radialBar: {
                        startAngle: -90,
                        endAngle: 90,
                        hollow: { margin: 15, size: '70%' },
                        dataLabels: { showOn: "always" }
                    }
                };
                options.labels = categories;
            } else if (type === "columnWithNegativeValues") {
                // Column with Negative Values
                if (data.length <= 1) {
                    alert("Por favor, selecione mais de uma coluna para este gráfico.");
                    return;
                }
                options.series = [{ name: "Quantidade", data: data }];
                options.plotOptions = { bar: { horizontal: false } };
                options.xaxis = { categories: categories };
                options.yaxis = { labels: { formatter: val => val.toFixed(0) } };
            } else if (type === "lineColumn") {
                // Line Column
                if (data.length <= 1) {
                    alert("Por favor, selecione mais de uma coluna para este gráfico.");
                    return;
                }
                options.series = [
                    { name: "Linha", type: "line", data: data.map(d => d * 1.2) },
                    { name: "Coluna", type: "column", data: data }
                ];
                options.xaxis = { categories: categories };
            } 
             else {
                alert("Tipo de gráfico não reconhecido.");
            }
        }
    
        console.log(`Creating chart of type: ${type} with options:`, options); // Log de depuração
    
        const chart = new ApexCharts(container, options);
        chart.render();
        return chart;
    }
    function addChart() {
        const selectedColumn = columnSelect.value;
        const selectedChartType = chartTypeSelect.value;
        const selectedColor = colorPicker.value;
    
        if (!selectedColumn) {
            alert("Por favor, selecione uma coluna.");
            return;
        }
    
        fetchUniqueCounts(selectedColumn).then(uniqueCounts => {
            const categories = Object.keys(uniqueCounts);
            const data = Object.values(uniqueCounts);
    
            const chartContainer = document.createElement("div");
            chartContainer.className = "chart-container hidden"; 
    
            const chartActions = document.createElement("div");
            chartActions.className = "chart-actions";
    
            const colorButton = document.createElement("button");
            colorButton.innerHTML = '<i class="fas fa-palette"></i>';
            colorButton.onclick = () => {
                const newColor = prompt("Digite a nova cor em formato hexadecimal:", selectedColor);
                if (newColor) {
                    chart.updateOptions({ colors: [newColor] });
                }
            };
    
            const columnButton = document.createElement("button");
            columnButton.innerHTML = '<i class="fas fa-columns"></i>';
            columnButton.onclick = async () => {
                const newColumn = prompt("Digite o nome da nova coluna:", selectedColumn);
                if (newColumn) {
                    const uniqueCounts = await fetchUniqueCounts(newColumn);
                    const categories = Object.keys(uniqueCounts);
                    const data = Object.values(uniqueCounts);
                    chart.updateOptions({ 
                        chart: { height: 350, type: selectedChartType },
                        series: [{
                            name: "Quantidade",
                            data: data
                        }],
                        xaxis: { categories: categories }
                    });
                }
            };
    
            const moveButton = document.createElement("button");
            moveButton.innerHTML = '<i class="fas fa-arrows-alt"></i>';
    
            const resizeButton = document.createElement("button");
            resizeButton.innerHTML = '<i class="fas fa-expand"></i>';
    
            const removeButton = document.createElement("button");
            removeButton.innerHTML = '<i class="fas fa-trash-alt"></i>';
            removeButton.onclick = () => {
                chartsContainer.removeChild(chartContainer);
                delete chartCache[selectedColumn]; 
            };
    
            chartActions.appendChild(colorButton);
            chartActions.appendChild(columnButton);
            chartActions.appendChild(moveButton);
            chartActions.appendChild(resizeButton);
            chartActions.appendChild(removeButton);
            chartContainer.appendChild(chartActions);
    
            const chartElement = document.createElement("div");
            chartContainer.appendChild(chartElement);
            chartsContainer.appendChild(chartContainer);
    
            const chart = createChart(chartElement, selectedChartType, categories, data, selectedColor);
            chartCache[selectedColumn] = chart; 
    
            interact(chartContainer)
                .draggable({
                    listeners: {
                        move(event) {
                            const target = event.target;
                            const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
                            const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;
    
                            target.style.transform = `translate(${x}px, ${y}px)`;
    
                            target.setAttribute('data-x', x);
                            target.setAttribute('data-y', y);
                        }
                    }
                })
                .resizable({
                    edges: { left: true, right: true, bottom: true, top: true },
                    listeners: {
                        move(event) {
                            let { x, y } = event.target.dataset;
    
                            x = (parseFloat(x) || 0) + event.dx;
                            y = (parseFloat(y) || 0) + event.dy;
    
                            Object.assign(event.target.style, {
                                width: `${event.rect.width}px`,
                                height: `${event.rect.height}px`,
                                transform: `translate(${x}px, ${y}px)`
                            });
    
                            event.target.dataset.x = x;
                            event.target.dataset.y = y;
    
                            chart.updateOptions({
                                chart: {
                                    height: event.rect.height,
                                    width: event.rect.width
                                }
                            }, false, false);
                        }
                    }
                });
    
            alert("Gráfico adicionado com sucesso!"); 
        });
    }
    
    fetchColumns().then(columns => {
        allColumns = columns;
        columns.forEach(column => {
            const option = document.createElement("option");
            option.value = column;
            option.text = column;
            columnSelect.appendChild(option);
        });
    });
    
    searchColumn.addEventListener("input", () => {
        const searchTerm = searchColumn.value.toLowerCase();
        columnSelect.innerHTML = "";
        const filteredColumns = allColumns.filter(column => column.toLowerCase().includes(searchTerm));
        filteredColumns.forEach(column => {
            const option = document.createElement("option");
            option.value = column;
            option.text = column;
            columnSelect.appendChild(option);
        });
    });
    
    addChartButton.addEventListener("click", () => {
        addChart(); 
    });
    
    dashboardButton.addEventListener("click", () => {
        if (chartsContainer.children.length === 0) {
            alert("Não há gráficos adicionados.");
        } else {
            hideSidebar();
            Array.from(chartsContainer.children).forEach(child => {
                child.classList.remove("hidden"); 
            });
            chartsContainer.classList.remove("hidden"); 
        }
    });
    
    darkModeButton.addEventListener("click", () => {
        sidebar.classList.remove("light-mode");
        sidebar.classList.add("dark-mode");
    });

    lightModeButton.addEventListener("click", () => {
        sidebar.classList.remove("dark-mode");
        sidebar.classList.add("light-mode");
    });

    document.getElementById('d-expandir').addEventListener('click', toggleFullScreen);
    document.getElementById('w-expandir').addEventListener('click', toggleFullScreen);

    function toggleFullScreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    }

    chartsContainer.classList.add("hidden"); 
});
