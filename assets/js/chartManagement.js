var chart;
let darkMode = false;

const defaultModeConfig = {
    maintainAspectRatio: false,
    responsive: true,
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
    let config = defaultModeConfig;
    config["plugins"]["title"]["text"] = title
    if (darkMode) {
        config = darkModeConfig;
    }
    

    let ctx = document.getElementById("wifi_data_chart").getContext("2d");
    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [initialValue["time"]],
            datasets: [
                {
                    borderColor: ["#A3BAFF"],
                    data: [initialValue["down"]],
                    label: "Download Speed"
                },
                {
                    borderColor: ["#a300cc"],
                    data: [initialValue["up"]],
                    label: "Upload Speed"
                },
                {
                    borderColor: ["#e69e88"],
                    data: [initialValue["ping"]],
                    label: "Ping"
                },
                {
                    borderColor: ["#fc2605"],
                    data: [initialValue["latency"]],
                    label: "Latency"
                },
                
            ]
        },
        options: config
    });
}

const limit = 30;
function add_data (newData) {
    console.log(chart);
    const data = chart.data;
    console.log(data);
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

function format_date(date) {
    console.log(date);
    date = date.split(" ")[1];
    date = date.split(".")[0];
    console.log(date);
    return date;
}

function update_chart_theme() {
    if (chart.datasets.length > 1) {
        let config = defaultModeConfig;
        if (darkMode) {
            config = darkModeConfig;
        }
        chart.data.options = config;
        chart.update();
    }
}