import { Player } from "@/app/game-manager/[room_code]/page";
import endpoint from "../endpoints.config";

type MessageHandler = (data: any) => void;
type WebSocketState = 'connecting' | 'open' | 'closing' | 'closed' | 'start';

export type GameMessage = {
  action: string,
  room_code?: string,
  state?: string,
  question_ids?: number[],
  players?: Player[],
  current_question_id?: number,
  nickname?: string,
  manager_connected?: boolean
  question?: Question,
};

export interface Question {
  id: number,
  description: string,
  time_limit: number,
  code_starter: string
}

class WsConnectionService {
  private socket: WebSocket | null = null;
  private messageHandler: MessageHandler | null = null;
  private connectionState: WebSocketState = 'start';
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private reconnectTimeout: NodeJS.Timeout | null = null;
  private currentConnectionParams: {
    type: 'player' | 'manager';
    roomCode?: string;
    nickname?: string;
    token?: string;
  } | null = null;

  async player_connect(roomCode: string, nickname: string, token: string): Promise<WebSocket> {
    if (this.socket && this.connectionState === 'open') {
      console.warn('WebSocket already connected');
      return this.socket;
    }

    this.currentConnectionParams = {
      type: 'player',
      roomCode,
      nickname,
      token
    };

    const wsUrl = `${endpoint.wsURL}/ws/player?room_code=${encodeURIComponent(roomCode)}&nickname=${encodeURIComponent(nickname)}&token=${encodeURIComponent(token)}`;
    return this.establishConnection(wsUrl);
  }

  async manager_connect(token: string, room_code: string): Promise<WebSocket> {
    if (this.socket && this.connectionState === 'open') {
      console.warn('WebSocket already connected');
      return this.socket;
    }

    this.currentConnectionParams = {
      type: 'manager',
      token,
      roomCode: room_code
    };

    const wsUrl = `${endpoint.wsURL}/ws/manager?token=${encodeURIComponent(token)}&room_code=${encodeURIComponent(room_code)}`;
    return this.establishConnection(wsUrl);
  }

  private async establishConnection(wsUrl: string): Promise<WebSocket> {
    return new Promise((resolve, reject) => {
      try {
        this.socket = new WebSocket(wsUrl);
        this.connectionState = 'connecting';
        this.reconnectAttempts = 0; 

        this.socket.onopen = () => {
          this.connectionState = 'open';
          this.reconnectAttempts = 0; 
          console.log('WebSocket connected');
          resolve(this.socket!);
        };

        this.socket.onerror = (error) => {
          console.error('WebSocket error:', error);
          if (!this.scheduleReconnect()) {
            this.cleanUp();
            reject(new Error(`WebSocket connection failed: ${error}`));
          }
        };

        this.socket.onclose = (event) => {
          if (!this.scheduleReconnect()) {
            this.connectionState = 'closed';
            console.log(`WebSocket disconnected: ${event.code} - ${event.reason}`);
            this.cleanUp();
          }
        };

        this.socket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data) as GameMessage;
            if (this.messageHandler) {
              this.messageHandler(data);
            }
          } catch (e) {
            console.error('Error parsing message:', e);
          }
        };

      } catch (error) {
        if (!this.scheduleReconnect()) {
          this.cleanUp();
          reject(new Error(`WebSocket initialization failed: ${error}`));
        }
      }
    });
  }

  private scheduleReconnect(): boolean {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      return false;
    }

    this.reconnectAttempts++;
    this.connectionState = 'connecting';

    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
    }

    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
    console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

    this.reconnectTimeout = setTimeout(() => {
      if (!this.currentConnectionParams) {
        console.error('No connection parameters available for reconnection');
        return;
      }

      let wsUrl: string;
      if (this.currentConnectionParams.type === 'player') {
        wsUrl = `${endpoint.wsURL}/ws/player?room_code=${encodeURIComponent(this.currentConnectionParams.roomCode!)}&nickname=${encodeURIComponent(this.currentConnectionParams.nickname!)}&token=${encodeURIComponent(this.currentConnectionParams.token!)}`;
      } else {
        wsUrl = `${endpoint.wsURL}/ws/manager?token=${encodeURIComponent(this.currentConnectionParams.token!)}&room_code=${encodeURIComponent(this.currentConnectionParams.roomCode!)}`;
      }

      this.establishConnection(wsUrl).catch(error => {
        console.error('Reconnection failed:', error);
      });
    }, delay);

    return true;
  }

  addMessageHandler(handler: MessageHandler): void {
    this.messageHandler = handler;
  }

  sendMessage(messageData: { [key: string]: any }): void {
    if (!this.socket || this.connectionState !== 'open') {
      console.error('WebSocket is not connected');
      return;
    }

    try {
      this.socket.send(JSON.stringify(messageData));
    } catch (error) {
      console.error('Error sending message:', error);
    }
  }

  getConnectionState(): string {
    return this.connectionState;
  }

  private cleanUp(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }

    if (this.socket) {
      this.socket.onopen = null;
      this.socket.onerror = null;
      this.socket.onclose = null;
      this.socket.onmessage = null;
      if (this.socket.readyState === WebSocket.OPEN) {
        this.socket.close();
      }
    }
    this.socket = null;
    this.connectionState = 'closed';
  }
}

export const connectionService = new WsConnectionService();