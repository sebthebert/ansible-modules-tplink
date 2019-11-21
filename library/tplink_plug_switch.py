#!/usr/bin/python
# Copyright (c) 2019 Sebastien Thebert

"""tplink_plug_switch Ansible module."""

from ansible.module_utils.basic import AnsibleModule

#from module_utils.tplink_plug import tplink_plug_get_state
try:
    from library.module_utils.tplink_plug import tplink_plug_get_state, tplink_plug_set_state
except ImportError:
    from ansible.module_utils.tplink_plug import tplink_plug_get_state, tplink_plug_set_state

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: tplink_plug_switch

author:
    - Sebastien Thebert (sebthebert@gmail.com)
'''

AVAILABLE_PORT = range(1, 65535)
AVAILABLE_STATE = ['on', 'off']

def main():
	"""tplink_plug_switch main() function."""
	
	module_args = dict(
		ip=dict(type='str', required=True),
		port=dict(type='int', required=False),
		state=dict(type='str', required=True)
    )
	module = AnsibleModule(
		argument_spec=module_args,
		supports_check_mode=True
	)
	result = dict(
		changed=False
	)

	# Validate module parameters
	if module.params['port'] not in AVAILABLE_PORT:
		module.fail_json(msg="Invalid 'port' value", **result)
	if module.params['state'].lower() not in AVAILABLE_STATE:
		module.fail_json(msg="Invalid 'state' value", **result)

	new_state = 0
	if module.params['state'].lower() == 'on':
		new_state = 1

	old_state = tplink_plug_get_state(module.params['ip'], module.params['port'])
	if new_state != old_state:
		result['changed'] = True
	
	if result['changed'] is True and module.check_mode is False:
		tplink_plug_set_state(module.params['ip'], module.params['port'], new_state)

	module.exit_json(**result)

if __name__ == '__main__':
	main()