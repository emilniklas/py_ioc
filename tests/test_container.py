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


class SimpleClass:
    pass


class ClassWithDependency:
    def __init__(self, simple: SimpleClass):
        self.simple = simple


class ClassWithAbstractDependency:
    def __init__(self, abstract: 'Abstract'):
        self.abstract = abstract
