import django.dispatch

# Envoyé depuis authens.backends.ENSCASBackend
# Doc dans le README.
post_cas_connect = django.dispatch.Signal()
