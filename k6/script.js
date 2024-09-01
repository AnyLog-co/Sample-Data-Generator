import http from 'k6/http';
import { check } from 'k6';
import { Trend } from 'k6/metrics';
import { randomSeed } from 'k6';

let myTrend = new Trend('response_time');
randomSeed(12345);  // Ensure consistency in randomness

export let options = {
    url: __ENV.URL || '127.0.0.1:32149', // URL for connecting to node
    vus: parseInt(__ENV.VUS) || 1, // Number of virtual users
    iterations: parseInt(__ENV.ITERATIONS) || 1, // Number of iterations
    batchSize: parseInt(__ENV.BATCH_SIZE) || 100000, // Set the batch size to 100,000
    nodeID: parseInt(__ENV.NODE_ID_LENGTH) || 10, // Max number of nodes
};

let totalRows = options.batchSize * options.iterations * options.vus; // Calculate the total number of rows to be inserted

console.log(`Expected total number of rows to be inserted: ${totalRows}`);

function generateSingleRow() {
    const data_url = 'http://localhost:5100/data';  // Adjust if needed
    const response = http.get(data_url);
    check(response, {
        'is status 200': (r) => r.status === 200,
        'response time < 200ms': (r) => r.timings.duration < 200,
    });
    return response.json();
}

export default function () {
    let data = [];
    let startTime = new Date().getTime();

    for (let i = 0; i < options.batchSize; i++) {
        data.push(generateSingleRow());

        // Optional: Log time taken for every 100 iterations
        if ((i + 1) % 100 === 0) {
            let elapsedTime = new Date().getTime() - startTime;
            console.log(`Time taken for iterations ${i - 99} to ${i + 1}: ${elapsedTime}ms`);
        }
    }

    let payload = JSON.stringify(data);
    let params = {
        headers: {
            'type': 'json',
            'dbms': 'new_company',
            'table': 'k6_monitor3',
            'mode': 'streaming',  // Adjust if needed
            'User-Agent': 'AnyLog/1.23',
            'Content-Type': 'application/json'  // Adjust if needed
        },
    };
    let url = `http://${__ENV.URL || '127.0.0.1:32149'}`;
    let res = http.put(url, payload, params);

    check(res, {
        'is status 200': (r) => r.status === 200,
    });

    myTrend.add(res.timings.duration);
}
