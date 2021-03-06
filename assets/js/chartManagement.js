var chart;
let darkMode = false;

// default style for chart
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

//dark theme for the chart
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
                display: true,
                text: 'Time'
            }
        }
    },
    plugins: {
        legend: {
            display:true,

        },
        title: {
            display: true,
        },
    },
}

//drawing initial chart to the page
function draw_chart(initialValue, title) {
    document.getElementById("loader").style.display = "none"
    if (chart) {
        chart.destroy();
    }
    let config = defaultModeConfig;
    Chart.defaults.color = "black";
    config["plugins"]["title"]["text"] = title
    if (darkMode) {
        config = darkModeConfig;
        Chart.defaults.color = "white";
    }
    let dataset = [];
    if (initialValue.hasOwnProperty("up") && initialValue.up.length != 0) {
        dataset = [
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
    }
    
    let ctx = document.getElementById("wifi_data_chart").getContext("2d");
    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: isArray(initialValue["time"])? initialValue["time"]: [initialValue["time"]],
            datasets: dataset
        },
        options: config
    });
    if_no_data();
}

function if_no_data() {
    if (chart.data.datasets.length === 0) {
        let ctx = document.getElementById("wifi_data_chart").getContext("2d");
        // No data is present
        var width = chart.width;
        var height = chart.height
        chart.clear();

        ctx.save();
        ctx.textAlign = 'center';
        ctx.fillStyle = darkMode ? "white" : "black"
        ctx.textBaseline = 'middle';
        ctx.font = "16px normal 'Helvetica Nueue'";
        ctx.fillText('No data to display', width / 2, height / 2);
        ctx.restore();
    }
}

//this function is used when new data is to be updated onto the chart (used in real time monitor)
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

// When the theme is changed, we need to update the configuration of the chart also
function update_chart_theme() {
    try {
        if_no_data();
        if (chart && chart.data.datasets.length > 1) {
            let tempTitle = chart.options.plugins.title.text;
            let config = defaultModeConfig;
            if (darkMode) {
                config = darkModeConfig;
            }
            config.plugins.title.text = tempTitle;
            chart.options = config;
            chart.update();
        }
    }catch (ex) {
        console.log(ex);
    }
}

// just a simple function to check if things is an array or not
function isArray (data) {
    return Array.isArray(data);
}