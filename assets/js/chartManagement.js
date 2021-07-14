var chart;

function draw_chart(initialValue) {
    let ctx = document.getElementById("wifi_data_chart").getContext("2d");
    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [initialValue["time"]],
            datasets: [
                {
                    borderColor: ["#e69e88"],
                    data: [initialValue["down"]],
                    label: "Download Speed"
                },
                {
                    borderColor: ["#a300cc"],
                    data: [initialValue["up"]],
                    label: "Upload Speed"
                },
                
        ]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
        }
        
    });
}

const limit = 30;
function add_data (newData) {
    const data = chart.data;
    console.log(data);
    //remove first data in array if limit reached
    if (data.labels.length >= limit) {
        data.labels.shift()
        data.datasets[0].data.shift()
        data.datasets[1].data.shift()
    }
    //add new data into chart datasets
    if (data.datasets.length > 1) {
        data.labels.push(newData["time"]);
        data.datasets[0].data.push(newData["down"]);
        data.datasets[1].data.push(newData["up"]);
        chart.update();
    }
}