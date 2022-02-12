# Munin


The observer pattern implementation with a cool name.


### Features:
- Simple observer implementation with Observer (`Protocol`) and ObservableMixin.
- Concept of *discreteness* to break infinite callback loops>
- Simple, **No python wizardry!**


### Goals:
- **Simplicity**: Limit python wizardry
- **Concise**: *SLOC* should never reach thousands
- **Flexible**: Should be able to cover every Pythonista's observing needs.
- **Typed**: Keep `munin` typed and type-safe to the furthest extent possible.
- **Well tested**: Code coverage should be *"at least"* 100%.

## Examples



```python
# examples/simple.py
import muninn as mn


class Worker(mn.ObservableMixin):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def do_work(self):
        self.notify()


class Manager(mn.Observer):
    def update(self, worker: Worker):
        print(f"Manager: Looking good, {worker.name}!")


if __name__ == "__main__":
    m = Manager()

    w1 = Worker("Theo")
    w1.add_observer(m)

    w2 = Worker("El")
    w2.add_observer(m)

    w1.do_work()
    w2.do_work()

# Output
Manager: Looking good, Theo!
Manager: Looking good, El!
```
