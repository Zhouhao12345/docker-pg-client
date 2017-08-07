    DELETE FROM fetchmail_server;

    DELETE FROM ir_mail_server;

    UPDATE ir_cron SET active = FALSE;

    DELETE FROM ir_config_parameter WHERE key = 'dead_mans_switch_client.url';

    UPDATE ir_config_parameter SET value = md5(random()::text || clock_timestamp()::text)::uuid WHERE key = 'database.uuid';

    DELETE FROM ir_config_parameter WHERE key IN ('database.enterprise_code', 'database.expiration_date', 'database.expiration_reason');
