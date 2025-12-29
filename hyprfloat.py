import os
import json
import subprocess
from socket import socket, AF_UNIX, SOCK_STREAM

SOCKET_PATH = f"{os.environ['XDG_RUNTIME_DIR']}/hypr/{os.environ['HYPRLAND_INSTANCE_SIGNATURE']}/.socket2.sock"

def hyprctl(cmd):
    subprocess.run(['hyprctl'] + cmd, capture_output=True)

def get_windows(workspace_id, class_filter=None):
    clients = json.loads(subprocess.run(['hyprctl', 'clients', '-j'], capture_output=True, text=True).stdout)
    windows = [c for c in clients if c['workspace']['id'] == workspace_id and not c['hidden']]
    if class_filter:
        windows = [w for w in windows if w['class'] == class_filter]
    return windows

def float_window(address):
    hyprctl(['dispatch', 'setfloating', f'address:{address}'])
    hyprctl(['dispatch', 'resizewindowpixel', 'exact', '1200', '800', f',address:{address}'])
    hyprctl(['dispatch', 'centerwindow', f',address:{address}'])

def tile_window(address):
    hyprctl(['dispatch', 'settiled', f'address:{address}'])

with socket(AF_UNIX, SOCK_STREAM) as sock:
    sock.connect(SOCKET_PATH)
    while True:
        event = sock.recv(1024).decode().strip()
        if not event:
            continue

        if event.startswith('openwindow>>'):
            data = event.split('>>')[1].split(',')
            if len(data) >= 3 and data[2] == 'Alacritty':
                address = f'0x{data[0]}'
                workspace_id = int(data[1])
                all_windows = get_windows(workspace_id)
                alacritty_windows = get_windows(workspace_id, 'Alacritty')
                
                if len(all_windows) == 1:
                    float_window(address)
                else:
                    for window in alacritty_windows:
                        tile_window(window['address'])
        
        elif event.startswith('closewindow>>'):
            workspace = json.loads(subprocess.run(['hyprctl', 'activeworkspace', '-j'], capture_output=True, text=True).stdout)
            workspace_id = workspace['id']
            all_windows = get_windows(workspace_id)
            alacritty_windows = get_windows(workspace_id, 'Alacritty')
            
            if len(all_windows) == 1 and len(alacritty_windows) == 1:
                float_window(alacritty_windows[0]['address'])