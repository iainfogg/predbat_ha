from functools import wraps
import logging
from typing import Any, Optional

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

class AppDaemonHassStub:
    def __init__(self, hass: HomeAssistant) -> None:
        self.args = {
            "prefix": "predbat",
        }
        self.hass = hass

    def log(self, msg: str, *args, **kwargs):
        # Figure out logging level from string content
        level = logging.INFO
        if (msg.lower().find('warn:') != -1):
            level = logging.WARNING
        if (msg.lower().find('error:') != -1):
            level = logging.ERROR

        _LOGGER.log(level, msg, *args, **kwargs)

    def set_state(self, entity_id: str, **kwargs: Optional[Any]):
        # Rename state key to suit HA set state method
        kwargs['new_state'] = kwargs.pop('state')
        self.hass.states.async_set(entity_id = entity_id, **kwargs)

    def get_state(
        self,
        entity_id: str = None,
        attribute: str = None,
        default: Any = None,
        copy: bool = True,
        **kwargs: Optional[Any],
    ) -> Any:
        """Get state of all or single entity/entities"""
        if entity_id is None:
            states = {}
            for entity in self.hass.states.async_all():
                states[entity.entity_id] = entity

            return states

        return self.hass.states.get(entity_id)


class AppDaemonAdStub:
    def __init__(self) -> None:
        pass

    def app_lock(f):
        """Synchronization decorator."""

        @wraps(f)
        def f_app_lock(*args, **kw):
            self = args[0]

            # self.lock.acquire()
            # try:
            return f(*args, **kw)
                # return f(*args, **kw)
            # finally:
                # self.lock.release()

        return f_app_lock


# ALL THESE THINGS ARE USED IN INVERTER FROM PREDBAT
# THEY ARE NOT THINGS USED FROM hassio.Hass
# ALL DONE IN ERROR
# log
# forecast_minutes
# get_arg()
# battery_capacity_nominal
# battery_scaling
# args
# battery_rate_max_scaling
# dp2()
# record_status()
# expose_config()
# set_reserve_enable
# entity_exists()
# sim_soc_kw
# sim_charge_start_time
# sim_charge_end_time
# inverter_clock_skew_start
# inverter_clock_skew_end
# time_abs_str
# inverter_clock_skew_discharge_start
# inverter_clock_skew_discharge_end
# sim_reserve
# get_entity()
# set_inverter_notify
# call_notify()
# time_now_str()
# record_status()
# sim_charge_rate_now
# sim_discharge_rate_now
# sim_soc
# sim_inverter_mode
# sim_discharge_start
# sim_discharge_end
# midnight_utc
# sim_charge_schedule_enable
# call_service()
