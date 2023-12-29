import pytest
from profiled import profiled, Profiler, get_func_id


@profiled
def get_answer():
    return 42


class AnswerFactory:
    @profiled
    def __call__(self):
        return 42

    @staticmethod
    @profiled
    def get_answer_static():
        return 42

    @classmethod
    @profiled
    def get_answer_class(cls):
        return 42


@pytest.fixture(
    scope="function", params=["function", "method", "staticmethod", "classmethod"]
)
def profiled_func(request):
    if request.param == "function":
        return get_answer
    elif request.param == "method":
        factory = AnswerFactory()
        return factory.__call__
    elif request.param == "staticmethod":
        factory = AnswerFactory()
        return factory.get_answer_static
    elif request.param == "classmethod":
        factory = AnswerFactory()
        return factory.get_answer_class


@pytest.fixture(scope="function")
def profiler():
    p = Profiler()
    yield p
    p.reset()


@pytest.mark.parametrize("profiled_func", ["function"], indirect=True)
def test_function_id(profiled_func):
    func_name = get_func_id(profiled_func)
    assert func_name == "get_answer"


@pytest.mark.parametrize("profiled_func", ["method"], indirect=True)
def test_method_id(profiled_func):
    func_name = get_func_id(profiled_func)
    assert func_name == "AnswerFactory.__call__"


@pytest.mark.parametrize("profiled_func", ["staticmethod"], indirect=True)
def test_staticmethod_id(profiled_func):
    func_name = get_func_id(profiled_func)
    assert func_name == "AnswerFactory.get_answer_static"


@pytest.mark.parametrize("profiled_func", ["classmethod"], indirect=True)
def test_classmethod_id(profiled_func):
    func_name = get_func_id(profiled_func)
    assert func_name == "AnswerFactory.get_answer_class"


def test_does_nothing_outside_of_context(profiler, profiled_func):
    for i in range(100):
        profiled_func()
    assert not profiler.compute_stats()


def test_compute_stats_more_than_two_runs(profiler, profiled_func):
    num_runs = 100000
    with profiler:
        for i in range(num_runs):
            profiled_func()

    stats = profiler.compute_stats()[get_func_id(profiled_func)]
    assert stats["min"] >= 0.0
    assert stats["max"] > 0.0
    assert stats["avg"] > 0.0
    assert stats["tot"] > 0.0
    assert stats["std"] > 0.0
    assert stats["num"] == num_runs


def test_compute_stats_less_than_two_runs(profiler, profiled_func):
    num_runs = 1
    with profiler:
        for i in range(num_runs):
            profiled_func()

    stats = profiler.compute_stats()[get_func_id(profiled_func)]
    assert stats["min"] >= 0.0
    assert stats["max"] > 0.0
    assert stats["avg"] > 0.0
    assert stats["tot"] > 0.0
    assert stats["num"] == num_runs
    assert "std" not in stats
