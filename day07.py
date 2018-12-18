#!/usr/bin/env python3

raw = []
with open('input/day7.txt') as file:
    for line in file:
        raw.append(line.rstrip('\n'))


steps = {}
possible = set()
for line in raw:
    step = line.split()
    upstream = step[1]
    downstream = step[7]
    steps.setdefault(upstream, dict()).setdefault('down',set()).add(downstream)
    for i in downstream:
        steps.setdefault(downstream, dict()).setdefault('up',set()).add(upstream)

steps

done = []
queue = []
up = set(steps.keys())
down = {j for i in steps.values() for j in i.get('down',[])}
possible = up | down
buffer = list(up - down)


class Sleigh():
    def __init__(self, raw):
        steps = {}
        for line in raw:
            step = line.split()
            upstream = step[1]
            downstream = step[7]
            steps.setdefault(upstream, dict()).setdefault('down',set()).add(downstream)
            for i in downstream:
                steps.setdefault(downstream, dict()).setdefault('up',set()).add(upstream)
        self.steps = steps
        self.done = []
        up = set(steps.keys())
        down = {j for i in steps.values() for j in i.get('down',[])}
        possible = up | down
        self.queue = sorted(list(up - down))
        self.in_progress = set()

    def refresh_queue(self):
        done = set(self.done)
        current_queue = set(self.queue)
        in_progress = self.in_progress
        possible = set()
        for node,updown in self.steps.items():
            if node not in done:
                continue
            for down in updown.get('down',set()):
                possible |= set(down)
        new_queue = list((possible | current_queue) - done - in_progress)
        new_queue.sort()
        self.queue = new_queue

    def start_step(self, step):
        idx = self.queue.index(step)
        self.in_progress.add(self.queue.pop(idx))

    def finish_step(self, step):
        self.in_progress.remove(step)
        self.done += step
        self.refresh_queue()


def ready_nodes(buffer):
    ready = []
    for i,val in enumerate(buffer):
        upstream = steps[val].get('up',set())
        if len(upstream - set(done)) == 0:
            ready.append(i)
    return ready

class Worker():
    def __init__(self):
        self.step = None
        self.time = 0

    def increment(self):
        if self.step is not None:
            self.time -= 1
            if self.time <= 0:
                done = self.step
                self.step = None
                return done
            else:
                return None
    
    def add(self, step, time):
        self.time = time
        self.step = step
        return self

   
assert Worker().step == None
assert Worker().time == 0
assert Worker().add('C',1).increment() == 'C'


class Workers(Worker):
    def __init__(self, worker_count, default_time):
        self.workers = [Worker() for i in range(worker_count)]
        self.done = []
        self.elapsed_time = 0
        self.default_time = default_time
            
    def increment(self):
        out = []
        for worker in self.workers:
            status = worker.increment()
            if status is not None:
                out.append(status)
                print(f"Finished: {status}, Total time {self.elapsed_time}")
                
        self.done.extend(out)
        self.elapsed_time += 1
        return out
    
    def available(self):
        return [worker for worker in self.workers if worker.step is None]

    def employ(self, step):
        ready = self.available()
        time = self.calc_time(step)
        if ready:
            ready[0].add(step, time)
            print(f"Employed {step} for time {time}")
    
    def in_progress(self):
        return set([x.step for x in self.workers if x.step])
    
    def calc_time(self, step):
        print(step)
        return self.default_time + ord(step) - 65 + 1

assert Workers(5, 60).workers[0].time == 0

sleigh = Sleigh(raw)
workers = Workers(5, 60)


while len(sleigh.steps) > len(sleigh.done):
    ready = min(len(workers.available()), len(sleigh.queue))
    if ready:
        queue = sleigh.queue[0:ready]
        for next_up in queue:
            print(f"Next up: {next_up} from buffer {sleigh.queue[0]} and workers {len(workers.available())}")
            workers.employ(next_up)
            sleigh.start_step(next_up)
    
    done = workers.increment()
    if len(done) > 0:
        print(f"Done: {done}")
    for step in done:
        sleigh.finish_step(step)
    
print(f"Order: {sleigh.done} in Time: {workers.elapsed_time + 1}")

