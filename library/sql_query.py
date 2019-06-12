#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None


def main():
    module = AnsibleModule(
        argument_spec=dict(
            connection=dict(required=True),
            query=dict(required=True),
            rows_are_lists=dict(type='bool', default=False)
        ),
        supports_check_mode=True,
    )

    if sqlalchemy is None:
        module.fail_json(msg='sqlalchemy module is not available')

    engine = sqlalchemy.create_engine(module.params['connection'])

    try:
        res = engine.execute(module.params['query'])
    except sqlalchemy.exc.SQLAlchemyError as err:
        module.fail_json(msg="query resulted in an error: %s" % err)

    if module.params.get('rows_are_lists', False):
        data = lambda: res.fetchall()
    else:
        data = lambda: [dict(row) for row in res.fetchall()]

    module.exit_json(changed=False,
                     results=data())


if __name__ == '__main__':
    main()
