import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import time
import asyncio
import random

def current_milli_time():
    return int(time.time_ns() / 1_000_000)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000, https://code-it-git-main-fxnuskys-projects.vercel.app", "https://www.code-it-game.xyz"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeExecutionRequest(BaseModel):
    code: str
    time_limit: Optional[float] = 2.0  # seconds
    memory_limit: Optional[int] = 65536  # KB
    language: Optional[str] = 'python'

@app.post("/")
async def hello():
    return "hello world"

@app.post("/execute")
async def execute_code(request: CodeExecutionRequest, response: Response):
    try:
        t1 = current_milli_time()
        init = False
        while not init:
            box_number = str(random.randint(0, 999))
            process = await asyncio.create_subprocess_exec(
                "isolate", "--init", f"--box={box_number}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            box_path = stdout.decode().strip()
        
            if process.returncode == 0:
                init = True
        
        box_dir = Path(box_path) / "box"
        os.chdir(box_dir)

        # Normalize code formatting
        code = request.code.strip()
        language = request.language
        if language == "c":
            file_path = box_dir / "script.c"
            with open(file_path, 'w') as f:
                f.write(code)
            
            compile_process = await asyncio.create_subprocess_exec(
                "gcc", str(file_path), "-o", str(box_dir/"script"),
                stderr=asyncio.subprocess.PIPE
            )
            _, stderr = await compile_process.communicate()
            
            if compile_process.returncode != 0:
                error_msg = stderr.decode().strip()
                meta_file = box_dir / "meta.txt"
                meta = {}
                if meta_file.exists():
                    with open(meta_file, 'r') as f:
                        for line in f:
                            if ':' in line:
                                key, value = line.split(':', 1)
                                meta[key.strip()] = value.strip()
                await cleanup_box(box_number)
                return {
                    "status": "error",
                    "data": {
                        "output": "",
                        "error": error_msg,
                        "return_code": compile_process.returncode,
                        "metadata": meta
                    }
                }
            
            if not (box_dir / "script").exists():
                await cleanup_box(box_number)
                raise HTTPException(
                    status_code=500,
                    detail="Executable was not created after successful compilation"
                )
            
            # Make the executable executable
            os.chmod(box_dir / "script", 0o755)
            
            # Use relative path for execution
            executable = ["./script"]
        
        elif language == "python":
            file_path = box_dir / "script.py"
            
            with open(file_path, 'w') as f:
                f.write(request.code)
            executable = ["/usr/bin/python3", "/box/script.py"]
        
        else:
            await cleanup_box(box_number)
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language: {language}"
            )

        # Execute with resource limits
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
            "--processes=50", 
            "--",
            *executable,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=box_dir
        )

        t3 = current_milli_time()
        stdout, stderr = await process.communicate()
        
        # Parse results
        output = stdout.decode().strip()
        error = stderr.decode().strip()
        meta_file = box_dir / "meta.txt"
        meta = {}
        if meta_file.exists():
            with open(meta_file, 'r') as f:
                for line in f:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        meta[key.strip()] = value.strip()
        # Cleanup
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
            "status": "success",
            "data": {
                "output": output,
                "error": error,
                "return_code": process.returncode,
                "metadata": meta
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

async def cleanup_box(box_number: str):
    """Cleanup isolate box"""
    await asyncio.create_subprocess_exec(
        "isolate", "--cleanup", f"--box-id={box_number}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )