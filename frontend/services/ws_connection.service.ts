import endpoint from "../endpoints.config";

type MessageHandler = (data: any) => void;
type WebSocketState = 'connecting' | 'open' | 'closing' | 'closed';

class WsConnectionService {
  private socket: WebSocket | null = null;
  private messageHandlers: MessageHandler[] = [];
  private connectionState: WebSocketState = 'closed';

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
            const data = JSON.parse(event.data);
            this.messageHandlers.forEach(handler => handler(data));
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

  async manager_connect(token: string): Promise<WebSocket> {
    if (this.socket && this.connectionState === 'open') {
      console.warn('WebSocket already connected');
      return this.socket;
    }

    const wsUrl = `${endpoint.wsURL}/ws/manager?token=${encodeURIComponent(token)}`;
    
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
            const data = JSON.parse(event.data);
            this.messageHandlers.forEach(handler => handler(data));
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
    this.messageHandlers.push(handler);
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