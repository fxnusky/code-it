'use client';
import { RequireAuth } from "../../../components/require_auth";
import styles from '../page.module.css';
import { useRouter } from 'next/navigation';
import { useAuth } from "../../../contexts/auth_context";
import { useWSConnection } from "../../../contexts/ws_connection_context";

export default function Profile() {
  const router = useRouter();
  const connectionService = useWSConnection();

  const {token} = useAuth();

  const connect = async () => {
    try {
        // TEMPLATE_ID HARDCODED TO 1
        await connectionService.manager_connect(token, 1);
        
    } catch (error) {
        console.error('Connection failed:', error);
    }
  };
  async function handleStartGame(){
      try{
        connect(); 
        
        await new Promise((resolve, reject) => {
            const checkConnection = () => {
                if (connectionService.getConnectionState() === "open") {
                    resolve(true);
                } else if (connectionService.getConnectionState() === "closed") {
                    reject(new Error("Connection failed"));
                } else {
                    setTimeout(checkConnection, 100);
                }
            };
            checkConnection();
        });
        router.push("/game-manager");
      }
      catch(e){
        console.error(e);
      }
  }

  return (
    <RequireAuth>
      <div className={styles.container}>
          <button className={styles.primaryButton} onClick={handleStartGame}>
              Start a Game
          </button>
      </div>
    </RequireAuth>
  );
}