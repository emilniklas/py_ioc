import py_ioc


def test_creates_an_instance():
    container = py_ioc.Container()
    assert isinstance(container.make(SimpleClass), SimpleClass)


def test_creates_dependencies():
    container = py_ioc.Container()
    with_dep = container.make(ClassWithDependency)
    assert isinstance(with_dep, ClassWithDependency)
    assert isinstance(with_dep.simple, SimpleClass)


def test_binds_abstractions():
    container = py_ioc.Container()
    container.bind('Abstract').to_class(SimpleClass)
    with_dep = container.make(ClassWithAbstractDependency)
    assert isinstance(with_dep, ClassWithAbstractDependency)
    assert isinstance(with_dep.abstract, SimpleClass)


def test_binds_singletons():
    container = py_ioc.Container()
    container.bind('Abstract', singleton=True) \
        .to_factory(lambda c: SimpleClass())
    a = container.make('Abstract')
    b = container.make('Abstract')
    assert a == b


def test_resolves_functions():
    container = py_ioc.Container()

    def fun(arg: SimpleClass):
        return arg

    assert isinstance(container.resolve(fun), SimpleClass)


def test_can_be_forked():
    base = py_ioc.Container()
    fork = base.fork()

    assert isinstance(fork.make(SimpleClass), SimpleClass)


def test_forked_containers_delegate_to_its_parent():
    base = py_ioc.Container()
    fork = base.fork()

    base.bind('token').to_instance(1)

    assert fork.make('token') == 1


def test_base_containers_do_not_delegate_to_its_children():
    base = py_ioc.Container()
    fork = base.fork()

    base.bind('token').to_instance(1)
    fork.bind('token').to_instance(2)

    assert base.make('token') == 1
    assert fork.make('token') == 2


def test_forks_can_be_nested():
    base = py_ioc.Container()
    middle = base.fork()
    child = middle.fork()

    base.bind('token').to_instance(1)
    middle.bind('other').to_instance(2)
    child.bind('token').to_instance(3)

    assert base.make('token') == 1
    assert middle.make('token') == 1
    assert middle.make('other') == 2
    assert child.make('token') == 3
    assert child.make('other') == 2


def test_kwargs_are_forwarded():
    container = py_ioc.Container()

    def fun_with_kwarg(kwarg=None):
        return kwarg

    assert container.make(ClassWithKwarg, kwarg=123).kwarg == 123
    assert container.resolve(fun_with_kwarg, kwarg=123) == 123


def test_classes_can_be_curried():
    container = py_ioc.Container()
    curried = container.curry(ClassWithDependency)

    assert isinstance(curried().simple, SimpleClass)


def test_functions_can_be_curried():
    container = py_ioc.Container()

    def fun(dep: SimpleClass):
        return dep

    curried = container.curry(fun)

    assert isinstance(curried(), SimpleClass)


def test_curried_functions_can_take_arguments_which_take_precedence():
    container = py_ioc.Container()

    def fun(arg: str, dep: SimpleClass):
        assert isinstance(dep, SimpleClass)
        return arg

    curried = container.curry(fun)

    assert curried('hello') == 'hello'


class SimpleClass:
    pass


class ClassWithDependency:
    def __init__(self, simple: SimpleClass):
        self.simple = simple


class ClassWithAbstractDependency:
    def __init__(self, abstract: 'Abstract'):
        self.abstract = abstract


class ClassWithKwarg:
    def __init__(self, kwarg=None):
        self.kwarg = kwarg
