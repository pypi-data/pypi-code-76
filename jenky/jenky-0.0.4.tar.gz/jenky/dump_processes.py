from collections import defaultdict
from pathlib import Path
from typing import List, Dict

import psutil


def dump_processes(dirs: List[Path]) -> Dict[str, dict]:
    print(f'dump_processes {dirs}')
    processes_by_pid = {}
    username = psutil.Process().username()

    attrs = ['pid', 'ppid', 'name', 'cwd', 'exe', 'username', 'cmdline', 'create_time']

    for proc in psutil.process_iter(attrs=attrs, ad_value=None):
        info = proc.info
        if info.get('username', None) != username:
            continue
        if Path(info.get('cwd', '') or '') not in dirs:
            continue
        processes_by_pid[info['pid']] = info

    # return
    children_by_pid = defaultdict(lambda: [])
    for n in processes_by_pid.values():
        children_by_pid[n['ppid']].append(n)

    def taint_parents(node):
        # print(f'taint_parents {node["pid"]}')
        while node['ppid'] in processes_by_pid:
            node = processes_by_pid[node['ppid']]
            if 'taint' in node:
                break
            node['taint'] = True

    def taint_children(node):
        # print(f'taint_children {node["pid"]}')
        for child in children_by_pid[node['pid']]:
            if 'taint' not in child:
                child['taint'] = True
                taint_children(child)

    for node in processes_by_pid.values():
        if True or 'cwd' in node and node['cwd'] and Path(node['cwd']) in dirs:
            taint_children(node)
            taint_parents(node)
            node['taint'] = True

    def dump(node, indent, verbose):
        # print(f'dump {node["pid"]}')
        pid = node['pid']
        ppid = node['ppid']
        name = node['name']
        username = node['username']
        cwd = node.get('cwd', '')
        paths = [f.path for f in (node.get('open_files', []) or [])]
        cmdline = node.get('cmdline', []) or []
        print(indent + f'{pid} {ppid} {username} {name} {cwd} ' + ', '.join(cmdline) + ' ' + ', '.join(paths))
        # print(indent + f'{pid} {ppid} ' + str(node))
        for child in children_by_pid[pid]:
            if 'taint' in child:
                dump(child, indent + '  ', verbose)

    roots = [node for node in processes_by_pid.values() if node['ppid'] not in processes_by_pid and 'taint' in node]
    for root in roots:
        dump(root, '', True)

    return processes_by_pid
