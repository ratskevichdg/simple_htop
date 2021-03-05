import psutil as ps
import math


# TEMPLATES = {
#     'cpu': {
#         'times': None
#     }
# }


def get_cpu_percent():
        res = {'core': [], 'percent': [], 'percent_bar': []}
        cpus = ps.cpu_percent(interval=0.2, percpu=True)
        for i in range(len(cpus)):
            res['core'].append(i)
            res['percent'].append(cpus[i])
            res['percent_bar'].append(math.ceil(cpus[i]/5))

        return res

def get_memory():
    res = {}
    memory_info = ps.virtual_memory()
    res['total'] = memory_info.total / (1024**3)
    res['used'] = memory_info.used / (1024**3)
    # посмотри тут подробнее, почему у тебя использованной больше, чем на самом
    # деле если сравнить с оригинальным htop
    res['used_bar'] = math.ceil(res['used'] * 100 / res['total'])

    return res

def get_swap_memory():
    res = {}
    swap_memory_info = ps.swap_memory()
    res['total'] = swap_memory_info.total / (1024**3)
    res['used'] = swap_memory_info.used / (1024**3)
    # посмотри тут подробнее, почему у тебя использованной больше, чем на самом
    # деле если сравнить с оригинальным htop
    res['used_bar'] = math.ceil(res['used'] * 100 / res['total'])

    return res

def show(**kwargs):
    for kwarg in kwargs:
        print(kwarg)

def main():
    #print(get_cpu_percent())
    print(get_memory())
    print(get_swap_memory())
    # pass


if __name__ == '__main__':
    main()
