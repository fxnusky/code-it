'use client';
import { RequireAuth } from "../../../components/require_auth";
import styles from '../page.module.css';
import { useRouter } from 'next/navigation';
import { useAuth } from "../../../contexts/auth_context";
import RoomService from "../../../services/room.service";
import { ApiResponse } from "../../../services/api_response";
import { Button } from "@/components/ui/button"
import { useState } from "react";
import { LoadingState } from "../../../components/loading_state";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter
} from "@/components/ui/dialog"

const GAME_TEMPLATES = [
  { id: 1, title: "Template 1", description: "Three easy questions" },
  { id: 2, title: "Template 2", description: "20 test cases" },
  { id: 3, title: "Template 3", description: "Sorting questions" },
];

export default function Profile() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [templateId, setTemplateId] = useState(0);
  const [roomCode, setRoomCode] = useState('');
  const {token} = useAuth();

  async function handleStartGame(template_id: number, override: boolean = false) {
    try {
      setIsLoading(true);
      const response: ApiResponse | null = await RoomService.createRoom({ template_id, token, override });
      
      if (response && response.status === "success") {
        router.push(`/game-manager/${response.data["room_code"]}`);
      } else if (response?.status_code === 405) {
        console.log("ENTRA", response)
        setTemplateId(template_id)
        setRoomCode(response.data["room_code"])
        setDialogOpen(true); 
      } else {
        console.log(response?.status_code)
        console.error('Connection failed:', response?.detail);
      }
    } catch (error) {
      console.error('Connection failed:', error);
    } finally {
      setIsLoading(false);
    }
  }

  const handleLogout = () => {
    router.push('/login'); 
  };

  const handleContinueExistingGame = () => {
    router.push(`/game-manager/${roomCode}`);
    setDialogOpen(false)
  };
  const handleCreateNewGame = () => {
    handleStartGame(templateId, true)
    setDialogOpen(false)
  };

  return (
    <RequireAuth>
      <div className={styles.pageContainer}>
        <div className={styles.logoutContainer}>
          <Button onClick={handleLogout}>
            Log Out
          </Button>
        </div>

        {isLoading ? (
          <LoadingState text="Creating game..." />
        ) : (
          <div className={styles.templatesContainer}>
            <h1 className={styles.title}>Choose a Game Template</h1>
            <div className={styles.templatesGrid}>
              {GAME_TEMPLATES.map((template) => (
                <div key={template.id} className={styles.templateCard}>
                  <h3 style={{ fontWeight: "bold"}}>{template.title}</h3>
                  <p style={{ marginBottom: '1rem' }}>{template.description}</p>
                  <Button onClick={() => handleStartGame(template.id)}>
                    Start Game
                  </Button>
                </div>
              ))}
            </div>
          </div>
        )}

        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Game Session Limit Reached</DialogTitle>
              <DialogDescription>
                You already have an active game session. Would you like to continue your existing game or create a new one?
              </DialogDescription>
            </DialogHeader>
            <DialogFooter>
              <Button variant="outline" onClick={handleContinueExistingGame}>
                Continue Existing Game
              </Button>
              <Button onClick={handleCreateNewGame}>
                Create New Game
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </RequireAuth>
  );
}