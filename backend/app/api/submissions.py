from fastapi import APIRouter, HTTPException, Depends, status, Response
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
import time
import logging
import re 
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

router = APIRouter()

class CodeSubmissionRequest(BaseModel):
    code: str
    token: str
    question_id: int
    main_function: str
    time_limit: float = 2.0
    memory_limit: int = 65536
    language: str = 'python'

def normalize_value(value):
    if isinstance(value, str):
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                pass
    return value

def current_milli_time():
    return int(time.time_ns() / 1_000_000)

def get_python_test_code(code: str, main_function: str, input: str):
    return f"""import sys
import json
from io import StringIO

old_stdout = sys.stdout
sys.stdout = StringIO()

{code}

try:
    result = {main_function}({input})
    
    sys.stdout = old_stdout
    
    print(result)
except Exception as e:
    sys.stdout = old_stdout
    print(json.dumps({{"error": str(e)}}))
"""
def get_c_test_code(code: str, main_function: str, input: str):
    main_pattern = re.compile(
        r'(?P<prefix>^|\n)[ \t]*'
        r'(?P<return_type>int\s+|void\s+|)'
        r'main\s*'
        r'\((?P<args>[^)]*)\)\s*'
        r'(?P<declspec>__attribute__\s*\(\(.*?\)\)\s*)?' 
        r'\s*\{.*?\}\s*', 
        re.DOTALL | re.MULTILINE
    )
    
    code_excluding_main = main_pattern.sub('\n', code)
    
    new_main = f"""int main() {{
    int result = {main_function}({input});
    
    printf("%d", result);
    return 0;
}}"""
    
    return f"""#include <stdio.h>
#include <stdlib.h>
#include <string.h>

{code_excluding_main.strip()}

{new_main}"""

@router.post("/submit")
async def submit(request: CodeSubmissionRequest, res: Response, db: Session = Depends(get_db)):
    t1 = current_milli_time()
    try:
        player_repository = PlayerRepository(db)
        player_service = PlayerService(player_repository)
        if request.token[:5] != "load-":
            player_id = player_service.get_player_id_by_token(request.token)
        else:
            player_id = player_service.create_player_with_token(request.token)
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
        t2 = current_milli_time()
        execution_times = []
        for test_case in test_cases:
            t3 = current_milli_time()
            if request.language == 'python':
                test_code = get_python_test_code(request.code, request.main_function, test_case.input)
            else:
                test_code = get_c_test_code(request.code, request.main_function, test_case.input)
            t4 = current_milli_time()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://{os.getenv('ISOLATE_SERVICE_URL')}:8001/execute",
                    json={
                        "code": test_code,
                        "time_limit": request.time_limit,
                        "memory_limit": request.memory_limit,
                        "language": request.language
                    },
                    timeout=30.0
                )
                t5 = current_milli_time()
                result = response.json()
                logger.info(result)
                submission_id = submission["id"]
                case_id = test_case.case_id
                try:
                    if result["status"] == "success":
                        try:
                            obtained_output = json.loads(result["data"]["output"].strip())
                        except json.JSONDecodeError:
                            raw_output = result["data"]["output"].strip()
                            
                            if request.language == 'c':
                                obtained_output = raw_output
                            else:
                                try:
                                    obtained_output = literal_eval(raw_output)
                                except (ValueError, SyntaxError):
                                    obtained_output = raw_output
                        
                        try:
                            expected_evaluated = literal_eval(test_case.expected_output)
                        except (ValueError, SyntaxError):
                            expected_evaluated = test_case.expected_output
                        
                        if isinstance(expected_evaluated, (int, float)) and isinstance(obtained_output, (int, float)):
                            correct = math.isclose(obtained_output, expected_evaluated, rel_tol=1e-9)
                        elif isinstance(expected_evaluated, bool) or isinstance(obtained_output, bool):
                            correct = bool(expected_evaluated) == bool(obtained_output)
                        elif request.language == 'c':
                            correct = str(obtained_output) == str(expected_evaluated)
                        else:
                            correct = str(obtained_output).strip('\'"') == str(expected_evaluated).strip('\'"')
                            
                    else:
                        obtained_output = result["data"]["error"]
                        correct = False

                except Exception as e:
                    logger.error(f"Error evaluating test case: {str(e)}")
                    obtained_output = f"Evaluation error: {str(e)}"
                    correct = False
                test_case_execution_service.create_test_case_execution(submission_id, case_id, obtained_output, correct)
                t6 = current_milli_time()
                execution_times.append((t4-t3) + (t6-t5))
        execution_times_str = ':'.join(str(t) for t in execution_times)
        t7 = current_milli_time()
        earned_points = test_case_execution_service.compute_earned_points(submission_id, len(test_cases))
        submission_service.update_submission_points(submission_id, earned_points)
        t8 = current_milli_time()
        res.headers["X-Req-Insights"] = f"received={t1},prepare_exec={t2},executions={execution_times_str},end_exec={t7},end={t8}"
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "data": submission,
            "detail": "Submission created successfully",
        }
    except httpx.HTTPStatusError as e:
        logger.exception(e)
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
