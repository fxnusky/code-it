import { check } from 'k6';
import { Trend } from 'k6/metrics';
import http from 'k6/http';

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
};

export default function () {
  const url = 'http://localhost:8001/execute';
  const params = {
    headers: {
      'Content-Type': 'application/json',
    }
  };
  const payload = JSON.stringify({
        "code": "print(2+2)",
        "time_limit": 2,
        "memory_limit": 65536,
        "language": "python"
    })

  const response = http.post(url, payload, params);

  check(response, {
    'status is 200': (r) => r.status === 200
  });

  if (response.headers['X-Req-Insights']) {
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

