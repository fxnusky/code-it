import os
import subprocess
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from pathlib import Path

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("isolate_runner")

class CodeExecutionRequest(BaseModel):
    code: str
    time_limit: Optional[float] = 2.0  # seconds
    memory_limit: Optional[int] = 65536  # KB

@app.post("/execute/python")
async def execute_code(request: CodeExecutionRequest):
    try:
        # Step 1: Initialize the isolate box
        logger.info("Initializing isolate box...")
        init_result = subprocess.run(
            ["isolate", "--init", "--box-id=60"],
            capture_output=True,
            text=True
        )
        
        if init_result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize isolate box: {init_result.stderr}"
            )
        
        box_path = init_result.stdout.strip()
        logger.info(f"Box initialized at: {box_path}")

        # Step 2: Prepare the code file
        box_dir = Path(box_path) / "box"
        os.chdir(box_dir)
        
        file_path = box_dir / "script.py"
        with open(file_path, 'w') as f:
            f.write(request.code)
        executable = ["python3", "script.py"]

        logger.info(f"Code written to {file_path}")

        # Step 3: Execute the code in isolate
        logger.info("Running code in isolate...")
        meta_file = box_dir / "meta.txt"
        
        executable = ["/usr/bin/python3", "/box/script.py"]

        run_result = subprocess.run([
            "isolate",
            "--run",
            f"--time={request.time_limit}",
            f"--mem={request.memory_limit}",
            "--meta=meta.txt",
            f"--box-id=60",
            "--dir=/usr/bin/",
            "--dir=/usr/lib/",
            "--",
            *executable
        ], capture_output=True, text=True, cwd=box_dir)

        # Step 4: Read output and metadata
        output = run_result.stdout
        error = run_result.stderr
        
        meta = {}
        if meta_file.exists():
            with open(meta_file, 'r') as f:
                for line in f:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        meta[key.strip()] = value.strip()
        
        logger.info(f"Execution completed. Status: {run_result.returncode}")

        # Step 5: Clean up
        logger.info("Cleaning up isolate box...")
        subprocess.run(["isolate", "--cleanup", "--box-id=60"], check=True)

        return {
            "output": output,
            "error": error,
            "return_code": run_result.returncode,
            "metadata": meta
        }

    except subprocess.CalledProcessError as e:
        logger.error(f"Subprocess error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Execution failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )