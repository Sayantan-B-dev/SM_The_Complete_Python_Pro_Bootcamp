import psutil
import platform
import time
from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_size(bytes):
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"

def get_cpu_info():
    """Gather CPU statistics."""
    try:
        freq = psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {}
    except Exception:
        freq = {}
    try:
        load_avg = [round(x / psutil.cpu_count() * 100, 2) for x in psutil.getloadavg()] if hasattr(psutil, "getloadavg") else []
    except Exception:
        load_avg = []
    return {
        'percent': psutil.cpu_percent(interval=0.5),
        'per_cpu': psutil.cpu_percent(percpu=True, interval=0.5),
        'cores': psutil.cpu_count(logical=True),
        'physical_cores': psutil.cpu_count(logical=False),
        'freq': freq,
        'load_avg': load_avg
    }

def get_memory_info():
    """Gather memory statistics, handling swap errors."""
    mem = psutil.virtual_memory()
    try:
        swap = psutil.swap_memory()
        swap_dict = swap._asdict() if swap else {}
    except Exception:
        swap_dict = {}  # Swap unavailable or error
    return {
        'virtual': mem._asdict(),
        'swap': swap_dict
    }

def get_disk_info():
    """Gather disk partitions and usage, handling errors gracefully."""
    partitions = []
    for part in psutil.disk_partitions():
        try:
            # Attempt to get disk usage – skip if it fails
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append({
                'device': part.device,
                'mountpoint': part.mountpoint,
                'fstype': part.fstype,
                'total': get_size(usage.total),
                'used': get_size(usage.used),
                'free': get_size(usage.free),
                'percent': usage.percent
            })
        except (PermissionError, OSError, SystemError, FileNotFoundError) as e:
            # Log the error (optional) and skip this partition
            print(f"Skipping {part.mountpoint}: {e}")
            continue

    # Disk I/O (optional – may not work on all Windows systems)
    try:
        io = psutil.disk_io_counters()
        io_dict = io._asdict() if io else {}
    except Exception:
        io_dict = {}

    return {'partitions': partitions, 'io': io_dict}

def get_network_info():
    """Gather network interfaces and I/O, handling permission errors."""
    try:
        if_addrs = psutil.net_if_addrs()
        interfaces = {iface: [addr._asdict() for addr in addrs] for iface, addrs in if_addrs.items()}
    except Exception:
        interfaces = {}

    try:
        io = psutil.net_io_counters()
        io_dict = io._asdict() if io else {}
    except Exception:
        io_dict = {}

    try:
        connections = len(psutil.net_connections())
    except (psutil.AccessDenied, Exception):
        connections = -1  # or 0, depending on what you prefer

    return {
        'interfaces': interfaces,
        'io': io_dict,
        'connections': connections
    }

def get_sensors_info():
    """Gather temperature, fan, battery data."""
    sensors = {}
    if hasattr(psutil, "sensors_temperatures"):
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                sensors['temperatures'] = {name: [x._asdict() for x in entries] for name, entries in temps.items()}
        except Exception:
            pass
    if hasattr(psutil, "sensors_fans"):
        try:
            fans = psutil.sensors_fans()
            if fans:
                sensors['fans'] = {name: [x._asdict() for x in entries] for name, entries in fans.items()}
        except Exception:
            pass
    if hasattr(psutil, "sensors_battery"):
        try:
            batt = psutil.sensors_battery()
            if batt:
                sensors['battery'] = batt._asdict()
        except Exception:
            pass
    return sensors

def get_processes_info():
    """Return top 5 CPU and memory consuming processes."""
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pinfo = proc.info
            if pinfo['cpu_percent'] is not None and pinfo['memory_percent'] is not None:
                procs.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    # Sort and get top 5
    cpu_top = sorted(procs, key=lambda x: x['cpu_percent'], reverse=True)[:5]
    mem_top = sorted(procs, key=lambda x: x['memory_percent'], reverse=True)[:5]
    return {'cpu_top': cpu_top, 'mem_top': mem_top}

def get_system_info():
    """Basic system information, handling user list errors."""
    uname = platform.uname()
    boot_time = psutil.boot_time()
    try:
        users = [user._asdict() for user in psutil.users()]
    except Exception:
        users = []
    return {
        'hostname': uname.node,
        'system': f"{uname.system} {uname.release}",
        'version': uname.version,
        'machine': uname.machine,
        'processor': uname.processor,
        'boot_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(boot_time)),
        'uptime_seconds': time.time() - boot_time,
        'users': users
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def stats():
    """Endpoint returning all system stats as JSON."""
    data = {
        'cpu': get_cpu_info(),
        'memory': get_memory_info(),
        'disk': get_disk_info(),
        'network': get_network_info(),
        'sensors': get_sensors_info(),
        'processes': get_processes_info(),
        'system': get_system_info()
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)