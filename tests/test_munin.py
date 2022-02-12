from typing import Tuple

import pytest

import munin


class BasicObserver(munin.Observer):
    def __init__(self):
        self.notified = False

    def act(self, observable: munin.ObservableMixin):
        self.notified = True


class BasicObservable(munin.ObservableMixin):
    def __init__(self):
        super().__init__()
        self.value = 10

    def set_value(self, new_value) -> None:
        self.value = new_value
        self.notify()

    @munin.notify
    def set_value_decorated(self, new_value) -> None:
        self.value = new_value


@pytest.fixture
def simple_obs_pair() -> Tuple[munin.Observer, munin.ObservableMixin]:
    observer = BasicObserver()
    observable = BasicObservable()
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


def test_observer_isnt_instantiable():
    with pytest.raises(TypeError):
        munin.Observer()
