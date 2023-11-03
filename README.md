# Score Review Documentation
This project has been developed and deployed with the primary objective of 
aggregating and calculating the average score of various tour operators. 
The data is sourced from the following streaming platforms:
- Viator
- Tripadvisor
- Expedia
- Klook
- Get your guide
- Tiquets
- Google


## Technical Overview
This project has been developed by using the Django REST Framework as backend and Angular as frontend.

The working mechanism to retrieve the data is the standard one,
the django framework exposes API endpoints that are interrogated by the angular platform.

Both the frontend and the backend reside in one EC2 Amazon server.
Both the frontend and the backend use a docker-compose infrastructure with nginx to expose the running ports of the systems.

- Port 8000 for the Backend
- Port 80 for the Frontend

### Frontend Infrastructure
The frontend infrastructure is pretty standard, angular is running in its compose 
bucket and nginx is exposing the application on the port 80.

### Backend Infrastructure
The backend is composed by the following services:
- The Django backend itself
- Nginx Proxy, to expose the backend outside to the port 8000
- Redis
- Celery
- Celery Beat

- Plus a selenium grid service that, for computational power requirements runs on another mor powerful server. 

The backend uses a `.env` file that is not pushed on the repository to keep all the secrets variable safe.
Below the description of the platform, you'll find a template for the `.env` file


### Django Backend
The Django backend is composed by four applications.

**API:**
\
This application serves as the central conduit for enabling seamless 
communication between the backend and the frontend by exposing 
structured data stored in the database. The `views` directory houses a 
comprehensive set of view functions responsible for retrieving, manipulating, 
and delivering data via the API.

**AUTHENTICATION:**
\
This application is the dedicated platform responsible for 
handling all authentication operations required to maintain 
data security and reliability for the frontend. It provides a 
suite of features including user login, password reset, role management, 
and employee account creation.

**SCORE REVIEW:**
\
Serving as the backbone of the entire software ecosystem, this Core Application is pivotal for orchestrating basic to advanced settings that govern how the application operates. The architecture of this core module is meticulously designed to allow seamless configuration, making it indispensable for overall system functionality.

One of the cornerstone files within this application is `tasks.py`. This Python script is not merely a file but the main gateway for task queue orchestration. It schedules, initializes, and manages various tasks, ensuring that they are executed in the correct sequence and with the necessary resources.

At the zenith of the `tasks.py` file, you'll encounter a function called `scrape()`. This function serves a crucial role — it gets triggered whenever there is a requirement to scrape a tour-related URL for data extraction. It's worth noting that the `scrape()` function is versatile, capable of accommodating different types of data scraping needs.

Digging deeper into the `scrape()` function, you'll come across a nested sub-function called `import_bot`. This sub-function embodies intelligence—it dynamically identifies the type of web scraper that is most suitable for the specific tour URL that needs to be scraped. This adaptability ensures a high rate of success in data retrieval operations.

For those interested in understanding the task queuing and data scraping functionalities in greater detail, additional insights and technical documentation can be found in the "STREAMS" application guide. This accompanying documentation will help you grasp the intricacies of how the Core Application interacts with other modules to accomplish complex tasks.

This holistic approach taken by the Core Application module underlines its importance in not just managing tasks but also in serving as the central nervous system that ensures the entire application runs cohesively and efficiently.


**STREAMS:**
\
This application serves as the central hub for our web scraping operations and is organized into two primary directories: `apis` and `scrapers`. 

The application is designed to retrieve streams of data through two distinct methods, depending on the source platform. For instance, Facebook streams can be easily accessed via its official API, while TripAdvisor doesn't offer such an API, necessitating the use of a custom Selenium scraper.

The `apis` folder typically contains scripts that use the official APIs provided by various platforms. This is a more straightforward method for data collection, relying on authenticated, programmatic access to the target platforms. Since this is a well-understood standard, there's little need for additional explanation.

On the other hand, the `scrapers` folder is a bit more intricate. When you delve into this directory, one of the key files you'll encounter is `main_bot.py`. 

The `main_bot.py` script serves multiple important functions:

1. **Launching Selenium Grid Sessions**: Selenium Grid is a suite of tools that allows simultaneous browser automation across different platforms and browsers. `main_bot.py` initiates these sessions, thereby enabling us to scrape data from platforms that require more complex interactions than a simple API call.

2. **Managing Sessions**: The script is not just responsible for launching the Selenium sessions; it also manages their lifecycle, ensuring that they are effectively utilized and shut down after their tasks are completed.

3. **Proxy Rotation**: An essential feature integrated into `main_bot.py` is the use of rotating proxies. This is particularly important for obfuscating our scraping activities from the targeted platforms, thereby reducing the chances of our operations being flagged or blocked.

In Summary the architectural division into `apis` and `scrapers` allows our application to be versatile in its data collection methods. While the API approach offers a clean, authorized way to gather data, the Selenium-based scrapers give us the flexibility to collect data from platforms where API access is either restricted or non-existent. Both methods are orchestrated from the central `main_bot.py` script in the `scrapers` folder, which manages the more complex aspects of the operation, such as Selenium Grid sessions and proxy rotation.

