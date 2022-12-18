from django_cron import CronJobBase, Schedule


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # every 1 hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Recommend.views.cached_user'    # a unique code

