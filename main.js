
document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector(".sidebar");
    const sidebarOff = document.querySelector(".sidebar-off");
    const personalizarSection = document.getElementById("personalizar-section");
    const closeSidebarButton = document.getElementById("close-sidebar");
    const closePersonalizarButton = document.getElementById("close-personalizar");
    const personalizarButton = document.getElementById("personalizar");
    const colorPicker = document.getElementById("colorPicker");
    const colorDisplay = document.getElementById("colorDisplay");
    const chartsContainer = document.getElementById("charts");
    const searchColumn = document.getElementById("searchColumn");
    const columnSelect = document.getElementById("columnSelect");
    const chartTypeSelect = document.getElementById("chartTypeSelect");
    const addChartButton = document.getElementById("addChartButton");

    let allColumns = [];

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
    closeSidebarButton.addEventListener("click", hideSidebar);
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

    async function fetchMapData(column) {
        try {
            const response = await fetch(`http://localhost:8000/map_data/${column}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data.data;
        } catch (error) {
            console.error("Erro ao buscar dados do mapa:", error);
            return [];
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
        let options = {
            chart: {
                type: type,
                height: 350
            },
            series: [],
            colors: [color]
        };

        if (type === "pie") {
            options.series = data;
            options.labels = categories;
            options.colors = generateColors(data.length);
        } else if (type === "scatter" || type === "radar") {
            options.series = [
                {
                    name: "Quantidade",
                    data: categories.map((category, index) => ({ x: category, y: data[index] }))
                }
            ];
        } else if (type === "heatmap") {
            options.series = [
                {
                    name: "Quantidade",
                    data: categories.map((category, index) => ({ x: category, y: "Valor", value: data[index] }))
                }
            ];
        } else if (type === "candlestick") {
            options.series = [
                {
                    name: "Candlestick",
                    data: categories.map((category, index) => ({ x: category, y: [data[index], data[index] * 1.2, data[index] * 0.8, data[index] * 1.1] }))
                }
            ];
        } else if (type === "boxPlot") {
            options.series = [
                {
                    type: "boxPlot",
                    data: categories.map((category, index) => ({
                        x: category,
                        y: [data[index] * 0.9, data[index] * 0.95, data[index], data[index] * 1.05, data[index] * 1.1]
                    }))
                }
            ];
        } else {
            options.series = [
                {
                    name: "Quantidade",
                    data: data
                }
            ];
            options.xaxis = { categories: categories };
        }

        const chart = new ApexCharts(container, options);
        chart.render();
        return chart;
    }

    function createMap(container, data) {
        const map = L.map(container).setView([-15.793889, -47.882778], 4);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: '© OpenStreetMap'
        }).addTo(map);

        data.forEach(({ state, value }) => {
            const marker = L.marker([state.lat, state.lng]).addTo(map);
            marker.bindPopup(`<b>${state}</b><br>Value: ${value}`);
        });
    }

    function addChart() {
        const selectedColumn = columnSelect.value;
        const selectedChartType = chartTypeSelect.value;
        const selectedColor = colorPicker.value;

        if (!selectedColumn) {
            alert("Por favor, selecione uma coluna.");
            return;
        }

        const chartContainer = document.createElement("div");
        chartContainer.className = "chart-container";

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
        moveButton.onclick = () => {
            chartContainer.classList.toggle("movable");
        };

        const resizeButton = document.createElement("button");
        resizeButton.innerHTML = '<i class="fas fa-expand"></i>';

        const removeButton = document.createElement("button");
        removeButton.innerHTML = '<i class="fas fa-trash-alt"></i>';
        removeButton.onclick = () => {
            chartsContainer.removeChild(chartContainer);
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

        if (selectedChartType === "map") {
            fetchMapData(selectedColumn).then(mapData => {
                createMap(chartElement, mapData);
            });
        } else {
            fetchUniqueCounts(selectedColumn).then(uniqueCounts => {
                const categories = Object.keys(uniqueCounts);
                const data = Object.values(uniqueCounts);
                const chart = createChart(chartElement, selectedChartType, categories, data, selectedColor);

                interact(chartContainer)
                    .draggable({
                        listeners: {
                            move(event) {
                                if (!event.target.classList.contains("movable")) return;

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
                            }
                        }
                    });
            });
        }
    }

    addChartButton.addEventListener("click", addChart);

    fetchColumns().then(columns => {
        allColumns = columns;
        columns.forEach(column => {
            let option = document.createElement("option");
            option.value = column;
            option.text = column;
            columnSelect.appendChild(option);
        });
    });

    searchColumn.addEventListener("input", () => {
        const searchValue = searchColumn.value.toLowerCase();
        const options = columnSelect.querySelectorAll("option");

        options.forEach(option => {
            const text = option.textContent.toLowerCase();
            option.style.display = text.includes(searchValue) ? "block" : "none";
        });
    });
});
