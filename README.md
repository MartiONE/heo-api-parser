# Introduction

heo-api-parser is a small repository that aims to create a method to extract and process [heo.com](https://www.heo.com/) catalog. The project contains a single spider that goes trough the entire website and downloads all of the items found.


# How to use it

## Clone the repo:

```
git clone https://github.com/MartiONE/heo-api-parser.git
```

## Install the required dependencies

with virtualenv:
```
virtualenv venv
source venv/bin/activate
pip install -r requirements
```

## Run the spider

```
scrapy crawl heo -o output.json
```

# Development
The project is on active development so any PR is welcome, I crafted a couple of things TODO but feel free to add or modify any.

- [ ] support database connection
- [ ] add section division via cli
- [ ] add support for custom sections
- [x] add login settings for pricing and volume purposes
- [ ] include FR and DE to the data schema
- [ ] image download and configuration
