import sys
import json
import os
import signal

count = 0

def print_count(count):
    # Print the count on the same line, overwriting the previous output
    sys.stderr.write(f'\rSuccessfully processed JSON messages: {count}')
    sys.stderr.flush()

def kill_gunicorn():
    # Read Gunicorn PID from pidfile
    try:
        with open('gunicorn.pid', 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)
    except Exception as e:
        sys.stderr.write(f'\nError: Could not kill Gunicorn process: {e}\n')
        sys.stderr.flush()

try:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if line.startswith('{') or line.startswith('['):
            # Likely a JSON message
            try:
                data = json.loads(line)
                count += 1
                print_count(count)
            except json.JSONDecodeError:
                # Write incorrect JSON to error.out
                with open('error.out', 'w') as f:
                    f.write(line)
                sys.stderr.write('\nError: Invalid JSON detected. Exiting.\n')
                sys.stderr.flush()
                kill_gunicorn()
                # Terminate the script
                sys.exit(1)
        else:
            # Service message, print to stderr
            sys.stderr.write(f'\n{line}\n')
            sys.stderr.flush()
except KeyboardInterrupt:
    pass

