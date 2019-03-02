# accessify

Python class members accessibility levels.

[![Release](https://img.shields.io/github/release/dmytrostriletskyi/accessify.svg)](https://github.com/dmytrostriletskyi/pdbe/releases)
[![Build Status](https://travis-ci.com/dmytrostriletskyi/accessify.svg?branch=develop)](https://travis-ci.com/dmytrostriletskyi/accessify)
[![codecov](https://codecov.io/gh/dmytrostriletskyi/design-kit/branch/develop/graph/badge.svg)](https://codecov.io/gh/dmytrostriletskyi/design-kit)

![Python3](https://img.shields.io/badge/Python-3.3-brightgreen.svg)
![Python3](https://img.shields.io/badge/Python-3.4-brightgreen.svg)
![Python3](https://img.shields.io/badge/Python-3.5-brightgreen.svg)
![Python3](https://img.shields.io/badge/Python-3.6-brightgreen.svg)
![Python3](https://img.shields.io/badge/Python-3.7-brightgreen.svg)

  * [Getting started](#getting-started)
    * [What is accessify](#what-is-accessify)
    * [Motivation](#motivation)
    * [How to install](#how-to-install)
  * [Usage](#usage)
    * [Private](#private)
    * [Protected](#protected)
    * [Other features](#other-features)
  * [Contributing](#contributing)
  * [References](#references)

## Getting started

### What is accessify

Access level modifiers determine whether other classes can use a particular field or invoke a particular method.
Accessibility levels are presented from the box in the languages like `C++`, `C#` and `Java`. 

```csharp
class Car 
{
    private string StartEngine()
    {
        // Code here.
    }
}
```

But `Python` does not have this in the same way. `accessify` provides the functionality for `Python projects` that a 
bit close to the real accessibility levels.

### Motivation

* `We're all consenting adults here` that is the  part of the `Python philosophy` that relies on human factor instead of the interpreter.
* There is a `Python convention` that is to use an underscore prefix for protected and private members, that is a bit ugly. 
Isn't it? For instance, for the following piece of code that provides class private member.

```python
class Car:

    def __start_engine(self, *args, **kwargs):
        pass
```

* Moreover, private and protected methods could be easily accessed outside the class. This is really a point to postpone the 
correct design of the system to the backlog, increasing the technical debt, sacrificed to fast feature delivering.

 ```python
class Car:

    def _start_engine(self, *args, **kwargs):
        pass
        
    def __start_engine(self, *args, **kwargs):
        pass


car = Car()
car._start_engine()
car._Car__start_engine()
```

### How to install

Using [pip](https://pypi.org/project/pip) install the package from the [PyPi](https://pypi.org/project/accessify).

```bash
$ pip3 install accessify
```

## Usage

### Private

* Private members are accessible only within the body of the class.

In this example, the `Car` class contains a private member named `start_engine`. As a private member, they cannot be accessed
except by member methods. The private member `start_engine` is accessed only by way of a public method called `run`. 

```python
from accessify import private


class Car:

    @private
    def start_engine(self):
        return 'Engine sound.'

    def run(self):
        return self.start_engine()


if __name__ == '__main__':
    car = Car()

    assert 'Engine sound.' == car.run()

    car.start_engine()
```

The code above will produce the following traceback.

```bash
Traceback (most recent call last):
  File "examples/access/private.py", line 24, in <module>
    car.start_engine()
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/accessify/main.py", line 92, in private_wrapper
    class_name=instance_class.__name__, method_name=method.__name__,
accessify.errors.InaccessibleDueToItsProtectionLevelException: Car.start_engine() is inaccessible due to its protection level
```

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/basic-accessibility-levels/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhASP > private.py
$ python3 private.py
```

* Child classes cannot access parent private members.

In this example, the `Car` class contains a private member named `start_engine`. As a private member, they cannot be accessed
from the child classes, `Tesla` in our case. So overridden method `run` by `Tesla` class cannot use the parent's `start_engine` member.

```python
from accessify import private


class Car:

    @private
    def start_engine(self):
        return 'Engine sound.'


class Tesla(Car):

    def run(self):
        return self.start_engine()


if __name__ == '__main__':
    tesla = Tesla()
    tesla.run()
```

The code above will produce the following traceback.

```bash
Traceback (most recent call last):
  File "examples/inheritance/private.py", line 23, in <module>
    tesla.run()
  File "examples/inheritance/private.py", line 18, in run
    return self.start_engine()
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/accessify/main.py", line 94, in private_wrapper
    class_name=class_contain.__name__, method_name=method.__name__,
accessify.errors.InaccessibleDueToItsProtectionLevelException: Car.start_engine() is inaccessible due to its protection level
```

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/basic-accessibility-levels/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhASX > inheritence_private.py
$ python3 inheritence_private.py
```

### Protected

* A protected member is accessible within its class and by derived class instances.

In this example, the `Car` class contains a protected member named `start_engine`. As a protected member, they cannot be accessed
except by member methods. The protected member `start_engine` is accessed only by way of a public method called `run`. 

```python
from accessify import protected


class Car:

    @protected
    def start_engine(self):
        return 'Engine sound.'

    def run(self):
        return self.start_engine()


if __name__ == '__main__':
    car = Car()

    assert 'Engine sound.' == car.run()

    car.start_engine()
```

The code above will produce the following traceback.

```bash
Traceback (most recent call last):
  File "examples/access/protected.py", line 21, in <module>
    car.start_engine()
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/accessify/main.py", line 134, in protected_wrapper
    class_name=instance_class.__name__, method_name=method.__name__,
accessify.errors.InaccessibleDueToItsProtectionLevelException: Car.start_engine() is inaccessible due to its protection level
```

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/basic-accessibility-levels/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhASM > protected.py
$ python3 protected.py
```

* Child classes have access to those protected members.

In this example, the `Car` class contains protected member named `start_engine`. As protected member, they can be accessed
from the child classes, `Tesla` in our case. So overridden method `run` by `Tesla` class can use the parent's `start_engine` member.


```python
from accessify import protected


class Car:

    @protected
    def start_engine(self):
        return 'Engine sound.'


class Tesla(Car):

    def run(self):
        return self.start_engine()


if __name__ == '__main__':
    tesla = Tesla()

    assert 'Engine sound.' == tesla.run()
```

The code will work without errors.

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/basic-accessibility-levels/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhASD > inheritence_protected.py
$ python3 inheritence_protected.py
```

### Other features

* The `accessify` decorator removes private and protected members from class [dir](https://docs.python.org/3/library/functions.html#dir).

```python
from accessify import accessify, private


@accessify
class Car:

    @private
    def start_engine(self):
        return 'Engine sound.'

if __name__ == '__main__':
    car = Car()

    assert 'start_engine' not in dir(car)
```

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/basic-accessibility-levels/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhASy > dir.py
$ python3 dir.py
```

## Contributing

Clone the project and install requirements.

```bash
$ git clone git@github.com:dmytrostriletskyi/accessify.git && cd accessify
$ pip3 install -r requirements-dev.txt
$ pip3 install -r requirements-tests.txt
```

When you will make changes, ensure your code pass [the checkers](https://github.com/dmytrostriletskyi/accessify/blob/basic-accessibility-levels/.travis.yml#L15) 
and is covered by tests using [pytest](https://docs.pytest.org/en/latest).

If you are new for the contribution, please read:

* Read about pull requests — https://help.github.com/en/articles/about-pull-requests
* Read how to provide pull request — https://help.github.com/en/articles/creating-a-pull-request-from-a-fork
* Also the useful article about how to contribute — https://akrabat.com/the-beginners-guide-to-contributing-to-a-github-project/

## References

Check it out to familiarize yourself with class members accessibility levels:

* C# accessibility levels — https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/accessibility-levels
* Java accessibility levels — https://docs.oracle.com/javase/tutorial/java/javaOO/accesscontrol.html
