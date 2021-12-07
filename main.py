import datetime

import pandas as pd

from providers.plots_provider import PlotsProvider
from providers.forum_scraper import ForumScraper

print('Scraping....')
print('--------------------------------------------------')
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# df = ForumScraper.scrap_threads(fast_fetch=True)
#
# print(df)

# ForumScraper.scrap_threads(fast_fetch=True)
# ForumScraper.cache_threads_details()
# print(ForumScraper.scrap_threads_details(fast_fetch=True))
PlotsProvider.plot_user_top_10_locations()
print('--------------------------------------------------')
print('Done.')
