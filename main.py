import datetime

import pandas as pd

from providers.plots_provider import PlotsProvider
from providers.forum_scraper import ForumScraper

print('Scraping....')
print('--------------------------------------------------')
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

ForumScraper.scrap_threads(fast_fetch=True)
df = ForumScraper.cache_threads_details()

print(df)

# ForumScraper.scrap_threads(fast_fetch=True)
# ForumScraper.cache_threads_details()
# print(ForumScraper.scrap_threads_details(fast_fetch=True))
PlotsProvider.plot_views_with_replies()
print('--------------------------------------------------')
print('Done.')
