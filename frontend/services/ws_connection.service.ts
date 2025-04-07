import endpoint from "../endpoints.config";

type MessageHandler = (data: any) => void ;
type WebSocketState = 'connecting' | 'open' | 'closing' | 'closed';
export type GameMessage = {
  action: string,
  room_code?: string
};

class WsConnectionService {
  private socket: WebSocket | null = null;
  private messageHandler: MessageHandler | null = null;
  private connectionState: WebSocketState = 'closed';
  private messages: GameMessage[] = [];

  async player_connect(roomCode: string, nickname: string): Promise<WebSocket> {
    if (this.socket && this.connectionState === 'open') {
      console.warn('WebSocket already connected');
      return this.socket;
    }

    const wsUrl = `${endpoint.wsURL}/ws/player/${encodeURIComponent(roomCode)}?nickname=${encodeURIComponent(nickname)}`;
    
    return new Promise((resolve, reject) => {
      try {
        this.socket = new WebSocket(wsUrl);
        this.connectionState = 'connecting';

        this.socket.onopen = () => {
          this.connectionState = 'open';
          console.log('WebSocket connected');
          resolve(this.socket!);
        };

        this.socket.onerror = (error) => {
          console.error('WebSocket error:', error);
          this.cleanUp();
          reject(new Error(`WebSocket connection failed: ${error}`));
        };

        this.socket.onclose = (event) => {
          this.connectionState = 'closed';
          console.log(`WebSocket disconnected: ${event.code} - ${event.reason}`);
          this.cleanUp();
        };

        this.socket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data) as GameMessage;
            if (this.messageHandler){
              this.messageHandler(data);  
            }
            else{
              this.messages.push(data);
            }
          } catch (e) {
            console.error('Error parsing message:', e);
          }
        };

      } catch (error) {
        this.cleanUp();
        reject(new Error(`WebSocket initialization failed: ${error}`));
      }
    });
  }

  async manager_connect(token: string, template_id: number): Promise<WebSocket> {
    if (this.socket && this.connectionState === 'open') {
      console.warn('WebSocket already connected');
      return this.socket;
    }

    const wsUrl = `${endpoint.wsURL}/ws/manager?token=${encodeURIComponent(token)}&template_id=${encodeURIComponent(template_id)}`;
    
    return new Promise((resolve, reject) => {
      try {
        this.socket = new WebSocket(wsUrl);
        this.connectionState = 'connecting';

        this.socket.onopen = () => {
          this.connectionState = 'open';
          console.log('WebSocket connected');
          resolve(this.socket!);
        };

        this.socket.onerror = (error) => {
          console.error('WebSocket error:', error);
          this.cleanUp();
          reject(new Error(`WebSocket connection failed: ${error}`));
        };

        this.socket.onclose = (event) => {
          this.connectionState = 'closed';
          console.log(`WebSocket disconnected: ${event.code} - ${event.reason}`);
          this.cleanUp();
        };

        this.socket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data) as GameMessage;
            if (this.messageHandler){
              this.messageHandler(data);  
            }
            else{
              this.messages.push(data);
            }
          } catch (e) {
            console.error('Error parsing message:', e);
          }
        };

      } catch (error) {
        this.cleanUp();
        reject(new Error(`WebSocket initialization failed: ${error}`));
      }
    });
  }
  
  addMessageHandler(handler: MessageHandler): void {
    this.messageHandler = handler;
  }
  
  sendMessage(messageData: {[key: string]: any} ): void {
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

  popMessages(): GameMessage[] {
    const messages =  this.messages;
    this.messages = [];
    return messages;
  }

  private cleanUp(): void {
    if (this.socket) {
      this.socket.onopen = null;
      this.socket.onerror = null;
      this.socket.onclose = null;
      this.socket.onmessage = null;
    }
    this.socket = null;
    this.connectionState = 'closed';
  }
}

export const connectionService = new WsConnectionService();