# py_ioc

IoC Container for Python that uses [PEP3107](https://www.python.org/dev/peps/pep-3107/)
function annotations to automatically inject dependencies:

```python
import py_ioc


class SomeClass:
    pass


class SomeOtherClass:
    def __init__(self, some_class: SomeClass):
        self.some_class = some_class


container = py_ioc.Container()
some_other_class = container.make(SomeOtherClass)

assert isinstance(some_other_class.some_class, SomeClass)
```

Conceptually, a class might have a dependency on a contract rather than a concrete class.
Since we don't have interfaces to formalize this relationship in Python, we can use
strings instead.

```python
# Instead of an interface, we create a constant which will
# act like a token for the contract. We can also inline the
# string if this feels superflous.
Database = 'Database'


class PostgresDatabase:
    pass


class SomeRepository:
    def __init__(self, database: Database):
      self.database = database


container.bind(Database).to_class(PostgresDatabase)

repo = container.make(SomeRepository)

assert isinstance(repo.database, PostgresDatabase)

# We can also make contracts directly
database = container.make(Database)

assert isinstance(database, PostgresDatabase)
```
