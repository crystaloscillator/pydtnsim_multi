#!/usr/bin/env python3
#
# A simulator for DTN routing with several agent/mobility models.
# Copyright (c) 2010-2015, Hiroyuki Ohsaki.
# All rights reserved.
#
# Id: $
#

import os
import random
import sys

import dtnsim
import dtnsim.agent
import dtnsim.mobility
import dtnsim.mobility.graph
import dtnsim.monitor
import dtnsim.path

from perl import die, warn, getopts
import tbdump


class Pydtnsim:
    MAX_VELOCITY = 4000 / 60 / 60  # maximum node velocity [m/s]
    MIN_VELOCITY = MAX_VELOCITY / 2  # minimum node velocity [m/s]
    MIN_PAUSE = 0  # minimum pause time [s]
    MAX_PAUSE = 5 * 60  # maximum pause time [s]

    @classmethod
    def usage():
        prog = os.path.basename(sys.argv[0])
        die(f"""
    usage: {prog} [-v] [-s #] [-n #] [-r range] [-I id[,id]...] [-m mobility] [-p path] [-a agent] [-M monitor]
      -v            verbose mode
      -s #          seed of random number generator
      -n #          number of agents
      -r range      communication range [m]
      -I id[,id...] initial infected nodes
      -m mobility   name of mobility class (Fixed/FullMixed/LevyWalk/LimitedRandomWaypoint/RandomWalk/RandomWaypoint/graph.Fixed/graph.Sequential/graph.RandomWalk/grpah.CRWP)
      -p path       name of path class (NONE/Line/Grid/Voronoi)
      -a agent      name of agent class (CarryOnly/Random/Epidemic/P_BCAST/SA_BCAST/HP_BCAST/ProPHET)
      -M monitor    name of monitor class (Null/Log/Cell)
    """)

    def __init__(self,
                 id_=1,
                 verbose=False, seed=1, nagents=50, range_=40, init_infected=[1],
                 mobility_class='graph.CRWP', path_class='Voronoi',
                 agent_class='P_BCAST', monitor_class='Cell'
    ):
        self.id_ = id_
        self.verbose = verbose
        self.seed = seed
        self.nagents = nagents
        self.range_ = range_
        self.init_infected = init_infected
        self.mobility_class = mobility_class
        self.path_class = path_class
        self.agent_class = agent_class
        self.monitor_class = monitor_class
        self.delivered_agents = set(self.init_infected)
        self.finished = ""
        self.finish_time = 0

        # initialize random number generator
        random.seed(self.seed)

        self.sched = dtnsim.Scheduler(max_time=1000000, delta=5)
        cls = eval('dtnsim.monitor.' + self.monitor_class)

        self.monitor = cls(scheduler=self.sched)
        self.monitor.open()

        cls = eval('dtnsim.path.' + self.path_class)
        self.path = cls(npoints=100)
        self.monitor.display_path(self.path)

        self.create_agents(
            self.sched, self.monitor, self.agent_class, self.nagents, self.range_,
            self.init_infected, self.mobility_class, self.path)
        self.monitor.display_agents()

    def create_agents(self, sched, monitor, agent_class, nagents, range_, init_infected,
                      mobility_class, path):
        """Create the number NAGENTS of agents of the class AGENT_CLASS, whose
        mobility models are initialized as MOBILITY_CLASS class.  INIT_INFECTED is
        a list of identifiers (starting from 1) of initially-infected agents."""

        def vel_func():
            """A callback function for returning the velocity of an agent."""
            return random.uniform(Pydtnsim.MIN_VELOCITY, Pydtnsim.MAX_VELOCITY)

        def pause_func():
            """A callback function for returning the pause time of an agent."""
            return random.uniform(Pydtnsim.MIN_PAUSE, Pydtnsim.MAX_PAUSE)

        for i in range(nagents):
            cls = eval('dtnsim.mobility.' + mobility_class)
            mobility = cls(vel_func=vel_func, pause_func=pause_func, path=path)
            cls = eval('dtnsim.agent.' + agent_class)
            agent = cls(
                scheduler=sched, mobility=mobility, monitor=monitor, pydtnsim=self, range_=range_)

        for i in init_infected:
            # store a message (the first message sent from agent 1 destined for agent 2)
            sched.agent_by_id(i).received['1-2-1'] = 1

    def get_stats(self):
        return {
            "time": self.sched.time,
            "tx_total": self.monitor.tx_total,
            "rx_total": self.monitor.rx_total,
            "dup_total": self.monitor.dup_total,
            "uniq_total": self.monitor.uniq_total,
            "delivered_total": self.monitor.delivered_total,
            "uniq_delivered_total": self.monitor.uniq_delivered_total,
            "delivered_agents": self.delivered_agents,
            "finished": self.finished,
            "finish_time": self.finish_time
        }

    def set_delivered_agents(self, dst_agent):
        self.delivered_agents.add(dst_agent)

    def is_finished(self):
        if not self.finished and self.nagents <= len(self.delivered_agents):
            self.finish_time = self.sched.time
            self.finished = "finished at {}".format(self.finish_time)

    def main(self):
        # the main loop
        while self.sched.is_running():
            self.sched.cache_zones()
            for agent in self.sched.agents:
                agent.advance()
            for agent in self.sched.agents:
                agent.flush()
            self.monitor.display_status()
            self.monitor.update()
            self.sched.advance()
        self.monitor.close()

if __name__ == "__main__":
    pds1 = Pydtnsim(monitor_class='Null')
    classes = [pds1]
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
            else:
                cls.monitor.close()
            stats = cls.get_stats()
            print(stats["time"], len(stats["delivered_agents"]))
