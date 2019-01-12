from pydtnsim import Pydtnsim
from argparse import ArgumentParser
import time


def get_option():
    parser = ArgumentParser()
    parser.add_argument('files', metavar='FILE', nargs='*')
    parser.add_argument('-n', '--node', type=int)
    parser.add_argument('-r', '--range', type=int)
    parser.add_argument('-s', '--seed', type=int)
    parser.add_argument('-p', '--process', type=int)
    return parser.parse_args()


def main():
    args = get_option()
    nagents = args.node or 50
    range_ = args.range or 40
    seed = args.seed or 1 # not used
    process = args.process or 1
    classes = list()

    for i in range(process):
        classes.append(
            Pydtnsim(
                id_=i,
                seed=i,
                nagents=nagents,
                range_=range_,
                monitor_class='Null'
            )
        )

    while True:
        for cls in classes:
            if cls.sched.is_running():
                cls.sched.cache_zones()
                for agent in cls.sched.agents:
                    agent.advance()
                for agent in cls.sched.agents:
                    agent.flush()
                cls.monitor.display_status()
                cls.monitor.update()
                cls.sched.advance()
                cls.is_finished()
            else:
                cls.monitor.close()
            stats = cls.get_stats()
            print("{0}{1}: {2}/{3}".format(
                cls.id_, cls.finished, len(stats["delivered_agents"]), nagents
            ))
        print(stats["time"])
        print("\u001B[{0}A".format(len(classes)+1), end="")



if __name__ == "__main__":
    main()
