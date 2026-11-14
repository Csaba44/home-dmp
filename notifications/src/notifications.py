from config import cfg, save
from notification_lib.print_finished import on_progress_change

NOTIFICATIONS = {
    "print_finished": (f"{cfg.mqtt_topic}/print_info", on_progress_change),
}

for name in NOTIFICATIONS:
    cfg.notifications.setdefault(name, True)
save(cfg)
