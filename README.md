# lambda_integrate

Using Chalice with RDS, SQS, SNS

## Installing

Clone the repository:

```sh
$ git clone https://github.com/codnstj/lambda_integrate.git
```

Set up a virtual environment for the project and activate it.
> Even though we recommend python3 [venv](https://docs.python.org/3/library/venv.html)
> module feel free to use you prefer.

```sh
$ cd lambda_integrate
$ python3 -m venv venv
$ source venv/bin/activate
```

Using `virtualenv`

```sh
$ cd lambda_integrate
$ virtualenv [--python=python3.6] venv
$ source venv/bin/activate
```

Using `virtualwrapper`:

```sh
$ mkvirtualenv lambda_integrate
```

The app provides a `make` command as an interface to the most common tasks.

> Run `make help` to see the available commands!

To initialize the environment simply execute:

```sh
$ make install
```

🍪 You're ready ! try it with:


```sh
$ make run
```

## Running Tests

To run all tests, simply run:

```sh
$ make test
```
