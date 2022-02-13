from typing import Tuple

import pytest

from munin import ObservableMixin, Observer, discrete, discretion, notify


class SimpleObservable(ObservableMixin):
    def __init__(self) -> None:
        super().__init__()
        self.value: int = 10

    def set_value(self, new_value: int) -> None:
        self.value = new_value
        self.notify()

    @notify
    def set_value_decorated(self, new_value: int) -> None:
        self.value = new_value


class SimpleObserver(Observer[SimpleObservable]):
    def __init__(self) -> None:
        self.notified = False

    def act(self, _: SimpleObservable) -> None:
        self.notified = True


class ObserverWithDecoratedAct(Observer[ObservableMixin]):
    def __init__(self) -> None:
        self.number_of_notifies = 0

    @discrete
    def act(self, observable: SimpleObservable) -> None:
        self.number_of_notifies += 1
        observable.notify()  # This should be NOP since we are in a discretion context.


SimpleObsPair = Tuple[SimpleObserver, SimpleObservable]


@pytest.fixture
def simple_obs_pair() -> SimpleObsPair:
    observer = SimpleObserver()
    observable = SimpleObservable()
    observable.add_observer(observer)

    return observer, observable


# ===== Test cases ===== #


def test_value_change(simple_obs_pair: SimpleObsPair) -> None:
    observer, observable = simple_obs_pair
    observable.set_value(11)
    assert observer.notified


def test_value_change_with_decorator(simple_obs_pair: SimpleObsPair) -> None:
    observer, observable = simple_obs_pair
    observable.set_value_decorated(11)
    assert observer.notified


def test_adding_observer_twice_raises_error(
    simple_obs_pair: SimpleObsPair,
) -> None:
    observer, observable = simple_obs_pair
    with pytest.raises(ValueError):
        observable.add_observer(observer)


def test_discretion_turns_off_notify(simple_obs_pair: SimpleObsPair) -> None:
    observer, observable = simple_obs_pair
    with discretion:
        observable.set_value(11)

    assert not observer.notified


def test_discrete_decorator() -> None:
    observer = ObserverWithDecoratedAct()
    observable = ObservableMixin()
    observable.add_observer(observer)

    observable.notify()

    assert observer.number_of_notifies == 1


def test_using_munin_notify_decorator_on_non_subclasses_should_raise_type_error() -> None:
    class NotMuninSubclass:
        @notify
        def foo(self) -> None:
            ...

    with pytest.raises(TypeError):
        NotMuninSubclass().foo()
