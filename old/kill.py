import os
import signal
import socket
import psutil


def find_processes_using_port(port):
    """Find processes using a specific port."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port:
                    processes.append(proc)
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    return processes


def kill_processes_on_port(port):
    """Kill all processes using the specified port."""
    processes = find_processes_using_port(port)
    if not processes:
        print(f"No processes found using port {port}.")
        return

    for proc in processes:
        print(f"Killing process {proc.name()} (PID: {proc.pid}) on port {port}")
        os.kill(proc.pid, signal.SIGKILL)
    print(f"All processes on port {port} have been terminated.")


if __name__ == "__main__":
    PORT = 8000  # Change this to your desired port
    kill_processes_on_port(PORT)
