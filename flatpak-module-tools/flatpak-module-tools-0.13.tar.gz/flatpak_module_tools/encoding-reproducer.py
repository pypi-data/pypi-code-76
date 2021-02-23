import koji

options = koji.read_config(profile_name='koji')
session_opts = koji.grab_session_options(options)
session = koji.ClientSession(options['server'], session_opts)

session.CGImport({'a': 'Hydrogen est une boîte à rythme.'}, 'foo')
