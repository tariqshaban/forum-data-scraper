import pandas as pd

from providers.forum_scraper import ForumScraper
import matplotlib.pyplot as plt
import seaborn as sns


class PlotsProvider:
    """
    Static methods which perform the plotting functionality.

    Attributes
    ----------

    Methods
    -------
        plot_threads_posting(fast_fetch=True):
            Shows the number of thread's creation trend.
        plot_monthly_views_with_replies(fast_fetch=True):
            Shows the number of views trend alongside the replies.
        plot_daily_views_with_replies(fast_fetch=True):
            Shows the number of views trend alongside the replies for each day in the week.
        plot_view_with_replies_relation(fast_fetch=True):
            Shows the relation between views and replies.
        plot_top_15_thread_creators(fast_fetch=True):
            Shows the ranking of user's number of threads posted.
        plot_locked_sticky_threads(fast_fetch=True):
            Shows the percentage of locked/sticky threads.

        plot_top_15_repliers(fast_fetch=True, fast_fetch_threads=True):
            Shows the ranking of user's number of replies posted.
        plot_top_15_messages(fast_fetch=True, fast_fetch_threads=True):
            Shows the ranking of user's number of messages on all forums.
        plot_user_titles(fast_fetch=True, fast_fetch_threads=True):
            Shows the distribution of user's titles.
        plot_user_banners(fast_fetch=True, fast_fetch_threads=True):
            Shows the distribution of user's banners.
        plot_users_joining(fast_fetch=True, fast_fetch_threads=True):
            Shows the cumulative distribution in user numbers over time.
        plot_user_top_10_locations(fast_fetch=True, fast_fetch_threads=True):
            Shows the distribution of user's locations.
    """

    @staticmethod
    def plot_threads_posting(fast_fetch=True):
        """
        Shows the number of thread's creation trend.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        """

        df = ForumScraper.scrap_threads(fast_fetch=fast_fetch)

        fig, ax = plt.subplots(figsize=(10, 9))

        df['date_posted'] = df['date_posted'].map(lambda x: x.strftime('%Y-%m'))

        df = df.reset_index().groupby('date_posted')['thread_id'].count()

        df.plot(kind='bar', ax=ax)

        ax.set_xlabel('Months')
        ax.set_ylabel('Posts')

        fig.suptitle('Amount of Posts Over Time', fontsize=20)

        plt.show()

    @staticmethod
    def plot_monthly_views_with_replies(fast_fetch=True):
        """
        Shows the number of views trend alongside the replies.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        """

        df = ForumScraper.scrap_threads(fast_fetch=fast_fetch)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 9))

        df['date_posted'] = df['date_posted'].map(lambda x: x.strftime('%Y-%m'))

        df_views = df.groupby('date_posted')['views'].sum()
        df_replies = df.groupby('date_posted')['replies'].sum()

        df_views.plot(kind='bar', ax=ax1)
        df_replies.plot(kind='bar', ax=ax2)

        ax1.set_xlabel('Months')
        ax2.set_xlabel('Months')
        ax1.set_ylabel('Views')
        ax2.set_ylabel('Comments')

        fig.suptitle('Amount of Views & Replies Over Time', fontsize=20)

        plt.show()

    @staticmethod
    def plot_daily_views_with_replies(fast_fetch=True):
        """
        Shows the number of views trend alongside the replies for each day in the week.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        """

        df = ForumScraper.scrap_threads(fast_fetch=fast_fetch)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 9))

        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

        df_views = df.groupby(df['date_posted'].dt.strftime("%a"))['views'].sum().reindex(days)
        df_replies = df.groupby(df['date_posted'].dt.strftime("%a"))['replies'].sum().reindex(days)

        df_views.plot(kind='bar', ax=ax1)
        df_replies.plot(kind='bar', ax=ax2)

        ax1.set_xlabel('Day of Week')
        ax2.set_xlabel('Day of Week')
        ax1.set_ylabel('Views')
        ax2.set_ylabel('Comments')

        fig.suptitle('Amount of Views & Replies During The Days of Weeks', fontsize=20)

        plt.show()

    @staticmethod
    def plot_view_with_replies_relation(fast_fetch=True):
        """
        Shows the relation between views and replies.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        """

        df = ForumScraper.scrap_threads(fast_fetch=fast_fetch)

        fig, ax = plt.subplots(figsize=(10, 9))

        sns.regplot(x=df['views'], y=df['replies'])

        ax.set_xlabel('Views')
        ax.set_ylabel('Replies')

        fig.suptitle('Relationship between views and replies', fontsize=20)

        plt.show()

    @staticmethod
    def plot_top_15_thread_creators(fast_fetch=True):
        """
        Shows the ranking of user's number of threads posted.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        """

        df = ForumScraper.scrap_threads(fast_fetch=fast_fetch)

        fig, ax = plt.subplots(figsize=(10, 9))

        df = df.groupby('poster_name')['poster_name'].count().sort_values(ascending=False).head(15)

        df.plot(kind='bar', ax=ax)

        ax.set_xlabel('Users')
        ax.set_ylabel('Posts')

        plt.xticks(rotation=20)

        fig.suptitle('Top 15 Thread Creators', fontsize=20)

        plt.show()

    @staticmethod
    def plot_locked_sticky_threads(fast_fetch=True):
        """
        Shows the percentage of locked/sticky threads.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        """

        df = ForumScraper.scrap_threads(fast_fetch=fast_fetch)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 9))

        locked = [df[df['is_locked']].count()['poster_id'], df[~df['is_locked']].count()['poster_id']]
        sticky = [df[df['is_sticky']].count()['poster_id'], df[~df['is_sticky']].count()['poster_id']]

        locked_labels = ['Locked', 'Non-Locked']
        sticky_labels = ['Sticky', 'Non-Sticky']

        locked_explode = [0.1, 0]
        sticky_explode = [0.1, 0]

        ax1.pie(locked, labels=locked_labels, explode=locked_explode,
                autopct='%.3f', pctdistance=1.1, labeldistance=1.3, startangle=45)
        ax2.pie(sticky, labels=sticky_labels, explode=sticky_explode,
                autopct='%.3f', pctdistance=1.1, labeldistance=1.3, startangle=45)

        fig.suptitle('Locked/Sticky Percentage', fontsize=20)

        plt.show()

    @staticmethod
    def plot_top_15_repliers(fast_fetch=True, fast_fetch_threads=True):
        """
        Shows the ranking of user's number of replies posted.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        :param fast_fetch_threads: Retrieves threads from a saved snapshot instantly
        """

        df = ForumScraper.scrap_threads_details(fast_fetch=fast_fetch, fast_fetch_threads=fast_fetch_threads)

        fig, ax = plt.subplots(figsize=(10, 9))

        df = df.groupby('user_name')['user_name'].count().sort_values(ascending=False).head(15)

        df.plot(kind='bar', ax=ax)

        ax.set_xlabel('Users')
        ax.set_ylabel('Replies')

        plt.xticks(rotation=20)

        fig.suptitle('Top 15 Repliers', fontsize=20)

        plt.show()

    @staticmethod
    def plot_top_15_messages(fast_fetch=True, fast_fetch_threads=True):
        """
        Shows the ranking of user's number of messages on all forums.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        :param fast_fetch_threads: Retrieves threads from a saved snapshot instantly
        """

        df = ForumScraper.scrap_threads_details(fast_fetch=fast_fetch, fast_fetch_threads=fast_fetch_threads)

        fig, ax = plt.subplots(figsize=(10, 9))

        df.drop_duplicates('user_name', inplace=True)
        df = df.groupby('user_name')['user_messages'].sum().sort_values(ascending=False).head(15)

        df.plot(kind='bar', ax=ax)

        ax.set_xlabel('Users')
        ax.set_ylabel('Messages')

        plt.xticks(rotation=20)

        fig.suptitle('Top 15 Messages on All Forums', fontsize=20)

        plt.show()

    @staticmethod
    def plot_user_titles(fast_fetch=True, fast_fetch_threads=True):
        """
        Shows the distribution of user's titles.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        :param fast_fetch_threads: Retrieves threads from a saved snapshot instantly
        """

        df = ForumScraper.scrap_threads_details(fast_fetch=fast_fetch, fast_fetch_threads=fast_fetch_threads)

        fig, ax = plt.subplots(figsize=(10, 9))

        df.drop_duplicates('user_name', inplace=True)
        df = df.groupby('user_title')['user_title'].count().sort_values(ascending=False)

        df.plot(kind='bar', ax=ax)

        ax.set_xlabel('Titles')
        ax.set_ylabel('Count')

        plt.xticks(rotation=20)

        fig.suptitle('Distribution of User\'s Titles', fontsize=20)

        plt.show()

    @staticmethod
    def plot_user_banners(fast_fetch=True, fast_fetch_threads=True):
        """
        Shows the distribution of user's banners.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        :param fast_fetch_threads: Retrieves threads from a saved snapshot instantly
        """

        df = ForumScraper.scrap_threads_details(fast_fetch=fast_fetch, fast_fetch_threads=fast_fetch_threads)

        fig, ax = plt.subplots(figsize=(10, 9))

        df.drop_duplicates('user_name', inplace=True)
        df1 = df.groupby('user_banner_1')['user_banner_1'].count().sort_values(ascending=False)
        df2 = df.groupby('user_banner_2')['user_banner_2'].count().sort_values(ascending=False)

        df = pd.concat([df1, df2], axis=1).sum(axis=1)

        df.plot(kind='bar', ax=ax)

        ax.set_xlabel('Banners')
        ax.set_ylabel('Count')

        plt.xticks(rotation=20)

        fig.suptitle('Distribution of User\'s Banners', fontsize=20)

        plt.show()

    @staticmethod
    def plot_users_joining(fast_fetch=True, fast_fetch_threads=True):
        """
        Shows the cumulative distribution in user numbers over time.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        :param fast_fetch_threads: Retrieves threads from a saved snapshot instantly
        """

        df = ForumScraper.scrap_threads_details(fast_fetch=fast_fetch, fast_fetch_threads=fast_fetch_threads)

        fig, ax = plt.subplots(figsize=(10, 9))

        df['user_join_date'] = df['user_join_date'].map(lambda x: x.strftime('%Y'))

        df.drop_duplicates('user_name', inplace=True)
        df = df.groupby('user_join_date')['user_join_date'].count().cumsum()

        df.plot(kind='line', ax=ax)

        ax.set_xlabel('Duration')
        ax.set_ylabel('Users')

        fig.suptitle('Cumulative Distribution in User Numbers Over Time', fontsize=20)

        plt.show()

    @staticmethod
    def plot_user_top_10_locations(fast_fetch=True, fast_fetch_threads=True):
        """
        Shows the distribution of user's locations.

        :param bool fast_fetch: Retrieves forums from a saved snapshot instantly
        :param fast_fetch_threads: Retrieves threads from a saved snapshot instantly
        """

        df = ForumScraper.scrap_threads_details(fast_fetch=fast_fetch, fast_fetch_threads=fast_fetch_threads)

        fig, ax = plt.subplots(figsize=(10, 9))

        df.drop_duplicates('user_name', inplace=True)

        identical_country_names = {'USA': 'United States', 'California': 'United States', 'US': 'United States',
                                   'Florida': 'United States', 'Texas': 'United States', 'New York': 'United States',
                                   'usa': 'United States', 'Arkansas': 'United States',
                                   'UK': 'England', 'uk': 'England', 'U.K': 'England', 'Scotland': 'England',
                                   'London': 'England', 'Manchester': 'England',
                                   }
        df.replace({"user_location": identical_country_names}, inplace=True)

        df = df.groupby('user_location')['user_location'].count().sort_values(ascending=False).head(10)

        df.plot(kind='pie', autopct='%1.1f%%', ax=ax)

        ax.set_ylabel('')

        fig.suptitle('Top 10 User\'s Locations', fontsize=20)

        plt.show()
