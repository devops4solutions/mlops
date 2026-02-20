import sys
import subprocess

def main():
    # SageMaker runs: docker run <image> serve
    # If first arg is "serve", start uvicorn
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        cmd = ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8080"]
        raise SystemExit(subprocess.call(cmd))

    # Otherwise, run whatever was passed
    if len(sys.argv) > 1:
        raise SystemExit(subprocess.call(sys.argv[1:]))

    # Default
    cmd = ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8080"]
    raise SystemExit(subprocess.call(cmd))

if __name__ == "__main__":
    main()