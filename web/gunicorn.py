secure_scheme_headers = {
    'X_FORWARDED_PROTOCOL': 'ssl',
    'X_FORWARDED_PROTO': 'https',
    'X_FORWARDED_SSL': 'on'
}
bind = '0.0.0.0:8080'
errorlog = '-'
loglevel = 'info'
