import math
import time
import datetime as dt
import psutil as ps
from pynput import keyboard

TEMPLATES = {
    'cpu_status_bar': '{core}  [{percent_bar:.<50} {percent: >4}%]',
    'memory_status_bar': 'Mem[{used_bar:.<50}{used:.2}G/{total:.2}G]',
    'swap_status_bar': 'Swp[{used_bar:.<50}{used:.2}G/{total:.2}G]',
    'uptime_info': 'Uptime: {uptime}',
    'load_avg_info': 'Load average: {load_avg}',
    'process_info': ('{pid: <6} {name: <50} {create_time}'
                     '{status: ^10} {nice: ^4} {memory_usage: <12} {username: <15}')
}


def get_cpu_percent():
    # get the cpu usage in percents for each core
    res = {'core': [], 'percent': [], 'percent_bar': []}
    cpus = ps.cpu_percent(interval=0.5, percpu=True)
    for i in range(len(cpus)):
        res['core'].append(i)
        res['percent'].append(cpus[i])
        res['percent_bar'].append('|' * math.ceil(cpus[i] / 2))
    return res


def get_memory():
    # get the RAM usage 
    res = {}
    memory_info = ps.virtual_memory()
    res['total'] = memory_info.total / (1024 ** 3)
    res['used'] = memory_info.used / (1024 ** 3)
    res['used_bar'] = '|' * math.ceil(res['used'] * 100 / res['total'] / 2)
    return res


def get_swap_memory():
    # get the swap memory usage
    res = {}
    swap_memory_info = ps.swap_memory()
    res['total'] = swap_memory_info.total / (1024 ** 3)
    res['used'] = swap_memory_info.used / (1024 ** 3)
    try:
        res['used_bar'] = '|' * math.ceil(res['used'] * 100 / res['total'] / 2)
    except ZeroDivisionError:
        res['used_bar'] = ''
    return res


def get_uptime():
    # get the current uptime
    current_uptime = (
            dt.datetime.today().replace(microsecond=0) - dt.datetime.fromtimestamp(ps.boot_time())
    )
    return current_uptime


def get_load_average():
    # get the average system load over the last 1, 5 and 15 minutes
    load_average = ps.getloadavg()
    return '{:.2f} {:.2f} {:.2f}'.format(load_average[0], load_average[1], load_average[2])


def get_processes_info():
    processes = []
    for process in ps.process_iter():
        # get all process info in one shot
        with process.oneshot():
            # get the process id
            pid = process.pid
            name = process.name()
            # get the time the process was spawned
            try:
                create_time = dt.datetime.fromtimestamp(process.create_time())
            except OSError:
                # system processes, using boot time instead
                create_time = dt.datetime.fromtimestamp(ps.boot_time())
            # get the status of the process (running, idle, etc.)
            status = process.status()
            try:
                # get the process priority (a lower value means a more prioritized process)
                nice = int(process.nice())
            except ps.AccessDenied:
                nice = 0
            try:
                # get the memory usage in bytes
                memory_usage = process.memory_full_info().uss
            except ps.AccessDenied:
                memory_usage = 0
            try:
                username = process.username()
            except ps.AccessDenied:
                username = "N/A"
        processes.append({
            'pid': pid, 'name': name, 'create_time': create_time, 'status': status,
            'nice': nice, 'memory_usage': memory_usage, 'username': username
        })
    return processes


def show(**kwargs):
    # clear a terminal window
    print(chr(27) + "[2J")
    print('Press <esc> to exit')

    cores = kwargs['cpu_percent']['core']
    percent_bars = kwargs['cpu_percent']['percent_bar']
    percents = kwargs['cpu_percent']['percent']
    for c, b, p in zip(cores, percent_bars, percents):
        if c % 2 == 0:
            print(TEMPLATES['cpu_status_bar'].format(
                core=c,
                percent_bar=b,
                percent=p), end='\t\t')
        else:
            print(TEMPLATES['cpu_status_bar'].format(
                core=c,
                percent_bar=b,
                percent=p))

    memory_info = kwargs['memory_percent']
    print(TEMPLATES['memory_status_bar'].format(
        used_bar=memory_info['used_bar'],
        used=memory_info['used'],
        total=memory_info['total']), end='\t')

    load_average = kwargs['load_avg']
    print(TEMPLATES['load_avg_info'].format(load_avg=load_average))

    swap_info = kwargs['swap_percent']
    print(TEMPLATES['swap_status_bar'].format(
        used_bar=swap_info['used_bar'],
        used=swap_info['used'],
        total=swap_info['total']), end='\t')

    uptime = kwargs['uptime']
    print(TEMPLATES['uptime_info'].format(uptime=uptime))

    processes = kwargs['processes']
    print(
        '{: <6} {: <50} {: <26} {: <10} {: <4} {: <12} {: <15}'.format(
            'pid', 'name', 'create time',
            'status', 'nice', 'memory usage',
            'username'
        )
    )
    print('-' * 128)
    for proc in processes[:-10:-1]:
        print(TEMPLATES['process_info'].format(**proc))


def on_press(key):
    global break_program
    if key == keyboard.Key.esc and break_program:
        break_program = False


def main():
    cpu_percent_info = get_cpu_percent()
    memory_percent_info = get_memory()
    swap_percent_info = get_swap_memory()
    uptime = get_uptime()
    load_avg = get_load_average()
    processes = get_processes_info()

    show(cpu_percent=cpu_percent_info,
         memory_percent=memory_percent_info,
         swap_percent=swap_percent_info,
         uptime=uptime,
         load_avg=load_avg,
         processes=processes)


if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    break_program = True
    while True:
        if break_program:
            main()
            time.sleep(0.5)
        else:
            break
