import { check } from 'k6';
import { Trend } from 'k6/metrics';
import http from 'k6/http';

// Define custom metric for the header value
const begin_code_execution = new Trend('begin_code_execution_latency', true);
const end_code_execution = new Trend('end_code_execution_latency', true);

export const options = {
  scenarios: {
    thoughput: {
        executor: 'constant-arrival-rate',
        duration: '30s', 
        rate: 60,
        timeUnit: '1m',
        preAllocatedVUs: 50,
        maxVUs: 100
    }
  }
  /*thresholds: {
    // Define thresholds for your custom metric
    'response_header_time': ['p(95)<500'], // 95% of values should be below 500ms
  },*/
};

export default function () {
  const url = 'http://34.51.173.48:8001/execute/python';
  const params = {
    headers: {
      'Content-Type': 'application/json',
    }
  };
  const payload = JSON.stringify({
        "code": "print(2+2)",
        "time_limit": 2,
        "memory_limit": 65536
    })

  const response = http.post(url, payload, params);

  // Check for the header and record its value as a metric
  check(response, {
    'status is 200': (r) => r.status === 200
  });

  if (response.headers['X-Req-Insights']) {
    // Convert header value to number and add to metric
    const parsedDict = parseStringToDict(response.headers['X-Req-Insights']);
    begin_code_execution.add(parsedDict["run_start"]-parsedDict["received"]);
    end_code_execution.add(parsedDict["respond"]-parsedDict["run_end"]);
  }
  
}
const parseStringToDict = (str) => {
  const result = {};
  str.split(',').forEach(pair => {
    const [key, value] = pair.split('=');
    result[key] = value;
  });
  return result;
};

