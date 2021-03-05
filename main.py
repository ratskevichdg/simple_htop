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

    

def show(**kwargs):
    for kwarg in kwargs:
        print(kwarg)

def main():
    print(get_cpu_percent())
    # pass

if __name__ == '__main__':
    main()
