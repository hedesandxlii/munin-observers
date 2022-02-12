# Munin


The observer pattern implementation with a cool name.


### Features:
- Simple observer implementation with Observer (`Protocol`) and ObservableMixin.
- Concept of *"discretion"* to break infinite call-back loops.
- Simple, **No python wizardry!**
- Easily control behaviour with decorators `@notify` and `@discrete`.

### Goals:
- **Simplicity**: Limit python wizardry
- **Concise**: *SLOC* should never reach thousands
- **Flexible**: Should be able to cover every Pythonista's observing needs.
- **Typed**: Keep `munin` typed and type-safe to the furthest extent possible.
- **Well tested**: Code coverage should be *"at least"* 100%.

### Walk-through
Say we have a text field from some GUI-framework, `FrameworkTextField`. It's common for
GUI-frameworks to offer some synchronization mechanism of their own to handle certain events
(user input in a text field, for example), be it signals, call-backs or black magic.

```python
class FrameworkTextField:
    def __init__(self):
        self.content: str = "<Placeholder text>"
        self.content_changed_callbacks: List[Callable[str, ...]] = []

    def set_content(self, new_content):
        self.content = new_content
        self.on_content_changed()

    def on_content_changed(self):
        for callback in self.content_changed_callbacks:
            callback(self.content)
```

One is easily tempted to use the framework's synchronization mechanisms to keep their model synced,
but as in Uncle Bob's words; *"We should be sceptic of frameworks"* and most important of all:
We should not depend on them.

To separate view and model, you can do something like this with `munin`:

```python
from munin import Observer, ObservableMixin

class MyTextModel(ObservableMixin):
    """
    Basically an observable str.
    """
    def __init__(self):
        super().__init__()
        self.text: str = ""

    def set_text(self, new_text: str):
        self.text = new_text
        self.notify()  # alternatively decorator `@notify`

    # Implemented in ObservableMixin:
    #
    # * def add_observer(self, observer): ...
    # * def notify(self): ...


class MyTextField(FrameworkTextField, Observer[MyModel]):
    def __init__(self, model):
        FrameworkTextField.__init__(self)

        model.add_observer(self)
        self.content_changed_callbacks.append(model.set_text)

    def act(self, observable: MyModel):
        """
        act() is munin's "update"-function.
        When an Observable notify:s, the Observable passes itself through this function to
        all its Observers.
        """
        self.set_content(observable.content)

model = MyTextModel()
MyTextField(model)

```

The keen reader sees that a call to `MyTextField.set_content(...)` will start an infinite loop.
This can be combatted with *"Discretion"*, **litteraly**.
*"Discretion"* is the `munin`-way to temporarily turn off the observer synchronization.

```python
from munin import discretion, discrete, ...

class MyTextField(FrameworkTextField, Observer[MyModel]):
    ...

    @discrete  # "Discretion" with a decorator
    def act(self, observable: MyModel):
        # "Discretion" with a context manager
        with discretion:
            self.set_content(observable.content)
```

Some GUI frameworks (PySide for example) experience metaclass conflicts when doing
multiple inheritance like in this example. Luckily, `Observer` is a `Protocol`, which means that
the inheritance can be omitted without any repercussions.

```python
class MyTextField(FrameworkTextField):
    def act(self, observable: MyModel):
        """Still satisfies the Observer Protocol"""
        pass
```
