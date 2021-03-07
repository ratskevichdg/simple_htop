import math
import datetime as dt
import psutil as ps


TEMPLATES = {
    'cpu_percent': {
        'cpu_status_bar': '{core}  [{percent_bar:.<50} {percent: >4}%]'
    },
    'memory_percent': {
        'memory_status_bar': 'Mem[{used_bar:.<50}{used:.2}G/{total:.2}G]'
    },
    'swap_percent': {
        'swap_status_bar': 'Swp[{used_bar:.<50}{used:.2}G/{total:.2}G]'
    },
    'uptime_info': 'Uptime: {uptime}',
    'load_avg_info': 'Load average: {load_avg}'

}


def get_cpu_percent():
        res = {'core': [], 'percent': [], 'percent_bar': []}
        cpus = ps.cpu_percent(interval=0.1, percpu=True)
        for i in range(len(cpus)):
            res['core'].append(i)
            res['percent'].append(cpus[i])
            res['percent_bar'].append('|' * math.ceil(cpus[i]/2))

        return res


def get_memory():
    res = {}
    memory_info = ps.virtual_memory()
    res['total'] = memory_info.total / (1024**3)
    res['used'] = memory_info.used / (1024**3)
    # посмотри тут подробнее, почему у тебя использованной больше, чем на самом
    # деле если сравнить с оригинальным htop
    res['used_bar'] = '|' * math.ceil(res['used'] * 100 / res['total'] / 2)

    return res


def get_swap_memory():
    res = {}
    swap_memory_info = ps.swap_memory()
    res['total'] = swap_memory_info.total / (1024**3)
    res['used'] = swap_memory_info.used / (1024**3)
    # посмотри тут подробнее, почему у тебя использованной больше, чем на самом
    # деле если сравнить с оригинальным htop
    res['used_bar'] = '|' * math.ceil(res['used'] * 100 / res['total'] / 2)

    return res


def get_uptime():
    current_uptime = (
        dt.datetime.today().replace(microsecond=0) - dt.datetime.fromtimestamp(ps.boot_time())
    )

    return current_uptime


def get_load_average():
    load_average = ps.getloadavg() 
    
    return '{:.2f} {:.2f} {:.2f}'.format(load_average[0], load_average[1], load_average[2])   


def show(**kwargs):
    cores = kwargs['cpu_percent']['core']
    percent_bars = kwargs['cpu_percent']['percent_bar']
    percents = kwargs['cpu_percent']['percent']
    for c, b, p in zip(cores, percent_bars, percents):
        if c % 2 == 0:
            print(TEMPLATES['cpu_percent']['cpu_status_bar'].format(
                core=c, 
                percent_bar=b, 
                percent=p), end='\t')
        else:
            print(TEMPLATES['cpu_percent']['cpu_status_bar'].format(
                core=c, 
                percent_bar=b, 
                percent=p))
    
    memory_info = kwargs['memory_percent']
    print(TEMPLATES['memory_percent']['memory_status_bar'].format(
            used_bar=memory_info['used_bar'],
            used=memory_info['used'],
            total=memory_info['total']))

    swap_info = kwargs['swap_percent']
    print(TEMPLATES['swap_percent']['swap_status_bar'].format(
            used_bar=swap_info['used_bar'],
            used=swap_info['used'],
            total=swap_info['total']))

    uptime = kwargs['uptime']
    print(TEMPLATES['uptime_info'].format(uptime=uptime))

    load_average = kwargs['load_avg']
    print(TEMPLATES['load_avg_info'].format(load_avg=load_average))



def main():
    cpu_percent_info = get_cpu_percent()
    memory_percent_info = get_memory()
    swap_percent_info = get_swap_memory()
    uptime = get_uptime()
    load_avg = get_load_average()
    show(cpu_percent=cpu_percent_info, 
        memory_percent=memory_percent_info,
        swap_percent=swap_percent_info,
        uptime=uptime,
        load_avg=load_avg)
    

 


if __name__ == '__main__':
    main()
