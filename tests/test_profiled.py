import pytest

from profiled import profiled, Profiler


@profiled
def get_answer():
    return 42


@pytest.fixture(scope='function')
def profiler():
    return Profiler()


def test_does_nothing_outside_of_context(profiler):
    for i in range(100): get_answer()
    assert not profiler.compute_stats()


def test_compute_stats_more_than_two_runs(profiler):
    num_runs = 100000
    with profiler.as_default():
        for i in range(num_runs): get_answer()

    stats = profiler.compute_stats()['get_answer']
    assert stats['min'] >= 0.
    assert stats['max'] > 0.
    assert stats['avg'] > 0.
    assert stats['tot'] > 0.
    assert stats['std'] > 0.
    assert stats['num'] == num_runs


def test_compute_stats_less_than_two_runs(profiler):
    num_runs = 1
    with profiler.as_default():
        for i in range(num_runs): get_answer()

    stats = profiler.compute_stats()['get_answer']
    assert stats['min'] >= 0.
    assert stats['max'] > 0.
    assert stats['avg'] > 0.
    assert stats['tot'] > 0.
    assert stats['num'] == num_runs
    assert 'std' not in stats
