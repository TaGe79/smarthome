
"""
import os.path
import time

"""

entity_id = data.get('entity_id')
shutter_target_pos = data.get('shutter_target_pos')

shutter_switch_up = data.get('shutter_up')
shutter_switch_down = data.get('shutter_down')
shutter_state_input = data.get('shutter_state')

lock_file_name='.shutter_'+entity_id+'_lock'
state_file_name= '.shutter_'+entity_id+'_state.txt'

logger.info("SHUTTER")

if os.path.isfile(lock_file_name) == False: 
    lock_file=open(lock_file_name, 'w')
    lock_file.write('.')
    loc_file.close();
    
    if os.path.isfile(state_file_name):
        state_file = open(state_file_name, 'r')
        shutter_pos = int(state_file.read())
        state_file.close()
    else:
        shutter_pos=0
    
    shutter_move=abs(shutter_target_pos-shutter_pos)
    
    homeassistant.core.set(shutter_state_input,shutter_target_pos)
    
    if shutter_target_pos < shutter_pos:
        hass.services.call('switch', 'turn_on', {'entity_id': shutter_switch_up}, False)
        hass.services.call('switch', 'turn_off', {'entity_id': shutter_switch_down}, False)
    else:
        hass.services.call('switch', 'turn_off', {'entity_id': shutter_switch_up}, False)
        hass.services.call('switch', 'turn_on', {'entity_id': shutter_switch_down}, False)
    
    time.sleep(shutter_move)
    
    hass.services.call('switch', 'turn_off', {'entity_id': shutter_switch_up}, False)
    hass.services.call('switch', 'turn_off', {'entity_id': shutter_switch_down}, False)
    
    state_file = open(state_file_name, 'w')
    state_file.write(shutter_target_pos)
    state_file.close()
    
    os.remove(lock_file_name)
