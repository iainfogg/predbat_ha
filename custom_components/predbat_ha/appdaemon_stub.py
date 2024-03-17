"""appdaemon_stub module.

The appdaemon_stub module is designed to provide the same API to Predbat
as AppDaemon offered, and to return the same values.

The motivation has been to allow, as far as possible, the existing Predbat
code to run with either AppDaemon or as part of a HA integration.
"""

from functools import wraps, partial
from datetime import datetime, timedelta, timezone
import logging
from typing import Any
from collections.abc import Callable
from time import sleep

from homeassistant.core import HomeAssistant, State
from homeassistant.components.recorder import history
from homeassistant.helpers import entity_registry, event

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class AppDaemonHassApiStub:
    """This provides the AppDaemonHassApi methods that Predbat relies on."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialise the class, setting properties that AppDaemon would have offered that Predbat relies on."""

        self.args = {
            "prefix": "predbat",
        }
        self.hass = hass

    def log(self, msg: str, *args, **kwargs):
        """Provide logging"""
        # Figure out logging level from string content
        level = logging.INFO
        if (msg.lower().find('warn:') != -1):
            level = logging.WARNING
        if (msg.lower().find('error:') != -1):
            level = logging.ERROR

        _LOGGER.log(level, msg, *args, **kwargs)

    def set_state(self, entity_id: str, **kwargs: Any | None):
        """Set the state of an entity"""
        # Rename state key to suit HA set state method
        kwargs['new_state'] = kwargs.pop('state')


        # Trim state to 255 chars, errors if longer than that
        # TODO: Figure out which entity this is for
        if isinstance(kwargs['new_state'], State):
            kwargs['new_state'] = kwargs['new_state'].state

        # self.log(f"State is {kwargs['new_state']}")
        # self.log(f"Entity is {entity_id}")
        # self.log(f"Entity type is {type(kwargs['new_state'])}")

        # self.log("State value being set; entity {} state value {}".format(entity_id, kwargs['new_state']))
        # if isinstance(kwargs['new_state'], str) and len(kwargs['new_state']) > 255:
        #     self.log("WARN: State value longer than allowed 255; entity {} state value {}".format(entity_id, kwargs['new_state']))

        # TODO: Look into creating the device if it doesn't exist,
        # so that it can be created and attached to the Predbat device,
        # rather than just being a helper entity floating around by itself
        # self.hass.states.async_set(entity_id = entity_id, **kwargs)
        # entity_registry.async_resolve_entity_id(entity_id)

        # resolve_kwargs = {}
        # resolve_kwargs['registry'] = entity_registry.async_get(self.hass)
        # resolve_kwargs['entity_id_or_uuid'] = entity_id

        entity_registry_instance = self._call_async_method(
            entity_registry.async_get, self.hass
        )
        entity_is_registered = self._call_async_method(
            entity_registry_instance.async_is_registered, entity_id
        )
        if not entity_is_registered:
            self.log(f"Trace: entity {entity_id} is not in the entity registry and should be added")
        else:
            self.log(f"Trace: entity {entity_id} is in the entity registry")

        kwargs['entity_id'] = entity_id

        self.hass.states.async_set(**kwargs)

    def create_and_set_state(self, entity_id: str, **kwargs: Any | None):
        """
        This method's use is debatable, but for now it's aiming to allow
        Predbat to create entities and save their initial state.

        However, I suspect that entity creation will have to be restricted to the
        various platforms on boot-up, rather than being done dynamically.

        That's because entities created in the way they're done in this method
        are created in the entity registry, but can't handle having their state
        modified - they're orphaned from any entity code needed to handle the state.
        """
        entity_registry_instance: entity_registry.EntityRegistry = self._call_async_method(
            entity_registry.async_get, self.hass
        )
        entity_is_registered = self._call_async_method(
            entity_registry_instance.async_is_registered, entity_id
        )
        if not entity_is_registered:
            self.log(f"Trace: entity {entity_id} is not in the entity registry and should be added")
            # TODO Actually get it from the registry instead of hard-coding it!
            device_id = '96ff19b4e856c2c7be97b128364a2f94'
            type, split_entity = entity_id.split('.')

            func_partial = partial(
                entity_registry_instance.async_get_or_create,
                type,
                DOMAIN,
                split_entity,
                config_entry = self.hass.data[DOMAIN]['controller'].config_entry,
                device_id = device_id,
                suggested_object_id = split_entity,
            )
            self._call_async_method(
                func_partial
            )
        else:
            self.log(f"Trace: entity {entity_id} is in the entity registry")

        # modified_args = kwargs
        # modified_args.pop('type')

        # modified_args['entity_id'] = entity_id

        self.set_state(entity_id, **kwargs)

    def get_state(
        self,
        entity_id: str = None,
        attribute: str = None,
        default: Any = None,
        copy: bool = True,
        **kwargs: Any | None,
    ) -> Any:
        """Get state of all or single entity/entities"""

        if entity_id is None:
            states = {}
            # for entity in self.hass.states.async_all():
            for entity in self.hass.states.all():
                states[entity.entity_id] = self._get_state_as_dict(entity)

            # TODO: Should this return a state object, or the state from the object?
            return states

        # TODO: Should this return a state object, or the state from the object?
        # TODO: Add support for attributes and default
        # TODO: Should we be getting state via a helper rather than straight from the states dict?
        return self._get_state_as_dict(self.hass.states.get(entity_id = entity_id, **kwargs), attribute = attribute, default = default)

    def _get_state_as_dict(self, stateObject,
            entity_id: str = None,
            attribute: str = None,
            default: Any = None,
            copy: bool = True,
            **kwargs: Any | None,
    ):
        # self.log("Trace: _get_state_as_dict - attribute {} default {} state object {}".format(attribute, default, stateObject))
        if isinstance(stateObject, State):
            stateObjectAsDict = stateObject.as_dict()
            stateValue = default

            if attribute:
                if "attributes" in stateObjectAsDict and attribute in stateObjectAsDict["attributes"]:
                    stateValue = stateObjectAsDict["attributes"][attribute]
                else:
                    stateValue = None
            else:
                stateValue = stateObjectAsDict["state"]
            # stateValue = stateObject.as_dict()["state"]
            # self.log("Trace: _get_state_as_dict - State object found, will return {}".format(stateValue))
            return stateValue

        return default

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

        # Convert state objects to dictionary objects, so that the
        # legacy Predbat can run without modification
        entityHistoryValues = historyValues.get(entity_id, None)
        convertedEntityHistoryValues = []
        if entityHistoryValues is None:
            return None

        for stateObject in entityHistoryValues:
            convertedEntityHistoryValues.append(stateObject.as_dict())


        # Return within a list, to reflect the values the legacy Predbat code
        # expected to get from AppDaemon
        convertedEntityHistoryValues = [convertedEntityHistoryValues]

        # self.log("warn: getting history - entity_ids: {} - convertedEntityHistoryValues: {}".format(entity_ids, convertedEntityHistoryValues[0] if entity_id != 'update.predbat_version' else 'redacted due to length'))
        return convertedEntityHistoryValues

    def _call_async_method(self, method: Callable, *args):
        future = self.hass.async_add_executor_job(
            method, *args
        )
        return self.__wait_for_future(future)

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

    def listen_state(self, callback: Callable, entity_id: str):
        # self.hass.states.hel
        listener = event.track_state_change(self.hass, entity_id, callback)
        listener()

    def call_service(self, serviceId: str, **kwargs):
        # TODO test handling missing services e.g. if device to notify doesn't exist
        namespace, service = serviceId.split("/")
        self.log(f"Trace: Service call to namespace {namespace} service {service} (serviceId {serviceId})")
        if not namespace or not service:
            self.log(f"Warn: serviceId {serviceId} does not contain a namespace and service")
        self.hass.services.call(namespace, service, dict(kwargs))

    def run_every(self, callback: Callable, start: datetime, interval: int, **kwargs):
        pass

class AppDaemonAdStub:
    def __init__(self) -> None:
        pass

    def app_lock(f):
        """Synchronization decorator."""

        @wraps(f)
        def f_app_lock(*args, **kw):
            # self = args[0]

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
