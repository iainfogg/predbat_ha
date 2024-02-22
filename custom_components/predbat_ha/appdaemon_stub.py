from functools import wraps
from datetime import datetime, timedelta, timezone
import logging
from typing import Any, Optional, Callable
from time import sleep

from homeassistant.core import HomeAssistant
from homeassistant.components.recorder import history
from homeassistant.helpers import entity_registry

_LOGGER = logging.getLogger(__name__)


class AppDaemonHassApiStub:
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

        # TODO: Look into creating the device if it doesn't exist,
        # so that it can be created and attached to the Predbat device,
        # rather than just being a helper entity floating around by itself
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

    def get_history(self, **kwargs):
        entity_id = kwargs.get('entity_id', None)
        entity_ids = [entity_id] if entity_id is not None else None
        # TODO: Actually read the days passed in, if they exist
        # (and figure out what to do if they're not passed in)
        start_time = (datetime.now(timezone.utc) - timedelta(days=10))

        recorder_instance = self.hass.components.recorder.get_instance(self.hass)

        future = recorder_instance.async_add_executor_job(
            history.get_significant_states, self.hass, start_time, None, entity_ids
        )

        historyValues = self.__wait_for_future(future)

        return historyValues.get(entity_id, None)

    def __wait_for_future(self, future):
        while not future.done():
            sleep(0.01)  # Optionally, yield control to the event loop

        return future.result()

    async def async_get_history(self, **kwargs):
        entity_id = kwargs.get('entity_id', None)
        entity_ids = [entity_id] if entity_id is not None else None
        start_time = (datetime.now(timezone.utc) - timedelta(days=10))

        # historyValues = await self.hass.async_add_executor_job(history.get_significant_states(
        #     self.hass,
        #     start_time,
        #     datetime.datetime.now(),
        #     entity_ids
        # ))

        historyValues = self.hass.components.recorder.get_instance(self.hass).async_add_executor_job(
            history.get_significant_states, self.hass, start_time, None, entity_ids
        )

        # coro = history.get_significant_states(
        #     self.hass,
        #     start_time,
        #     datetime.datetime.now(),
        #     entity_ids
        # )

        # historyValues = asyncio.run_coroutine_threadsafe(
        #     coro,
        #     self.hass.loop
        # ).result()

        # historyValues = self.hass.async_add_executor_job(
        #     history.get_significant_states, self.hass, start_time, None, entity_ids
        # )

        # historyValues = history.get_significant_states(
        #     self.hass,
        #     start_time,
        #     datetime.datetime.now(),
        #     entity_ids
        # )

        return historyValues

    def run_every(self, callback: Callable, start: datetime, interval: int, **kwargs):
        pass

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