The flow of the scraper is the following:

1. The `scrape()` function present in the `tasks.py` file, triggers a `Bot()` class instance.
2. The Bot class triggered runs the script needed (for example the script `bot.py` for the Tripadvisor scraper)
3. The `bot.py` runs a `super().__init__(__file__)` function to start the selenium grid session on the server.
4. The `bot.py` runs the `self.start()` functions.
5. Then the bot retrieve the data by using the instruction provided from the scraper script
6. Save the data on the database
7. The `bot.py` calls `self.close(self.results)` and close the selenium grid session.
8. At this point the data is available through the `API` Django application.

This application provides a management command to launch bulk scraping sessions of various stream.

In order to launch bulk sessions you need to use the following commands:
```commandline
 docker exec -it scorereview_backend_1 /bin/sh
 python3 manage.py scrape_toururls {stream_id}
```

Streams id:

    VIATOR = 1
    TRIPADVISOR = 3
    EXPEDIA = 4
    KLOOK = 5
    GETYOURGUIDE = 7
    GOOGLE = 9
    TIQUETS = 12

The scraping mechanism queue has a max concurrency value.
Right now this value is set to 4, as we are currently using 4 rotating proxy for this project, but it can be changed in a higher or lower number.

>Our Selenium grid server, right now can host up to 12 simultaneous session.

This value can be changed in the `docker-compose.yaml` file, in the celery command where you see `--concurrency=4`

```yaml
    command: celery -A score_review worker --concurrency=4 --prefetch-multiplier=1 -l info
```


## Models (Database schema)
### List of Models Present:

1. `Review`
2. `TourOperator`
3. `Tour`
4. `TourURL`
5. `Country`
6. `State`
7. `City`
8. `User`

### How the Models are Linked:

1. **Review ⇆ Tour**:  
   - A `Review` has a foreign key relationship with `Tour`, which means each `Review` is associated with a `Tour` (`tour` field in `Review`).
   - The reverse relation `reviews` allows you to access all the `Review` instances related to a particular `Tour`.

2. **Tour ⇆ TourOperator**:  
   - A `Tour` has a foreign key relationship with `TourOperator`, indicating that each `Tour` belongs to a `TourOperator` (`tour_operator` field in `Tour`).

3. **Tour ⇆ TourURL**:  
   - A `Tour` has a one-to-many relationship with `TourURL`, meaning one `Tour` can have multiple `TourURL` objects associated with it (`tour` field in `TourURL`).
   - The reverse relation `tour_urls` allows you to access all the `TourURL` instances related to a particular `Tour`.

4. **Tour ⇆ Country, State, City**:  
   - A `Tour` can be associated with a `Country`, `State`, or `City` through foreign keys (`country_id`, `state_id`, `city_id` fields in `Tour`).

5. **State ⇆ Country**:  
   - A `State` is associated with a `Country` (`country` field in `State`).

6. **City ⇆ State**:  
   - A `City` is associated with a `State` (`state` field in `City`).

7. **User (Self-referencing)**:  
   - `User` has a foreign key relationship with itself to indicate who created the `User` (`created_by` field in `User`).

Each model has its own fields and may include optional fields, constraints, or choices that constrain the data that can be stored.

The `User` model is an extended version of Django's `AbstractUser` model, including additional fields like `role`, `groups`, `timezone`, and others.

Hopefully, this helps you understand how these models are interconnected!
____

## Developing

If you are trying to improve or debug the system, you can run celery on your local computer with the following commands:

```commandline
kill -9 $(ps aux | grep celery | grep -v grep | awk '{print $2}' | tr '\n'  ' ') > /dev/null 2>&1
celery -A score_review worker --concurrency=2 --prefetch-multiplier=1 -l info
celery -A score_review beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```


### Installation

If you need to deploy a new version of the system you need to use the following commands.


Run the docker:
```commandline
docker-compose -f docker/docker-compose.yaml -p ScoreReview up -d --build
```

Enter in the docker shell:
```commandline
 docker exec -it scorereview_backend_1 /bin/sh
```

Run the migrations:
```commandline
python3 manage.py migrate
python3 manage.py collectstatic
```

Create a superuser
```commandline
python3 manage.py createsuperuser
```

If you need to debug bots, you can easily run a test one with the following command in the django shell:
``` Debug bots
from streams.scrapers.utilities import import_bot
bot = import_bot('civitatis')
self = bot()
```


### Template for the `.env` file:

```
ENV_NAME=local
DEBUG=True
PRODUCTION=False
DATABASE_URL=sqlite:///stt/db.sqlite3
ALLOWED_HOSTS=*
CORS_ORIGIN_WHITELIST=*
SQL_ENGINE=django.db.backends.mysql

SECRET_KEY='somesecretkey'
MYSQL_DATABASE=ScoreReview
MYSQL_USER=ScoreReview
MYSQL_PASSWORD=ScoreReview
MYSQL_ROOT_PASSWORD=ScoreReview
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307

MYSQL_CHARSET=utf8mb4
MYSQL_COLLATION=utf8mb4_unicode_ci


SELENIUM_GRID_HOST=16.170.222.97

```