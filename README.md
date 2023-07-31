# accessify

[![Release](https://img.shields.io/github/release/dmytrostriletskyi/accessify.svg)](https://github.com/dmytrostriletskyi/accessify/releases)
[![PyPI version shields.io](https://img.shields.io/pypi/v/accessify.svg)](https://pypi.python.org/pypi/accessify/)
[![Build Status](https://travis-ci.com/dmytrostriletskyi/accessify.svg?branch=develop)](https://travis-ci.com/dmytrostriletskyi/accessify)
[![codecov](https://codecov.io/gh/dmytrostriletskyi/design-kit/branch/develop/graph/badge.svg)](https://codecov.io/gh/dmytrostriletskyi/design-kit)

[![Downloads](https://pepy.tech/badge/accessify)](https://pepy.tech/project/accessify)
[![PyPI license](https://img.shields.io/pypi/l/accessify.svg)](https://pypi.python.org/pypi/accessify/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/accessify.svg)](https://pypi.python.org/pypi/accessify/)

[![Habrahabr](https://img.shields.io/badge/Post-Habrahabr-brightgreen.svg)](https://habr.com/ru/post/443192/)

  * [Getting started](#getting-started)
    * [What is accessify](#what-is-accessify)
    * [Access modifiers](#getting-started-access-modifiers)
      * [Motivation](#getting-started-access-modifiers-motivation)
    * [Interfaces](#getting-started-interfaces)
      * [Motivation](#getting-started-interfaces-motivation)
    * [How to install](#how-to-install)
  * [Usage](#usage)
    * [Access modifiers](#usage-access-modifiers)
      * [Private](#private)
      * [Protected](#protected)
      * [Other features](#other-features)
    * [Interfaces](#usage-interfaces)
      * [Single interface](#single-interface)
      * [Multiple interfaces](#multiple-interfaces)
      * [Exception throws declaration](#exception-throws-declaration)
  * [Disable checking](#disable-checking)
  * [Contributing](#contributing)
  * [References](#references)

## Getting started

### What is accessify

`accessify` is a `Python` design kit that provides:
* interfaces,
* declared exceptions throws,
* class members accessibility levels.

that could be combined with each other to make your code slim and this library usage more justified.

<h3 id="getting-started-access-modifiers">Access modifiers</h3>

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

But `Python` does not have this in the same way.

<h4 id="getting-started-access-modifiers-motivation">Motivation</h4>

* `We're all consenting adults here` that is the  part of the `Python philosophy` that relies on human factor instead of the interpreter.
* There is a `Python convention` that is to use an underscore prefix for protected and private members, that is a bit ugly.
Isn't it? For instance, for the following piece of code that provides class a private member.

```python
class Car:

    def __start_engine(self, *args, **kwargs):
        pass
```

* Moreover, private and protected methods could be easily accessed outside the class. This is really a point to postpone the
correct design of the system to the backlog, increasing the technical debt.

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

<h3 id="getting-started-interfaces">Interfaces</h3>

An interface is a contract specifying a set of methods and properties which required to be available on any implementing class.
If the class implements an interface, but does not realize its method, corresponding errors should be raised. Interfaces are presented from the box in
the languages like `C++`, `C#` and `Java`.

```csharp
interface HumanInterface
{
    public string EatFood();
}

class Human : HumanInterface
{
    public string EatFood()
    {
        // Code here.
    }
}
```

But `Python` does not have this in the same way.

<h4 id="getting-started-interfaces-motivation">Motivation</h4>

* The interface makes checks during the implementation creation, but not actually while execution like [abc](https://docs.python.org/3/library/abc.html) module in `Python`.
* The interface requires that implementation's method arguments match with arguments declared in interfaces, [abc](https://docs.python.org/3/library/abc.html) — not.
* A lot of libraries that provide interfaces are no longer supported.
* A lot of libraries that provide interfaces require you to write a lot of code to use its functionality, this library — not.

### How to install

Using [pip](https://pypi.org/project/pip) install the package from the [PyPi](https://pypi.org/project/accessify).

```bash
$ pip3 install accessify
```

## Usage

<h3 id="usage-access-modifiers">Access modifiers</h3>

#### Private

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

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/master/examples).
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

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/master/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhASX > inheritence_private.py
$ python3 inheritence_private.py
```

#### Protected

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

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/master/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhASM > protected.py
$ python3 protected.py
```

* Child classes have access to those protected members.

In this example, the `Car` class contains a protected member named `start_engine`. As a protected member, they can be accessed
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

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/master/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhASD > inheritence_protected.py
$ python3 inheritence_protected.py
```

#### Other features

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

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/master/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhASy > dir.py
$ python3 dir.py
```

<h3 id="usage-interfaces">Interfaces</h3>

#### Single interface

* When you declare that class implements an interface, a class should implement **all methods** presented in the interface.

In this example, there is an interface called `HumanInterface` that contains two methods `love` and `eat`. Also, there is
a class `Human` that implements the interface but **missed method «eat»**, so the corresponding error should be raised.

```python
from accessify import implements


class HumanInterface:

    @staticmethod
    def eat(food, *args, allergy=None, **kwargs):
        pass


if __name__ == '__main__':

    @implements(HumanInterface)
    class Human:

        pass
```

The code above will produce the following traceback.

```bash
Traceback (most recent call last):
  File "examples/interfaces/single.py", line 18, in <module>
    @implements(HumanInterface)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/accessify/interfaces.py", line 66, in decorator
    interface_method_arguments=interface_method.arguments_as_string,
accessify.errors.InterfaceMemberHasNotBeenImplementedException: class Human does not implement interface member HumanInterface.eat(food, args, allergy, kwargs)
```

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/master/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhh2V > single_method.py
$ python3 single_method.py
```

* When you declare that class implements an interface, a class should implement all methods that presented in the interface
including **number, order and naming of the accepting arguments**.

In this example, there is an interface called `HumanInterface` that contains two methods `love` and `eat`. Also, there is
a class `Human` that implements the interface but **missed 3 of 4 arguments for method «eat»**, so the corresponding error should be raised.

```python
from accessify import implements


class HumanInterface:

    @staticmethod
    def eat(food, *args, allergy=None, **kwargs):
        pass


if __name__ == '__main__':

    @implements(HumanInterface)
    class Human:

        @staticmethod
        def eat(food):
            pass
```

The code above will produce the following traceback.

```bash
Traceback (most recent call last):
  File "examples/interfaces/single_arguments.py", line 16, in <module>
    @implements(HumanInterface)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/accessify/interfaces.py", line 87, in decorator
    interface_method_arguments=interface_method.arguments_as_string,
accessify.errors.InterfaceMemberHasNotBeenImplementedWithMismatchedArgumentsException: class Human implements interface member HumanInterface.eat(food, args, allergy, kwargs) with mismatched arguments
```

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/master/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhh2w > single_arguments.py
$ python3 single_arguments.py
```

* When you declare that class implements an interface, a class should implement all methods that presented in the interface
including number, order and naming of the accepting arguments and **access modifier type**.

In this example, there is an interface called `HumanInterface` that contains two methods `love` and `eat`. Also, there is
a class `Human` that implements the interface but **missed private access modifier type for method «eat»**, so the corresponding
error should be raised.

```python
from accessify import implements, private


class HumanInterface:

    @private
    @staticmethod
    def eat(food, *args, allergy=None, **kwargs):
        pass


if __name__ == '__main__':

    @implements(HumanInterface)
    class Human:

        @staticmethod
        def eat(food, *args, allergy=None, **kwargs):
            pass
```

The code above will produce the following traceback.

```bash
Traceback (most recent call last):
  File "examples/interfaces/single_access.py", line 18, in <module>
    @implements(HumanInterface)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/accessify/interfaces.py", line 77, in decorator
    interface_method_name=interface_method.name,
accessify.errors.ImplementedInterfaceMemberHasIncorrectAccessModifierException: Human.eat(food, args, allergy, kwargs) mismatches HumanInterface.eat() member access modifier.
```

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/master/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhh2r > single_access.py
$ python3 single_access.py
```

#### Multiple interfaces

* A class could implement multiple interfaces.
* When you declare that class that implements a bunch of interfaces, a class should implement all method that presented in
each interface including number, order and naming of the accepting arguments and access modifier type.

In this example, there are an interface `HumanSoulInterface` that contains a method called `love` and interface `HumanBasicsInterface` that
contains a method called `eat`. Also, there is a class `Human` that implements method `love` from the first interface, but
**missed method «eat»** from the second one, so the corresponding error should be raised.

```python
from accessify import implements


class HumanSoulInterface:

    def love(self, who, *args, **kwargs):
        pass


class HumanBasicsInterface:

    @staticmethod
    def eat(food, *args, allergy=None, **kwargs):
        pass


if __name__ == '__main__':

    @implements(HumanSoulInterface, HumanBasicsInterface)
    class Human:

        def love(self, who, *args, **kwargs):
            pass
```

The code above will produce the following traceback.

```bash
Traceback (most recent call last):
  File "examples/interfaces/multiple.py", line 19, in <module>
    @implements(HumanSoulInterface, HumanBasicsInterface)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/accessify/interfaces.py", line 66, in decorator
    interface_method_arguments=interface_method.arguments_as_string,
accessify.errors.InterfaceMemberHasNotBeenImplementedException: class Human does not implement interface member HumanBasicsInterface.eat(food, args, allergy, kwargs)
```

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/master/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhh2o > multiple.py
$ python3 multiple.py
```

#### Exception throws declaration

* When you declare that interface method throws a particular exception, a class method that implement interface should
contain code in the body that raise this exception.
* You can declare that the interface method throws multiple exceptions.

In this example, exception `HumanDoesNotExistsError` and exception `HumanAlreadyInLoveError` are declared to be raised by
the `Human` class method called `love` , but method **missed to raise the second exception**, so the corresponding error should be raised.

```python
from accessify import implements, throws


class HumanDoesNotExistsError(Exception):
    pass


class HumanAlreadyInLoveError(Exception):
    pass


class HumanInterface:

    @throws(HumanDoesNotExistsError, HumanAlreadyInLoveError)
    def love(self, who, *args, **kwargs):
        pass


if __name__ == '__main__':

    @implements(HumanInterface)
    class Human:

        def love(self, who, *args, **kwargs):

            if who is None:
                raise HumanDoesNotExistsError('Human whom need to love does not exist.')
```

The code above will produce the following traceback.

```bash
Traceback (most recent call last):
  File "examples/interfaces/throws.py", line 21, in <module>
    @implements(HumanInterface)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/accessify/interfaces.py", line 103, in decorator
    class_method_arguments=class_member.arguments_as_string,
accessify.errors.DeclaredInterfaceExceptionHasNotBeenImplementedException: Declared exception HumanAlreadyInLoveError by HumanInterface.love() member has not been implemented by Human.love(self, who, args, kwargs)
```

Test it out using the [examples](https://github.com/dmytrostriletskyi/accessify/tree/master/examples).
Get the example that contains the code above by `curl` and run it by `python3`.

```bash
$ curl -L https://git.io/fhh26 > throws.py
$ python3 throws.py
```

## Disable checking

You can disable all `accessify` checks. For instance, in the production, when you shouldn't check it because it already was checked
in the development. Use the following environment variable then:

```bash
export DISABLE_ACCESSIFY=True
```

## Contributing

Clone the project and install requirements:

```bash
$ git clone git@github.com:dmytrostriletskyi/accessify.git && cd accessify
$ pip3 install -r requirements-dev.txt
$ pip3 install -r requirements-tests.txt
```

If you prefer working with the [Docker](https://www.docker.com) and wanna easily change `Python` environments, follow:

```bash
$ git clone git@github.com:dmytrostriletskyi/accessify.git && cd accessify
$ export ACCESSIFY_PYTHON_VERSION=3.4
$ docker build --build-arg ACCESSIFY_PYTHON_VERSION=$ACCESSIFY_PYTHON_VERSION -t accessify . -f Dockerfile-python3.x
$ docker run -v $PWD:/accessify --name accessify accessify
```

Enter the container bash, check `Python` version and run tests:

```bash
$ docker exec -it accessify bash
$ root@36a8978cf100:/accessify# python --version
$ root@36a8978cf100:/accessify# pytest -vv tests
```

Clean container and images with the following command:

```bash
$ docker rm $(docker ps -a -q) -f
$ docker rmi $(docker images -q) -f
```

When you will make changes, ensure your code pass [the checkers](https://github.com/dmytrostriletskyi/accessify/blob/master/.travis.yml)
and is covered by tests using [pytest](https://docs.pytest.org/en/latest).

If you are new for the contribution, please read:

* Read about pull requests — https://help.github.com/en/articles/about-pull-requests
* Read how to provide pull request — https://help.github.com/en/articles/creating-a-pull-request-from-a-fork
* Also the useful article about how to contribute — https://akrabat.com/the-beginners-guide-to-contributing-to-a-github-project/

## References

Check it out to familiarize yourself with class members accessibility levels:

* C# accessibility levels — https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/accessibility-levels
* Java accessibility levels — https://docs.oracle.com/javase/tutorial/java/javaOO/accesscontrol.html
* Object-oriented programming interfaces — https://www.cs.utah.edu/~germain/PPS/Topics/interfaces.html
* Interfaces in C# — https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/interface
* Interfaces in Java — https://docs.oracle.com/javase/tutorial/java/concepts/interface.html
