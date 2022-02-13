from typing import Tuple

import pytest

import munin


class SimpleObservable(munin.ObservableMixin):
    def __init__(self):
        super().__init__()
        self.value = 10

    def set_value(self, new_value) -> None:
        self.value = new_value
        self.notify()

    @munin.notify
    def set_value_decorated(self, new_value) -> None:
        self.value = new_value


class SimpleObserver(munin.Observer[SimpleObservable]):
    def __init__(self):
        self.notified = False

    def act(self, _: SimpleObservable):
        self.notified = True


class ObserverWithDecoratedAct(munin.Observer[munin.ObservableMixin]):
    def __init__(self):
        self.number_of_notifies = 0

    @munin.discrete
    def act(self, observable: SimpleObservable):
        self.number_of_notifies += 1
        observable.notify()  # This should be NOP since we are in a discretion context.


@pytest.fixture
def simple_obs_pair() -> Tuple[munin.Observer, munin.ObservableMixin]:
    observer = SimpleObserver()
    observable = SimpleObservable()
    observable.add_observer(observer)

    return observer, observable


# ===== Test cases ===== #


def test_value_change(simple_obs_pair):
    observer, observable = simple_obs_pair
    observable.set_value(11)
    assert observer.notified


def test_value_change_with_decorator(simple_obs_pair):
    observer, observable = simple_obs_pair
    observable.set_value_decorated(11)
    assert observer.notified


def test_adding_observer_twice_raises_error(simple_obs_pair):
    observer, observable = simple_obs_pair
    with pytest.raises(ValueError):
        observable.add_observer(observer)


def test_discretion_turns_off_notify(simple_obs_pair):
    observer, observable = simple_obs_pair
    with munin.discretion:
        observable.set_value(11)

    assert not observer.notified


def test_instantiability():
    # Observer should not be instantiable
    with pytest.raises(TypeError):
        munin.Observer()

    # Observable should be instantiable
    munin.ObservableMixin()


def test_discrete_decorator():
    observer = ObserverWithDecoratedAct()
    observable = munin.ObservableMixin()
    observable.add_observer(observer)

    observable.notify()

    assert observer.number_of_notifies == 1
