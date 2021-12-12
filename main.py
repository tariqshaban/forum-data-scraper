from providers.plots_provider import PlotsProvider

print('Scraping....')
print('--------------------------------------------------')

# Fetches from threads
PlotsProvider.plot_threads_posting()
PlotsProvider.plot_views_with_replies()
PlotsProvider.plot_view_with_replies_relation()
PlotsProvider.plot_top_15_thread_creators()
PlotsProvider.plot_top_15_oldest_threads()
PlotsProvider.plot_locked_sticky_threads()

# Fetches from thread's details
PlotsProvider.plot_replies()
PlotsProvider.plot_top_15_repliers()
PlotsProvider.plot_top_15_messages()
PlotsProvider.plot_user_titles()
PlotsProvider.plot_user_banners()
PlotsProvider.plot_users_joining()
PlotsProvider.plot_user_top_10_locations()

print('--------------------------------------------------')
print('Done.')
