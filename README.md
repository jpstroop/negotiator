# Negotiator

Proper Content Negotiation for Python

[![Build Status](https://travis-ci.org/jpstroop/negotiator.svg?branch=master)](https://travis-ci.org/jpstroop/negotiator)
[![Coverage Status](https://coveralls.io/repos/github/jpstroop/negotiator/badge.svg?branch=master)](https://coveralls.io/github/jpstroop/negotiator?branch=master)
[![Python 3.6](https://img.shields.io/badge/python-3.6-yellow.svg)](https://img.shields.io/badge/python-3.6-yellow.svg)
[![Python 3.7](https://img.shields.io/badge/python-3.7-yellow.svg)](https://img.shields.io/badge/python-3.7-yellow.svg)
[![Python 3.8](https://img.shields.io/badge/python-3.8-yellow.svg)](https://img.shields.io/badge/python-3.8-yellow.svg)
[![Python Nightly](https://img.shields.io/badge/python-nightly-yellow.svg)](https://img.shields.io/badge/python-nightly-yellow.svg)


## Introduction

Negotiator offers a framework for making content negotiation decisions based on the HTTP accept headers.

NOTE it currently only formally supports `Accept` and `Accept-Language`, but it is a short haul to support for `Accept-Charset` and `Accept-Encoding` (TODO)

## Basic Usage

Import all the objects from the negotiator module

```python
from negotiator import ContentNegotiator, AcceptParameters, ContentType, Language
```

Specify the default parameters.  These are the parameters which will be used in place of any HTTP `Accept` headers which are not present in the negotiation request.  For example, if the `Accept-Language` header is not passed to the negotiator it will assume that the client request is for "en"

```python
default_params = AcceptParameters(ContentType("text/html"), Language("en"))
```

Specify the list of acceptable formats that the server supports

```python
acceptable = [AcceptParameters(ContentType("text/html"), Language("en"))]
acceptable.append(AcceptParameters(ContentType("text/json"), Language("en")))
```

Create an instance of the negotiator, ready to accept negotiation requests

```python
cn = ContentNegotiator(default_params, acceptable)
```

A simple negotiate on the HTTP `Accept` header `"text/json;q=1.0, text/html;q=0.9"`, asking for json, and if not json then html

```python
acceptable = cn.negotiate(accept="text/json;q=1.0, text/html;q=0.9")
```

The negotiator indicates that the best match the server can give to the client's request is `text/json` in english

```python
>> acceptable
AcceptParameters:: Content Type: text/json;Language: en;
```

## Advanced Usage

Import all the objects from the negotiator module

```python
from negotiator import ContentNegotiator, AcceptParameters, ContentType, Language
```

Specify the default parameters.  These are the parameters which will be used in place of any HTTP `Accept` headers which are not present in the negotiation request. For example, if the `Accept-Language` header is not passed to the negotiator it will assume that the client request is for "en"

```python
default_params = AcceptParameters(ContentType("text/html"), Language("en"))
```

Specify the list of acceptable formats that the server supports.  For this advanced example we specify html, json and pdf in a variety of languages

```python
acceptable = [AcceptParameters(ContentType("text/html"), Language("en"))]
acceptable.append(AcceptParameters(ContentType("text/html"), Language("fr")))
acceptable.append(AcceptParameters(ContentType("text/html"), Language("de")))
acceptable.append(AcceptParameters(ContentType("text/json"), Language("en")))
acceptable.append(AcceptParameters(ContentType("text/json"), Language("cz")))
acceptable.append(AcceptParameters(ContentType("application/pdf"), Language("de")))
```

Specify the weighting that the negotiator should apply to the different `Accept` headers. A higher weighting towards content type will prefer content type variations over language variations (e.g. if there are two formats which are equally acceptable to the client, in different languages, a content_type weight higher than a language weight will return the parameters according to the server's preferred content type.

```python
weights = {"content_type" : 1.0, "language" : 0.5}
```

Create an instance of the negotiator, ready to accept negotiation requests

```python
cn = ContentNegotiator(default_params, acceptable, weights)
```

Set up some more complex accept headers (you can try modifying the order of the elements without q values, and the q values themselves, to see different results).

```python
accept = "text/html, text/json;q=1.0, application/pdf;q=0.5"
accept_language = "en;q=0.5, de, cz, fr"
```

Negotiate over both headers, looking for an optimal solution to the client request

```python
acceptable = cn.negotiate(accept, accept_language)
```

The negotiator indicates the best fit to the client request is `text/html` in German

```python
>> acceptable
AcceptParameters:: Content Type: text/html;Language: de;
```

## Preference Ordering Rules

The Negotiator organises the preferences in each `Accept` header into a sequence,
from highest q value to lowest, grouping together equal q values.

For example, the HTTP `Accept` header:

```
"text/html, text/json;q=1.0, application/pdf;q=0.5"
```

Would result in the following preference sequence (as a python dictionary):

```python
{
    1.0 : ["text/json", "text/html"],
    0.5 : ["application/pdf"]
}
```

While the HTTP `Accept-Language` header:

```
"en;q=0.5, de, cz, fr"
```

Would result in the following preference sequence (as a python dictionary):

```python
{
    1.0 : ["de"],
    0.8 : ["cz"],
    0.6 : ["fr"],
    0.5 : ["en"]
}
```

(In reality, the q values for de, cz and fr would be evenly spaced between 1.0 and 0.5, using floating point numbers as the keys)

## Combined Preference Ordering Rules

The negotiator will compute all the possible allowed combinations and their weighted overall q values.

Given that the server supports the following combinations (from the code example above):

```
text/html, en
text/html, fr
text/html, de
text/json, en
text/json, cz
application/pdf, de
```

And given the weights:

```python
w = {"content_type" : 1.0, "language" : 0.5}
```

We can calculate the combined q value of each allowed (by both server and client) option, using the equation:

```python
overall_q = w["content_type"] * content_type_q + w["language"] * language_q
```

So, for the above options and q values from the previous section, we can generate the preference list (as a python dictionary):

```python
    {
        1.5  : ["text/html, de"],
        1.4  : ["text/json, cz"],
        1.3  : ["text/html, fr"],
        1.25 : ["text/html, en", "text/json, en"]
        1.0  : ["application/pdf, de"]
    }
```

It is clear, then, why the negotiator in the Advanced Usage section selected "text/html, de" as its preferred format.
