from __future__ import annotations

from abc import abstractmethod
from typing import Callable, List, Protocol, TypeVar

T = TypeVar("T")

_notifications_enabled = True


class _NotifyManager:
    """
    Cheeky context manager that lets you teporarily turn of
    observer syncronization.
    """
    def __enter__(self):
        global _notifications_enabled
        _notifications_enabled = False

    def __exit__(self, *_):
        global _notifications_enabled
        _notifications_enabled = True


discretion = _NotifyManager()

class Observer(Protocol):
    """
    Observer

    Defines a single function: `update(observable)` that an
    `ObservableMixin` calls once notified.
    """
    @abstractmethod
    def update(self, observable: ObservableMixin) -> None:
        ...


class ObservableMixin:
    """
    ObservableMixin

    Defines the `self.observers` list, `add_observer` to append to that
    and the `notify` method, which is used to notify "registered" observers
    """
    def __init__(self):
        self.observers: List[Observer] = []

    def add_observer(self, observer: Observer) -> None:
        if observer in self.observers:
            raise ValueError(f"{observer} is already in the observer list.")
        self.observers.append(observer)

    def notify(self) -> None:
        if not _notifications_enabled:
            return

        for observer in self.observers:
            observer.update(self)

# FIXME: type should be ~~~ Callable[[ObservableMixin, ...], T]
MethodOfObservable = Callable[..., T]

def notify(function: MethodOfObservable[T]) -> MethodOfObservable[T]:
    """
    A simple decorator that calls notify after `function` returns.
    """
    def notify_wrapper(instance: ObservableMixin, *args, **kwargs) -> T:
        result: T = function(instance, *args, **kwargs)
        instance.notify()
        return result

    return notify_wrapper
