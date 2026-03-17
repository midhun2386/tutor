"""
Unified Runner - Starts the FastAPI backend and Streamlit frontend concurrently.
Includes a self-healing mechanism to clear common Windows port conflicts.
"""
import subprocess
import os
import sys
import time
import requests
import re

def kill_port_owner(port):
    """Detects and kills any process owning the given port (Windows specific)."""
    try:
        # 1. Find the PID using netstat
        cmd = f'netstat -ano | findstr :{port} | findstr LISTENING'
        output = subprocess.check_output(cmd, shell=True, text=True)
        
        # Look for the PID (usually the last column)
        pids = re.findall(r'\s+(\d+)\s*$', output, re.MULTILINE)
        if pids:
            unique_pids = list(set(pids))
            print(f"🧹 Found zombie processes on port {port}: {unique_pids}. Cleaning up...")
            for pid in unique_pids:
                subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
            time.sleep(1) # Wait for OS to release the socket
            return True
    except Exception:
        pass
    return False

def run():
    print("🚀 Starting Vernacular AI Tutor (Web Version)...")
    
    # Self-healing: Clear port 8000 before starting
    kill_port_owner(8000)

    # 1. Start FastAPI in the background (Serving Web + API)
    api_cmd = [
        sys.executable, "-m", "uvicorn", 
        "api.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000"
    ]
    
    try:
        # Launch API
        api_proc = subprocess.Popen(
            api_cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True,
            bufsize=1
        )
        print("✅ Backend & Web Server started.")
        
        # Proactive wait for Backend
        print("⏳ Waiting for server to open port 8000...")
        max_retries = 30
        backend_ready = False
        backend_output = []
        
        import threading
        def collect_output(proc, output_list):
            try:
                for line in proc.stdout:
                    output_list.append(line.strip())
            except:
                pass
        
        output_thread = threading.Thread(target=collect_output, args=(api_proc, backend_output), daemon=True)
        output_thread.start()

        for i in range(max_retries):
            if api_proc.poll() is not None:
                break
            try:
                requests.get("http://127.0.0.1:8000/api/health", timeout=1)
                backend_ready = True
                print("\n" + "="*50)
                print("🌟 VERNACULAR AI TUTOR IS LIVE! 🌟")
                print("👉 URL: http://127.0.0.1:8000")
                print("="*50 + "\n")
                break
            except:
                time.sleep(1)
        
        if not backend_ready:
            if api_proc.poll() is not None:
                print("❌ Server crashed immediately. Status:", api_proc.returncode)
                print("\n".join(backend_output[-20:]))
                sys.exit(1)
        
        # Keep alive
        while True:
            if api_proc.poll() is not None:
                print("❌ Server crashed. Shutting down...")
                break
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        api_proc.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error in runner: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
