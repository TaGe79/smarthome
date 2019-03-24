import asyncio
import logging

import voluptuous as vol

from homeassistant.const import (
    CONF_ENTITY_ID, 
    CONF_SWITCHES,
    CONF_OFFSET,
    CONF_NAME,
    STATE_OFF,
    STATE_ON,
    STATE_UNKNOWN,
    STATE_OPENING,
    STATE_CLOSING)
from homeassistant.core import callback
from homeassistant.helpers.config_validation import (  # noqa
    PLATFORM_SCHEMA, PLATFORM_SCHEMA_BASE)
from homeassistant.helpers.event import async_track_state_change
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.restore_state import RestoreEntity

_LOGGER = logging.getLogger(__name__)

DOMAIN = "shutter"
PLATFORM_NAME="statefullshutter"


DEFAULT_NAME="Smart Shutter"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_ENTITY_ID): cv.entity_id,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_SWITCHES): cv.entities_domain('switch'),
})

ENTITY_ID_FORMAT = DOMAIN + '.{}'

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """ Set up shutter!"""  
    await async_add_entities([StatefullShutter(hass,config)])

class StatefullShutter(RestoreEntity):
    def __init__(self, hass, config):
        """Initialize a shutter."""
        super().__init__()
        self.hass = hass
        self._name = config.get(CONF_NAME)
        self.entity_id = config.get(CONF_ENTITY_ID)
        self._up_switch = config.get(CONF_SWITCHES)[0]
        self._down_switch = config.get(CONF_SWITCHES)[1]
        _LOGGER.info("Shutter instantiated")

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()
    
        last_state = await self.async_get_last_state()

        if last_state is not None:
            if 'offset' in last_state.attributes:
                self._offset = last_state.attributes['offset']
            self.state = last_state    

            if self._up_switch:
                async_track_state_change(self.hass, self._up_switch, self._async_up_switch_changed)

            if self._down_switch:
                async_track_state_change(self.hass, self._down_switch, self._async_down_switch_changed)
        _LOGGER.info("Added to hass")

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self.entity_id
    
    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def open(self):
        return run_coroutine_threadsafe( self.async_open(), self.hass.loop).result()

    def close(self):
        return  run_coroutine_threadsafe( self.async_close(), self.hass.loop).result()

    def stop(self):
        return  run_coroutine_threadsafe(
            self.async_stop(), self.hass.loop).result()

    def move_to(self, offset):
        return run_coroutine_threadsafe( self.async_move_to(offset), self.hass.loop).result()

    async def async_open(self):
        _LOGGER.info("Opening shutter ["+self.entity_id+"]")

    async def async_close(self):
        _LOGGER.info("Closing shutter ["+self.entity_id+"]")

    async def async_stop(self):
        _LOGGER.info("Stop shutter ["+self.entity_id+"]")

    async def async_move_to(self, offset):
        _LOGGER.info("Move shutter from ."+self._offset+" to ."+offset)

    async def _async_up_switch_changed(self, entity_id, old_state, new_state):
        """Handle power sensor changes."""
        if new_state is None:
            return

        if new_state.state == STATE_ON:
            self._moving = True
            self._state = STATE_OPENING

        if new_state.state == STATE_OFF:
            self._movig = False
            self._state = STATE_OFF

        await self.async_update_ha_state()

    async def _async_down_switch_changed(self, entity_id, old_state, new_state):
        """Handle power sensor changes."""
        if new_state is None:
            return

        if new_state.state == STATE_ON:
            self._moving = True
            self._state = STATE_CLOSING

        if new_state.state == STATE_OFF:
            self._movig = False
            self._state = STATE_OFF

        await self.async_update_ha_state()   
