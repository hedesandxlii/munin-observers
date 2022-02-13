from __future__ import annotations

from abc import abstractmethod
from typing import Callable, List, Protocol, TypeVar

T = TypeVar("T")
T_contra = TypeVar("T_contra", contravariant=True)

_notifications_enabled = True


class _NotifyManager:
    """
    Cheeky context manager that lets you teporarily turn off
    observer syncronization.
    """

    def __enter__(self):
        global _notifications_enabled
        _notifications_enabled = False

    def __exit__(self, *_):
        global _notifications_enabled
        _notifications_enabled = True


discretion = _NotifyManager()


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
            observer.act(self)


class Observer(Protocol[T_contra]):
    """
    Observer

    Defines a single function: `act(observable)` that an
    `ObservableMixin` calls once notified.
    """

    @abstractmethod
    def act(self, observable: T_contra) -> None:
        ...


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


def discrete(function: MethodOfObservable[T]) -> MethodOfObservable[T]:
    """
    A simple decorator that calls `function` is the `discretion` context.
    """

    def discretion_wrapper(instance: ObservableMixin, *args, **kwargs) -> T:
        with discretion:
            result: T = function(instance, *args, **kwargs)
        return result

    return discretion_wrapper
