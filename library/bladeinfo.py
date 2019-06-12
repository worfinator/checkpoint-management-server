#!/usr/bin/python

import datetime
import sys
import json
import os
import shlex

from ansible.module_utils.basic import AnsibleModule

# arguments for the module:
fields = {
    "data": {
        "required": True,
        "type": "str"
    },
    "name": {
        "required": False,
        "type": "str"
    }
}

blades = {
    "app": 30,
    "ips": 1,
    "av": 30,
    "ab": 30
}

columns = "app_update_file,app_update_age,app_update_date,app_blade_status,ips_update_file,ips_update_age,ips_update_date,ips_blade_status,ab_update_file,ab_update_age,ab_update_data,ab_blade_status,av_update_file,av_update_age,av_update_date,av_blade_status"

module = AnsibleModule(argument_spec=fields, supports_check_mode=True)

def getTaskHost():
    task_data = module.params["name"].split(' - ')
    return task_data[0]

def getColumns():
    return columns.split(',')

def convert2object():
    column_names = getColumns()
    column_data = module.params["data"].split('|')
    
    i = 0
    my_data = {}
    my_data['host'] = getTaskHost()
    my_data['data_exists'] = True
    
    for column in column_names:
        my_data[column.lstrip(' ')] = column_data[i]
        i = i + 1
   
    return my_data

def checkBlades(_blade_data):
    passed = True
    message = ''
    
    for key, value in blades.iteritems():
        msg = ''

        # Catch the CP-TE instances
        if key == 'ips' and _blade_data['host'].find('CP-TE-'):
            _blade_data[key] = 'Ok'
        
        # Catch the disabled blades with no updates
        elif _blade_data[key + '_update_file'] == 'N/A' and _blade_data[key + '_blade_status'] == 'disabled':
            _blade_data[key] = 'Ok'
        
        # Now deal with the real cases
        else:
            
            # check enabled blades
            if _blade_data[key + '_blade_status'] == 'enabled':

                if _blade_data[key + '_update_age'] > value:
                    _blade_data[key] = 'Failed'
                    msg += key + ' blade update file is out of date ('+ _blade_data[key + '_update_age'] + ' days old)'
            
            else:
                _blade_data[key] = 'Failed'

                msg += key + ' blade is disabled '

                if _blade_data[key + '_update_age'] > value:
                    msg += ' and update file is out of date ('+ _blade_data[key + '_update_age'] + ' days old)'

        if len(msg):
            msg += '\n'

        # Make sure all blades have passed
        if _blade_data[key] == 'Failed':
            passed = False

    _blade_data['passed'] = passed
    _blade_data['message'] = msg
    
    return _blade_data

def main():
    # Convert string to object
    bladedata = convert2object()
    
    # perform checks
    bladedata = checkBlades(bladedata)
    
    module.exit_json(changed=False,
                     results=bladedata)


if __name__ == '__main__':
    main()
