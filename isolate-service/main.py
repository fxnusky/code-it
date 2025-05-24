import os
import subprocess
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import time
import asyncio

def current_milli_time():
    return int(time.time_ns() / 1_000_000)

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
async def execute_code(request: CodeExecutionRequest, response: Response):
    try:
        t1 = current_milli_time()
        # Step 1: Initialize the isolate box
        process = await asyncio.create_subprocess_exec(
            "isolate",
            "--init",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for the process to complete and capture output
        stdout, stderr = await process.communicate()
        
        # Convert bytes to string (text=True equivalent)
        box_path = stdout.decode().strip()
        error = stderr.decode()
        
        if process.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize isolate box: {error}"
            )

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
        t2 = current_milli_time()
        process = await asyncio.create_subprocess_exec(
            "isolate",
            "--run",
            f"--time={request.time_limit}",
            f"--mem={request.memory_limit}",
            "--meta=meta.txt",
            f"--box-id={box_number}",
            "--dir=/usr/bin/",
            "--dir=/usr/lib/",
            "--",
            *executable,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=box_dir
        )
        t3 = current_milli_time()
        # Wait for the process to complete and capture output
        stdout, stderr = await process.communicate()
        
        # Convert bytes to string if needed (text=True equivalent)
        output = stdout.decode()
        error = stderr.decode()

        meta = {}
        if meta_file.exists():
            with open(meta_file, 'r') as f:
                for line in f:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        meta[key.strip()] = value.strip()
        

        # Step 5: Clean up
        await asyncio.create_subprocess_exec(
            "isolate",
            "--cleanup",
            f"--box-id={box_number}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=box_dir
        )
        t4 = current_milli_time()
        response.headers["X-Req-Insights"] = f"received={t1},run_start={t2},run_end={t3},respond={t4}"
        return {
            "status":"success",
            "data": {
                "output": output,
                "error": error,
                "return_code": process.returncode,
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