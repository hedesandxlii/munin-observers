from munin import ObservableMixin, Observer


class Worker(ObservableMixin):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def do_work(self):
        self.notify()


class Manager(Observer[Worker]):
    def act(self, worker: Worker):
        print(f"Manager: Looking good, {worker.name}!")


if __name__ == "__main__":
    m = Manager()

    w1 = Worker("Theo")
    w1.add_observer(m)

    w2 = Worker("El")
    w2.add_observer(m)

    w1.do_work()
    w2.do_work()
