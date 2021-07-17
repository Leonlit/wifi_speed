var chart;
let darkMode = false;

const defaultModeConfig = {
    maintainAspectRatio: false,
    responsive: true,
    scales: {
        y: {
            title: {
                display: true,
                text: 'Value'
            }
        },
        x: {
            ticks: {
                autoSkip: true,
                maxTicksLimit: 10
            },
            title: {    
                display: true,
                text: 'Time'
            }
        }
    },
    plugins: {
        title: {
            display: true,
            color: "black"
        },
    }
}

const darkModeConfig = {
    maintainAspectRatio: false,
    responsive: true,
    scales: {
        y: {
            grid: {
                color: 'grey',
                borderColor: 'grey',
                tickColor: 'white'
            },
            ticks: {
                color: 'white',
            },
            title: {
                color: 'white',
                display: true,
                text: 'Value'
            }
        },
        x: {
            grid: {
                color: 'white',
                borderColor: 'grey',
                tickColor: 'white'
            },
            ticks: {
                color: 'white',
                autoSkip: true,
                maxTicksLimit: 10
            },
            title: {
                color: 'white',
                display: true,
                text: 'Time'
            }
        }
    },
    plugins: {
        legend: {
            display:true,
            labels: {
                color: 'white'
            }
        },
        title: {
            display: true,
            color: "white"
        },
    },
}


function draw_chart(initialValue, title) {
    if (chart) {
        chart.destroy();
    }
    let config = defaultModeConfig;
    config["plugins"]["title"]["text"] = title
    if (darkMode) {
        config = darkModeConfig;
    }
    let ctx = document.getElementById("wifi_data_chart").getContext("2d");
    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: isArray(initialValue["time"])? initialValue["time"]: [initialValue["time"]],
            datasets: [
                {
                    borderColor: ["#A3BAFF"],
                    data: isArray(initialValue["down"]) ? initialValue["down"]: [initialValue["down"]],
                    label: "Download Speed"
                },
                {
                    borderColor: ["#a300cc"],
                    data: isArray(initialValue["up"]) ? initialValue["up"]: [initialValue["up"]],
                    label: "Upload Speed"
                },
                {
                    borderColor: ["#e69e88"],
                    data: isArray(initialValue["ping"]) ? initialValue["ping"]: [initialValue["ping"]],
                    label: "Ping"
                },
                {
                    borderColor: ["#fc2605"],
                    data: isArray(initialValue["latency"]) ? initialValue["latency"]: [initialValue["latency"]],
                    label: "Latency"
                },
                
            ]
        },
        options: config
    });
}

const limit = 30;
function add_data (newData) {
    const data = chart.data;
    //remove first data in array if limit reached
    if (data.labels.length >= limit) {
        data.labels.shift()
        data.datasets[0].data.shift()
        data.datasets[1].data.shift()
        data.datasets[2].data.shift()
        data.datasets[3].data.shift()
    }
    //add new data into chart datasets
    if (data.datasets.length > 1) {
        data.labels.push(newData["time"]);
        data.datasets[0].data.push(newData["down"]);
        data.datasets[1].data.push(newData["up"]);
        data.datasets[2].data.push(newData["ping"]);
        data.datasets[3].data.push(newData["latency"]);
        chart.update();
    }
}

function update_chart_theme() {
    if (chart.data.datasets.length > 1) {
        let tempTitle = chart.options.plugins.title.text;
        let config = defaultModeConfig;
        if (darkMode) {
            config = darkModeConfig;
        }
        config.plugins.title.text = tempTitle;
        console.log(config);
        chart.options = config;
        chart.update();
    }
}

function isArray (data) {
    return Array.isArray(data);
}