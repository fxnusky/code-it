import { fail } from 'k6';
import { sleep } from 'k6';
import { Trend } from 'k6/metrics';
import http from 'k6/http';
import ws from 'k6/ws'

// Define custom metric for the header value
const server_receipt_to_delivery = new Trend('server_receipt_to_delivery_latency', true);

const WS_URL_PLAYER = 'ws://localhost:8000/ws/player';
const WS_URL_MANAGER = 'ws://localhost:8000/ws/manager';
const URL_CREATE_PLAYER = 'http://localhost:8000/players';
const URL_CREATE_ROOM = 'http://localhost:8000/rooms';

const n_rooms = 2
const playersPerRoom = 19;
export const options = {
  vus: playersPerRoom*n_rooms,
  iterations: playersPerRoom*n_rooms
};

const seed = __ENV.SEED
const NMESSAGES = 11

const quickSleep = (seconds) => {
    for (let i = 0; i < seconds * 2; i++){
        sleep(0.5)
    }
}

export default function () {
    
    const room_code = (seed + Math.floor(__VU/(playersPerRoom+1))).toString()
    if (__VU % (playersPerRoom + 1) === 1){
        
        console.log("manager" + room_code )
        const params = {
            headers: {
                'Content-Type': 'application/json',
            }
        };
        const token = "load-" + Math.random(999999999999999);
        const payload = JSON.stringify({ "token": token, "template_id": 1, "room_code": room_code })
        const res_create_room = http.post(URL_CREATE_ROOM, payload, params);     
        console.log(JSON.stringify(res_create_room.json()))
        if (res_create_room.status !== 200){
            fail("status "+ res_create_room.status + " with body " + JSON.stringify(res_create_room.json()))
        }  

const res = ws.connect(
  WS_URL_MANAGER + `?token=${encodeURIComponent(token)}&room_code=${encodeURIComponent(room_code)}`,
  {},
  function (socket) {
    let runningSleep = 30000;
    socket.setTimeout(() => {
      socket.send(JSON.stringify({ action: "start_game", question_id: 1 }));
      console.log("start_game");
    }, runningSleep);

    runningSleep += 2000;
    socket.setTimeout(() => {
      socket.send(JSON.stringify({ action: "end_question", question_id: 1 }));
      console.log("end_question");
    }, runningSleep);

    runningSleep += 2000;
    socket.setTimeout(() => {
      socket.send(JSON.stringify({ action: "show_ranking" }));
      console.log("show_ranking");
    }, runningSleep);

    runningSleep += 2000;
    socket.setTimeout(() => {
      socket.send(JSON.stringify({ action: "next_question", question_id: 2 }));
      console.log("next_question");
    }, runningSleep);

    runningSleep += 2000;
    socket.setTimeout(() => {
      socket.send(JSON.stringify({ action: "end_question", question_id: 2 }));
      console.log("end_question");
    }, runningSleep);

    runningSleep += 2000;
    socket.setTimeout(() => {
      socket.send(JSON.stringify({ action: "show_ranking" }));
      console.log("show_ranking");
    }, runningSleep);

    runningSleep += 2000;
    socket.setTimeout(() => {
      socket.send(JSON.stringify({ action: "next_question", question_id: 3 }));
      console.log("next_question");
    }, runningSleep);

    runningSleep += 2000;
    socket.setTimeout(() => {
      socket.send(JSON.stringify({ action: "end_question", question_id: 3 }));
      console.log("end_question");
    }, runningSleep);

    runningSleep += 2000;
    socket.setTimeout(() => {
      socket.send(JSON.stringify({ action: "show_ranking" }));
      console.log("show_ranking");
    }, runningSleep);

    runningSleep += 2000;
    socket.setTimeout(() => {
      socket.send(JSON.stringify({ action: "end_game" }));
      console.log("end_game");
    }, runningSleep);

    runningSleep += 10000;
    socket.setTimeout(() => {
      socket.close();
      console.log("socket closed");
    }, runningSleep);
  }
);

    }
    else{
        quickSleep(2);
        console.log("player" + room_code + " "+ seed)
        const params = {
            headers: {
                'Content-Type': 'application/json',
            }
        };
        const nickname = Math.random(999999999999999).toString();
        const payload = JSON.stringify({ "nickname": nickname, "room_code": room_code })
        const res_create_player = http.post(URL_CREATE_PLAYER, payload, params); 
        const response = res_create_player.json();    
        if (res_create_player.status !== 201){
            fail("status "+ res_create_player.status + " with body " + JSON.stringify(response))
        }
        let n_mes = 0
        console.log(response)
        const token = response.data["token"];
        const res = ws.connect(WS_URL_PLAYER+ `?room_code=${encodeURIComponent(room_code)}&nickname=${encodeURIComponent(nickname)}&token=${encodeURIComponent(token)}`, {}, function(socket){
            console.log("player"+ __VU)
            socket.on("open", () => {
                console.log("socket opened");
            });

            socket.on("message", (event) => {
                n_mes +=1
                const data = JSON.parse(event);
                if (data['X-Req-Insights']) {
                  console.log(data['X-Req-Insights'])
                    // Convert header value to number and add to metric
                    const parsedDict = parseStringToDict(data['X-Req-Insights']);
                    server_receipt_to_delivery.add(parsedDict["sent"]-parsedDict["received"]);
                }
                if (data["action"] == "game_ended"){
                    if (n_mes != NMESSAGES){
                        fail(n_mes + " !=" + NMESSAGES)
                    }
                    socket.close();
                }
            });
            socket.on("close", () => {
                console.log("closed")
            });
            socket.on("error", (e) => {
                console.log(e)
            });

        })
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
