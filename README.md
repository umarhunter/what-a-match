
# What-A-Match

This project incorporates Gale-Shapley's (1962) and Irving's (1985) algorithms for Stable Matching and Stable Roommate (respectively). This project was created as my final project for Hunter College's **CSCI49387: Distributed Artificial Intelligence** taught by Dr. Anita Raja. 

A long term goal is to also incorporate Niclas Boehmer & Klaus Heeger's paper "Adapting Stable Matchings to Forced and Forbidden Pairs" [[AAMAS 2023]](https://arxiv.org/abs/2204.10040) so we can adapt our matches as the scenarios shift. 

## Demo

This project is **not complete** as of right now. Nevertheless, current progress can be seen on the [deployed website](https://whatamatch-06b09a339de1.herokuapp.com/).

## Installation

Clone the project

```bash
  git clone https://github.com/umarhunter/what-a-match.git
```

Navigate to the project's directory

```bash
  cd what-a-match
```
Install all dependencies with Anaconda (creating a new environment)

```bash
  conda env create -f environment.yml
```
Activate the new environment

```bash
  conda activate my_env
```
## Run Locally

Go to the project directory

```bash
  cd what-a-match
```

Make necessary migrations

```bash
  python manage.py makemigrations
```

Make necessary migrations

```bash
  python manage.py migrate
```

Start the Django server

```bash
  python manage.py runserver
```







## Acknowledgements

 - [Gale & Shapley](https://www.jstor.org/stable/2312726?origin=JSTOR-pdf)
 - [Robert W. Irving](https://www.sciencedirect.com/science/article/abs/pii/0196677485900331)
 - [Niclas Boehmer & Klaus Heeger](https://arxiv.org/abs/2204.10040)
 - [Anita Raja](https://anraja.commons.gc.cuny.edu/)


## Authors

- [@umarhunter](https://www.github.com/umarhunter)

