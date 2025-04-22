import os
import subprocess
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeExecutionRequest(BaseModel):
    code: str
    time_limit: Optional[float] = 2.0  # seconds
    memory_limit: Optional[int] = 65536  # KB

@app.post("/execute/python")
async def execute_code(request: CodeExecutionRequest):
    try:
        # Step 1: Initialize the isolate box
        init_result = subprocess.run(
            ["isolate", "--init"],
            capture_output=True,
            text=True
        )
        
        if init_result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize isolate box: {init_result.stderr}"
            )
        
        box_path = init_result.stdout.strip()

        # Step 2: Prepare the code file
        box_dir = Path(box_path) / "box"
        box_number = box_path.split("/")[-1]
        os.chdir(box_dir)
        
        file_path = box_dir / "script.py"
        with open(file_path, 'w') as f:
            f.write(request.code)
        executable = ["python3", "script.py"]

        # Step 3: Execute the code in isolate
        meta_file = box_dir / "meta.txt"
        
        executable = ["/usr/bin/python3", "/box/script.py"]

        run_result = subprocess.run([
            "isolate",
            "--run",
            f"--time={request.time_limit}",
            f"--mem={request.memory_limit}",
            "--meta=meta.txt",
            f"--box-id={box_number}",
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
        

        # Step 5: Clean up
        subprocess.run(["isolate", "--cleanup", f"--box-id={box_number}"], check=True)

        return {
            "status":"success",
            "data": {
                "output": output,
                "error": error,
                "return_code": run_result.returncode,
                "metadata": meta
            }
        }

    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status="error",
            status_code=500,
            detail=f"Execution failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status="error",
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )