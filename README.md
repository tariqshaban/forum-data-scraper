Data Scraping on Forums Website
==============================
This is a submission of **assignment 2** for the **CIS711** course.

It contains the code necessary to scrape data from a selected forum website.

This repository is merely a demonstration of how web scraping performs.


Getting Started
------------
Clone the project from GitHub

`$ git clone https://github.com/tariqshaban/forum-data-scraper.git`

Install numpy
`pip install numpy`

Install pandas
`pip install pandas`

install matplotlib
`pip install matplotlib.pyplot`

Install scipy
`pip install scipy`

Install cloudscraper
`pip install cloudscraper`

Install beautiful soup
`pip install bs4`

You may need to configure the Python interpreter (depending on the used IDE)

No further configuration is required.


Project Structure
------------
    ├── README.md                 <- The top-level README for developers using this project.
    │
    ├── helpers
    │   ├── date_time_handler     <- Set of static methods that aid some time manipulations
    │   └── progress_handler      <- Set of static methods that aid some progress manipulations
    │
    ├── providers
    │   ├── plots_provider        <- Static methods which perform the plotting functionality
    │   └── forum_scraper         <- Static methods which perform the scraping functionality
    │
    └── main                      <- Acts as a sandbox for methods invocation


Report / Findings
------------
### What tools have been used to scrape data off the web?

Beautiful Soup has been used for scraping; it contains abstract out-of-the-box methods that help extract information
from the HTML file.

> Beautiful Soup is a Python library for pulling
> data out of HTML and XML files. It works with your
> favorite parser to provide idiomatic ways of navigating,
> searching, and modifying the parse tree.
> It commonly saves programmers hours or days of work.

There were no modifications committed for this scraping tool since it already satisfies the required objectives.

We used cloudscraper instead of the well-known requests since the website is protected under Cloudflare bot spam
detection, a normal HTTP request would not suffice (returns forbidden 403 status code)

### What were the target websites?

Primarily [Mental Health Forum](https://www.mentalhealthforum.net/),
[covid-19-mental-health](https://www.mentalhealthforum.net/forum/forums/coronavirus-covid-19-mental-health.394/)
subforum

### What information did you extract?

We successfully collected information of the following:

* Thread
    * Thread ID
    * Poster ID
    * Poster Name
    * Poster Image
    * Last Replier ID
    * Last Replier Name
    * Last Replier Image
    * Last Replier Date
    * Date Posted
    * Title
    * Status
        * IsLocked :lock:
        * Is Sticky :pushpin:
    * Replies
    * Views
* Thread's Details
    * Thread ID
    * User ID
    * User Name
    * User Image
    * User Title
    * User Banners
    * User Join Date
    * User Total Sent Messages
    * User Location
    * Reactions
        * Like :thumbsup:
        * Thanks :grinning:
        * Hug :hugs:
    * User Post Date
    * User Post

### What manipulations have you made for the data?

* Thread
    * Column datatype conversion
    * Replaced blank spaces/empty values with nulls
* Thread's Details
    * Column datatype conversion
    * Replaced blank spaces/empty values with nulls

### What illustrations have you made?

***TBA***

--------