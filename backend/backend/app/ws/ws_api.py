import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from ..services.game_connection_service import GameConnectionService
from .message_handlers import handle_manager_message, handle_player_message
from ..database import get_db
from ..services.auth_service import AuthService
from ..repositories.user_repository import UserRepository
from ..services.question_service import QuestionService
from ..repositories.question_repository import QuestionRepository
from ..services.player_service import PlayerService
from ..repositories.player_repository import PlayerRepository
from ..services.submission_service import SubmissionService
from ..repositories.submission_repository import SubmissionRepository
from ..services.test_case_execution_service import TestCaseExecutionService
from ..repositories.test_case_execution_repository import TestCaseExecutionRepository
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


router = APIRouter()

game_connection_service = GameConnectionService()

@router.websocket("/ws/player")
async def websocket_player_endpoint(websocket: WebSocket, token: str = Query(...),  room_code: str = Query(...), nickname: str = Query(...), db: Session = Depends(get_db)):
    try:
        
        player_repository = PlayerRepository(db)
        player_service = PlayerService(player_repository)
        player_id = player_service.verify_token(token, room_code)
        if not player_id:
            await websocket.close()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This player is not authorized to connect to this room."
            )
        question = None
        state = game_connection_service.state
        submission_repository = SubmissionRepository(db)
        submission_service = SubmissionService(submission_repository)
        if game_connection_service.state == "question" and game_connection_service.current_question_id:
            question_repository = QuestionRepository(db)
            question_service = QuestionService(question_repository)
            question = question_service.get_question_by_id(game_connection_service.current_question_id)

            submission = submission_service.get_submission_by_question_player(game_connection_service.current_question_id, player_id)
            if submission:
                state = "question_submitted"
        await game_connection_service.connect_player(websocket, room_code, player_id)

        test_case_execution_repository = TestCaseExecutionRepository(db)
        test_case_execution_service = TestCaseExecutionService(test_case_execution_repository)

        question_results = {}
        if game_connection_service.current_question_id and game_connection_service.state == "question_results":
            points = submission_service.get_question_results_by_player(player_id, game_connection_service.current_question_id)
            test_case_executions = test_case_execution_service.get_question_results_by_player(player_id, game_connection_service.current_question_id)
            question_results = {
                "total_points": points["total_points"],
                "question_points": points["question_points"],
                "test_case_executions": test_case_executions
            }
        await game_connection_service.send_message({
            "action": "status", 
            "state": state, 
            "room_code": room_code, 
            "nickname": nickname, 
            "manager_connected": game_connection_service.rooms[room_code]["manager"] != None,
            "question": question,
            "question_results": question_results
            }, 
            websocket)
        await game_connection_service.send_manager_message({"action": "player_joined"}, room_code)
       
        while True:
            try:
                data = await websocket.receive_json()
                await handle_player_message(data, room_code, websocket, game_connection_service)
                
            except WebSocketDisconnect:
                await game_connection_service.disconnect_player(websocket, room_code, player_id)
                await game_connection_service.send_manager_message({"action": "player_disconnected"})

    except WebSocketDisconnect:
        await game_connection_service.disconnect_player(websocket, room_code, player_id)
        await game_connection_service.send_manager_message({"action": "player_disconnected"})
        
        
    except Exception as e:
        logger.error(str(e))
    
@router.websocket("/ws/manager")
async def websocket_manager_endpoint(websocket: WebSocket, token: str = Query(...),  room_code: str = Query(...), db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        user_repository = UserRepository(db)
        auth_service = AuthService(user_repository)
        user = auth_service.get_or_create_user(token)
        if not user.active_room == room_code:
            await websocket.close()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This user is not authorized to manage this room."
            )
        game_connection_service.set_room_manager(user.active_room, websocket)
        
        question_repository = QuestionRepository(db)
        question_service = QuestionService(question_repository)
        question_ids = question_service.get_sorted_question_ids(room_code)

        question = None
        if game_connection_service.state == "question" and game_connection_service.current_question_id:
            question = question_service.get_question_by_id(game_connection_service.current_question_id)
        
        player_repository = PlayerRepository(db)
        player_service = PlayerService(player_repository)
        players = player_service.get_players_by_room_code(room_code)

        submission_repository = SubmissionRepository(db)
        submission_service = SubmissionService(submission_repository)
        result_stats = {}
        if game_connection_service.current_question_id and game_connection_service.state == "question_results":
            result_stats = submission_service.get_question_results_stats(room_code, game_connection_service.current_question_id)
        await game_connection_service.send_message({
            "action": "status", 
            "state": game_connection_service.state, 
            "question_ids": question_ids, 
            "players": players, 
            "current_question_id": game_connection_service.current_question_id,
            "question": question,
            "stats": result_stats,
            "submissions": submissions
            }, websocket)
        await game_connection_service.broadcast_players({"action": "manager_connected"}, room_code)
    except Exception as e:
        logger.error(str(e))
        
    try:
        test_case_execution_repository = TestCaseExecutionRepository(db)
        test_case_execution_service = TestCaseExecutionService(test_case_execution_repository)
        while True:
            try:
                data = await websocket.receive_json()
                await handle_manager_message(data, room_code, game_connection_service, db, question_service, submission_service, test_case_execution_service)
            except WebSocketDisconnect:
                await game_connection_service.disconnect_manager(room_code)
                await game_connection_service.broadcast_players({"action": "manager_disconnected"}, room_code)
    except Exception as e:
        logger.error(str(e))
