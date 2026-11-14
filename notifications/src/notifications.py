from config import cfg
from notification_lib.print_finished import on_progress_change

NOTIFICATIONS = {
    f"{cfg.mqtt_topic}/print_info": on_progress_change,
}
