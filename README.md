# About

API for viewing roll calls and votes in the United States Congress. This API
currently only supports Senate data (as provided by [senate.gov](https://senate.gov)); support for
Congress is forthcoming.

You can try out the service [here](https://senatevotes.gq).

# Usage

## As a Library

`src.api` exposes two public functions.

- `votes_for_range`: generates [Vote](#vote-object)s for the given date range.
  Optionally uses local caching to avoid making HTTP requests on subsequent
  calls. See documentation in `src/api/vote.py` for detailed usage instructions.
- `rolls_for_range`: generates [Roll](#roll-object)s for the given date range.
  Optionally uses local caching to avoid making HTTP requests on subsequent
  calls. See documentation in `src/api/roll.py` for detailed usage instructions.

## As a Service

From project root, run

```
$ FLASK_APP=congress PYTHONPATH=`pwd` flask run
```

Navigate to [localhost:5000](localhost:5000). There you will be able to enter initial and final
dates (half-open interval). The service will generate a .csv file tabulating all
legistlators' voting behavior in the given date range.

# Objects

## Vote <a name="vote-object" />
[Source](src/objects/vote.py)

Votes encapsulate data about single measures put before congress. This includes
the measure's title and number, date, voting behavior of every legislator, etc.
A Vote is a straightforward translation of [senate.gov](https://senate.gov)'s XML format,
[e.g.](https://www.senate.gov/legislative/LIS/roll_call_votes/vote1162/vote_116_2_00080.xml)

## Roll <a name="roll-object" />
[Source](src/objects/roll.py)

Rolls encapsulate all measures put before a house of congress in a given year.
Rolls mostly contain lists of votes. A Roll is a straightforward translation
of [senate.gov]'s XML format,
[e.g.](https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_116_2.xml)
