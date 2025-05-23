from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
import httpx
from ..services.test_case_service import TestCaseService
from ..repositories.test_case_repository import TestCaseRepository
from ..services.submission_service import SubmissionService
from ..repositories.submission_repository import SubmissionRepository
from ..services.test_case_execution_service import TestCaseExecutionService
from ..repositories.test_case_execution_repository import TestCaseExecutionRepository
from ..services.player_service import PlayerService
from ..repositories.player_repository import PlayerRepository
from sqlalchemy.orm import Session
from ..database import get_db
import json
import math
from ast import literal_eval

router = APIRouter()

class CodeSubmissionRequest(BaseModel):
    code: str
    token: str
    question_id: int
    main_function: str
    time_limit: float = 2.0
    memory_limit: int = 65536

@router.post("/submit/python")
async def submit_python(request: CodeSubmissionRequest, db: Session = Depends(get_db)):
    try:
        player_repository = PlayerRepository(db)
        player_service = PlayerService(player_repository)
        player_id = player_service.get_player_id_by_token(request.token)

        submission_repository = SubmissionRepository(db)
        submission_service = SubmissionService(submission_repository)
        submission = submission_service.create_submission(request.question_id, player_id, request.code)
        if not submission or not submission["id"]:
            raise HTTPException(
                status_code=500,
                detail="Error creating the submission. Submission:" + str(submission)
            )
        test_case_repository = TestCaseRepository(db)
        test_case_service = TestCaseService(test_case_repository)
        test_cases = test_case_service.get_test_cases_by_question_id(request.question_id)

        if not test_cases:
            raise HTTPException(
                status_code=404,
                detail="No test cases found for this question"
            )

        test_case_execution_repository = TestCaseExecutionRepository(db)
        test_case_execution_service = TestCaseExecutionService(test_case_execution_repository)
        for test_case in test_cases:
            test_code = f"""import sys
import json
from io import StringIO

# Redirect stdout to suppress prints
old_stdout = sys.stdout
sys.stdout = StringIO()

{request.code}

try:
    # Call the main function with test case input
    result = {request.main_function}({test_case.input})
    
    # Restore stdout
    sys.stdout = old_stdout
    
    # Return only the result as JSON
    print(json.dumps({{"result": result}}))
except Exception as e:
    sys.stdout = old_stdout
    print(json.dumps({{"error": str(e)}}))
"""
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://isolate-service:8001/execute/python",
                    json={
                        "code": test_code,
                        "time_limit": request.time_limit,
                        "memory_limit": request.memory_limit
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                submission_id = submission["id"]
                case_id = test_case.case_id
                try:
                    if result["status"] == "success":
                        obtained_output = json.loads(result["data"]["output"].strip())["result"]
                        
                        try:
                            expected_evaluated = literal_eval(test_case.expected_output)
                        except (ValueError, SyntaxError):
                            expected_evaluated = test_case.expected_output 
                        
                        if isinstance(expected_evaluated, (int, float)) and isinstance(obtained_output, (int, float)):
                            correct = math.isclose(obtained_output, expected_evaluated, rel_tol=1e-9)
                        else:
                            correct = obtained_output == expected_evaluated
                    else:
                        obtained_output = result["data"]["error"]
                        correct = False

                except json.JSONDecodeError:
                    obtained_output = "Invalid output format"
                    correct = False
                test_case_execution_service.create_test_case_execution(submission_id, case_id, obtained_output, correct)

        earned_points = test_case_execution_service.compute_earned_points(submission_id, len(test_cases))
        submission_service.update_submission_points(submission_id, earned_points)
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "data": submission,
            "detail": "Submission created successfully",
        }
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
