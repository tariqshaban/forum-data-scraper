import datetime

import cloudscraper as cloudscraper
import pandas as pd
import numpy as np
import bs4
import re
from helpers.date_time_handler import DateTimeHandler
from helpers.progress_handler import ProgressHandler


class ForumScraper:
    """
    Static methods which perform the scraping functionality.

    Attributes
    ----------
        __threads           Acts as a cache for storing threads
        __threads_details   Acts as a cache for storing thread's details

    Methods
    -------
        __get_cached_threads():
            Retrieves the threads snapshot.
        cache_threads():
            Collects a snapshot of the threads for faster fetch in the future.
        __get_threads_pagination():
            Returns the pagination of the threads
        __scrap_threads():
            Scraps data containing a list of threads.
        scrap_threads():
            Calls __scrap_threads if __threads is None, otherwise, it retrieves __threads immediately.

        __get_cached_threads_details():
            Retrieves the thread's details snapshot.
        cache_threads_details():
            Collects a snapshot of the thread's details for faster fetch in the future.
        __get_threads_details_pagination():
            Returns the pagination of the thread's details
        __scrap_threads_details():
            Scraps data containing a list of thread's details.
        scrap_threads_details():
            Calls __scrap_threads_details if __threads_details is None, otherwise,
            it retrieves __threads_details immediately.
    """

    __threads = None
    __threads_details = None

    @staticmethod
    def __get_cached_threads():
        """
        Retrieves the threads snapshot.
        """

        threads_df = pd.read_csv('cached_threads.csv', index_col='thread_id')

        threads_df['last_replied_date'] = pd.to_datetime(threads_df['last_replied_date'], utc=True)
        threads_df['date_posted'] = pd.to_datetime(threads_df['date_posted'], utc=True)

        return threads_df

    @staticmethod
    def cache_threads():
        """
        Collects a snapshot of the threads for faster fetch in the future.
        """
        threads_df = ForumScraper.scrap_threads()

        # noinspection PyTypeChecker
        threads_df.to_csv('cached_threads.csv')

    @staticmethod
    def __get_threads_pagination():
        """
        Returns the pagination of the threads

        :return: The last page number
        """

        # This site is protected under CloudFlare bot spam detection, a normal http request would not suffice
        scraper = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
        # Partially prevents scraping detection
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
        res = scraper.get(f'https://www.mentalhealthforum.net/forum/forums/coronavirus-covid-19-mental-health.394/',
                          headers=headers)

        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        pages = soup.find('ul', attrs={'class': 'pageNav-main'})

        if not pages:
            return 1

        last_page = pages.find_all('a')[-1].text
        return last_page

    @staticmethod
    def __scrap_threads(fast_fetch=False):
        """
        Scraps data containing a list of threads.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        :return: A threads dataframe
        """

        if fast_fetch:
            return ForumScraper.__get_cached_threads()

        threads_df = pd.DataFrame()

        data = []
        processed = 0

        pagination = int(ForumScraper.__get_threads_pagination())

        for page in np.arange(1, pagination + 1):
            print(ProgressHandler.show_progress(processed, pagination))
            processed += 1

            # This site is protected under CloudFlare bot spam detection, a normal http request would not suffice
            scraper = cloudscraper.create_scraper(
                browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
            # Partially prevents scraping detection
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
            res = scraper.get(
                f'https://www.mentalhealthforum.net/forum/forums/coronavirus-covid-19-mental-health.394/'
                f'page-{page}',
                headers=headers)

            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            threads = soup \
                .find_all('div',
                          {'class': ['structItemContainer-group js-threadList',
                                     'structItemContainer-group structItemContainer-group--sticky XenStickyBg']})

            new_threads = []
            for threads_container in threads:
                new_threads.append(threads_container.find_all('div', attrs={
                    'class': re.compile('^structItem structItem--thread js-inlineModContainer.*')}))

            threads = new_threads

            if not threads:
                continue

            for threads_container in threads:
                for thread in threads_container:
                    thread_id = thread['class'][-1].split('-')[-1]
                    poster_id = thread.find_all(['span', 'a'], {'class', 'username'})[0]['data-user-id']
                    poster_name = thread.find_all(['span', 'a'], {'class', 'username'})[0].text

                    poster_image = None
                    poster_image_container = thread.find('span', {'class', 'avatar avatar--s'})
                    if poster_image_container is not None:
                        poster_image = poster_image_container.find('img')['src']

                    last_replier_id = thread.find_all(['span', 'a'], {'class', 'username'})[-1]['data-user-id']
                    last_replier_name = thread.find_all(['span', 'a'], {'class', 'username'})[-1].text

                    last_replier_image = None
                    last_replier_image_container = thread.find('span', {'class', 'avatar avatar--xxs'})
                    if last_replier_image_container is not None:
                        last_replier_image = last_replier_image_container.find('img')['src']

                    last_replied_date = DateTimeHandler.datetime_from_utc_to_local(
                        datetime.datetime.strptime(thread.find_all('time')[-1]['datetime'], '%Y-%m-%dT%H:%M:%S%z'))
                    date_posted = DateTimeHandler.datetime_from_utc_to_local(
                        datetime.datetime.strptime(thread.find_all('time')[0]['datetime'], '%Y-%m-%dT%H:%M:%S%z'))
                    title = thread.find('div', {'class': 'structItem-title'}).find('a').text
                    is_locked = thread.find('i', {'class': 'structItem-status structItem-status--locked'}) is not None
                    is_sticky = thread.find('i', {'class': 'structItem-status structItem-status--sticky'}) is not None
                    replies = thread.find('div', {'class', 'structItem-cell structItem-cell--meta'}).find_all('dd')[
                        0].text
                    views = thread.find('div', {'class', 'structItem-cell structItem-cell--meta'}).find_all('dd')[
                        -1].text

                    data.append(
                        [thread_id, poster_id, poster_name, poster_image,
                         last_replier_id, last_replier_name, last_replier_image, last_replied_date,
                         date_posted, title,
                         is_locked, is_sticky, replies, views])

        threads_df = threads_df.append(data)

        if threads_df.empty:
            threads_df = pd.DataFrame(np.empty((0, 11)))

        threads_df.columns = ['thread_id', 'poster_id', 'poster_name', 'poster_image',
                              'last_replier_id', 'last_replier_name', 'last_replier_image', 'last_replied_date',
                              'date_posted', 'title',
                              'is_locked', 'is_sticky', 'replies', 'views']

        threads_df = threads_df.replace(r'^\s*$', np.nan, regex=True) \
            .fillna(value=np.nan) \
            .dropna(thresh=3) \
            .reset_index(drop=True)

        threads_df.set_index('thread_id', inplace=True)

        threads_df['replies'] = (threads_df['replies'].replace(r'[KM]+$', '', regex=True).astype(int) *
                                 threads_df['replies'].str.extract(r'[\d\.]+([KM]+)', expand=False)
                                 .fillna(1)
                                 .replace(['K', 'M'], [10 ** 3, 10 ** 6]).astype(int))

        threads_df['views'] = (threads_df['views'].replace(r'[KM]+$', '', regex=True).astype(int) *
                               threads_df['views'].str.extract(r'[\d\.]+([KM]+)', expand=False)
                               .fillna(1)
                               .replace(['K', 'M'], [10 ** 3, 10 ** 6]).astype(int))

        cols = ['replies', 'views']
        threads_df[cols] = threads_df[cols].apply(pd.to_numeric)

        threads_df['last_replied_date'] = pd.to_datetime(threads_df['last_replied_date'], utc=True)
        threads_df['date_posted'] = pd.to_datetime(threads_df['date_posted'], utc=True)

        ProgressHandler.reset_progress()
        return threads_df

    @staticmethod
    def scrap_threads(fast_fetch=False):
        """
        Calls __scrap_threads if __threads is None, otherwise, it retrieves __threads immediately.

        :param bool fast_fetch: Retrieves thread's details from a saved snapshot instantly
        :return: A thread dataframe
        """

        if ForumScraper.__threads is None:
            print('Fetching threads, this is a one time process...')
            ForumScraper.__threads = ForumScraper.__scrap_threads(fast_fetch=fast_fetch)
            print('Received threads\n')

        return ForumScraper.__threads.copy()

    @staticmethod
    def __get_cached_threads_details():
        """
        Retrieves the thread's details snapshot.
        """

        threads_details_df = pd.read_csv('cached_threads_details.csv', index_col='thread_id')

        threads_details_df['user_join_date'] = pd.to_datetime(threads_details_df['user_join_date'], utc=True)
        threads_details_df['user_post_date'] = pd.to_datetime(threads_details_df['user_post_date'], utc=True)

        return threads_details_df

    @staticmethod
    def cache_threads_details():
        """
        Collects a snapshot of the thread's details for faster fetch in the future.
        """
        threads_details_df = ForumScraper.scrap_threads_details()

        # noinspection PyTypeChecker
        threads_details_df.to_csv('cached_threads_details.csv')

    @staticmethod
    def __get_threads_details_pagination(thread_id):
        """
        Returns the pagination of the thread's details

        :return: The last page number
        """

        # This site is protected under CloudFlare bot spam detection, a normal http request would not suffice
        scraper = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
        # Partially prevents scraping detection
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
        res = scraper.get(f'https://www.mentalhealthforum.net/forum/threads/{thread_id}', headers=headers)

        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        pages = soup.find('ul', attrs={'class': 'pageNav-main'})

        if not pages:
            return 1

        last_page = pages.find_all('a')[-1].text
        return last_page

    @staticmethod
    def __scrap_threads_details(fast_fetch=False, fast_fetch_threads=False):
        """
        Scraps data containing a list of thread's details.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        :param fast_fetch_threads: Retrieves threads from a saved snapshot instantly
        :return: A thread's details dataframe
        """

        if fast_fetch:
            return ForumScraper.__get_cached_threads_details()

        threads_details_df = pd.DataFrame()

        data = []

        processed = 0

        threads_ids = ForumScraper.scrap_threads(fast_fetch=fast_fetch_threads).index

        for thread_id in threads_ids:
            processed += 1
            pagination = int(ForumScraper.__get_threads_details_pagination(thread_id=thread_id))
            for page in np.arange(1, pagination + 1):
                print(ProgressHandler.show_progress(processed, len(threads_ids)))

                # This site is protected under CloudFlare bot spam detection, a normal http request would not suffice
                scraper = cloudscraper.create_scraper(
                    browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
                res = scraper.get(
                    f'https://www.mentalhealthforum.net/forum/threads/'
                    f'{thread_id}/'
                    f'page-{page}')

                soup = bs4.BeautifulSoup(res.text, 'html.parser')

                thread_details = soup \
                    .find_all('article', {'class': 'message message--post js-post js-inlineModContainer'})

                if not thread_details:
                    continue

                for post in thread_details:
                    user_id = post.find_all(['span', 'a'], {'class', 'username'})[0]['data-user-id']
                    user_name = post.find_all(['span', 'a'], {'class', 'username'})[0].text

                    user_image = None
                    user_image_container = post.find('span', {'class', 'avatar avatar--m'})
                    if user_image_container is not None:
                        user_image = user_image_container.find('img')['src']

                    user_title = post.find('h5', {'class', 'userTitle message-userTitle'}).text

                    banners = post.find('div', {'class', 'message-userDetails'}) \
                        .find_all('div', {'class': re.compile('^userBanner userBanner.*')})
                    user_banner_1 = None
                    user_banner_2 = None
                    if banners is not None:
                        if len(banners) >= 1:
                            user_banner_1 = banners[0].find('strong').text
                        if len(banners) > 1:
                            user_banner_2 = banners[1].find('strong').text

                    user_extras = post.find('div', {'class': 'message-userExtras'})
                    user_join_date = None
                    user_messages = None
                    user_location = None
                    if user_extras:
                        user_extras = user_extras.find_all('dd')
                        user_join_date = datetime.datetime.strptime(user_extras[0].text, '%b %d, %Y')
                        user_messages = user_extras[1].text.replace(',', '')
                        if len(user_extras) > 2:
                            user_location = user_extras[2].find('a').text

                    reactions = post.find('ul', {'class': 'sv-rating-bar__ratings'})
                    post_reaction_like = None
                    post_reaction_thanks = None
                    post_reaction_hug = None
                    if reactions:
                        post_reaction_like = reactions.find('a', {'title': 'Like'})
                        post_reaction_thanks = reactions.find('a', {'title': 'Thanks'})
                        post_reaction_hug = reactions.find('a', {'title': 'Hug'})
                        if post_reaction_like is not None:
                            post_reaction_like = post_reaction_like.find('div', {'class', 'sv-rating__count'}).text
                        if post_reaction_thanks is not None:
                            post_reaction_thanks = post_reaction_thanks.find('div', {'class', 'sv-rating__count'}).text
                        if post_reaction_hug is not None:
                            post_reaction_hug = post_reaction_hug.find('div', {'class', 'sv-rating__count'}).text

                    user_post_date = datetime.datetime.strptime(
                        post.find('time', {'class', 'u-dt'})['datetime'], '%Y-%m-%dT%H:%M:%S%z')

                    user_post = ' '.join(post.find('div', {'class', 'message-userContent'}).text.split())

                    data.append(
                        [thread_id, user_id, user_name, user_image, user_title, user_banner_1,
                         user_banner_2, user_join_date, user_messages, user_location,
                         post_reaction_like, post_reaction_thanks, post_reaction_hug,
                         user_post_date, user_post])

        threads_details_df = threads_details_df.append(data)

        if threads_details_df.empty:
            threads_details_df = pd.DataFrame(np.empty((0, 13)))

        threads_details_df.columns = ['thread_id', 'user_id', 'user_name', 'user_image', 'user_title', 'user_banner_1',
                                      'user_banner_2', 'user_join_date', 'user_messages', 'user_location',
                                      'post_reaction_like', 'post_reaction_thanks', 'post_reaction_hug',
                                      'user_post_date', 'user_post']

        threads_details_df = threads_details_df.replace(r'^\s*$', np.nan, regex=True) \
            .fillna(value=np.nan) \
            .dropna(thresh=3) \
            .reset_index(drop=True)

        threads_details_df.set_index('thread_id', inplace=True)

        cols = ['user_messages', 'post_reaction_like', 'post_reaction_thanks', 'post_reaction_hug']
        threads_details_df[cols] = threads_details_df[cols].apply(pd.to_numeric)

        threads_details_df['user_join_date'] = pd.to_datetime(threads_details_df['user_join_date'], utc=True)
        threads_details_df['user_post_date'] = pd.to_datetime(threads_details_df['user_post_date'], utc=True)

        ProgressHandler.reset_progress()
        return threads_details_df

    @staticmethod
    def scrap_threads_details(fast_fetch=False, fast_fetch_threads=False):
        """
        Calls __scrap_threads_details if __threads_details is None, otherwise,
        it retrieves __threads_details immediately.

        :param bool fast_fetch: Retrieves thread's details from a saved snapshot instantly
        :param fast_fetch_threads: Retrieves threads from a saved snapshot instantly
        :return: A thread's details dataframe
        """

        if ForumScraper.__threads_details is None:
            print('Fetching threads_details, this is a one time process...')
            ForumScraper.__threads_details = ForumScraper.__scrap_threads_details(fast_fetch=fast_fetch,
                                                                                  fast_fetch_threads=fast_fetch_threads)
            print('Received threads_details\n')

        return ForumScraper.__threads_details.copy()
