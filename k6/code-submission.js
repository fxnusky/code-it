import { check } from 'k6';
import { Trend } from 'k6/metrics';
import { fail } from 'k6';
import http from 'k6/http';

const begin_code_execution = new Trend('begin_code_execution_latency', true);
const end_code_execution = new Trend('end_code_execution_latency', true);
const total = new Trend('total_latency', true);

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
  const url = 'http://localhost:8000/submit';
  const params = {
    headers: {
      'Content-Type': 'application/json',
    }
  };
  const payload = JSON.stringify({
        "code": "def add(a, b):\n    return a+b'",
        "token":  "load-" + Math.random(99999999999999).toString(),
        "question_id": 1,
        "main_function": "add",
        "time_limit": 2,
        "memory_limit": 65536,
        "language": "python"
    })

  const response = http.post(url, payload, params);

  if (response.status !== 200){
    fail(response.status +" !== 200")
  }
  check(response, {
    'status is 200': (r) => r.status === 200
    
  });

  if (response.headers['X-Req-Insights']) {
    const parsedDict = parseStringToDict(response.headers['X-Req-Insights']);
    const before_preparing_exec = Number(parsedDict["prepare_exec"])-Number(parsedDict["received"])
    parsedDict["executions"].forEach(exec => {
      begin_code_execution.add(before_preparing_exec + exec);
    })
    end_code_execution.add(parsedDict["end"]-parsedDict["end_exec"]);
    total.add(parsedDict["end"]-parsedDict["received"]);
  }
  
}
const parseStringToDict = (str) => {
  const result = {};
  console.log(str)
  str.split(',').forEach(pair => {
    const [key, value] = pair.split('=');
    result[key] = value; 
  });
  console.log(result)
  result["executions"] = result["executions"].split(':').map(Number); 
  return result;
};

