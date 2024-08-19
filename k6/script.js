// k6 run -e VUS=1 -e ITERATIONS=1000 -e BATCH_SIZE=1000 /home/moshe/script.js
//
import http from 'k6/http';
import { check } from 'k6';
import { Trend } from 'k6/metrics';
import { randomSeed } from 'k6';

let myTrend = new Trend('response_time');
randomSeed(12345);  // Ensure consistency in randomness

export let options = {
    vus: parseInt(__ENV.VUS) || 1, // Number of virtual users
    iterations: parseInt(__ENV.ITERATIONS) || 10, // Number of iterations
    batchSize: parseInt(__ENV.BATCH_SIZE) || 10, // Set the desired batch size
    nodeID: parseInt(__ENV.NODE_ID_LENGTH) || 10, // max number of nodes
};

let totalRows = options.batchSize * options.iterations; // Calculate the total number of rows to be inserted

console.log(`Expected total number of rows to be inserted: ${totalRows}`);

function generateSingleRow() {
    // Simulate uptime and system metrics
    const uptime = Math.floor(Math.random() * 86400); // Random uptime in seconds for simulation
    
    // Convert uptime to days, hours, minutes, and seconds
    const days = Math.floor(uptime / (24 * 3600));
    const hours = Math.floor((uptime % (24 * 3600)) / 3600);
    const minutes = Math.floor((uptime % 3600) / 60);
    const seconds = uptime % 60;

    return {
        'timestamp': new Date().toISOString(),
        'uptime': `${days}:${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toFixed(0).toString().padStart(2, '0')}`,
	'node_id': Math.floor(Math.random() * options.nodeID) + 1,
        'load_avg_5min': Math.random() * 2, // Simulated load average
        'disk_space': Math.random() * 100, // Simulated disk space percentage
        'cpu_percent': Math.random() * 100, // Simulated CPU usage percentage
        'virtal_memory': Math.random() * 100, // Simulated virtual memory usage percentage
        'swap_memory': Math.random() * 100, // Simulated swap memory usage percentage
        'disk_write': Math.floor(Math.random() * 1000), // Simulated disk write count
        'disk_read': Math.floor(Math.random() * 1000), // Simulated disk read count
        'packets_recv': Math.floor(Math.random() * 1000), // Simulated packets received count
        'packets_sent': Math.floor(Math.random() * 1000), // Simulated packets sent count
        'load_avg_15min': Math.random() * 2 // Simulated load average
    };
}

function generateData(batchSize) {
    let data = [];
    for (let i = 0; i < batchSize; i++) {
        data.push(generateSingleRow());
    }
    return data;
}

export default function () {
    // Generate data directly in JavaScript
    let data = generateData(options.batchSize);

    // Use the generated batch of data as the payload for the target API
    let url = 'http://127.0.0.1:32149'; // Replace with your actual REST API endpoint
    let payload = JSON.stringify(data);

    let params = {
        headers: {
            'type': 'json',
            'dbms': 'new_company',
            'table': 'k6_monitor3',
            'mode': 'streaming',
            'User-Agent': 'AnyLog/1.23',
            'Content-Type': 'application/json'
        },
    };

    let res = http.put(url, payload, params);

    check(res, {
        'is status 200': (r) => r.status === 200,
    });

    myTrend.add(res.timings.duration);
}

