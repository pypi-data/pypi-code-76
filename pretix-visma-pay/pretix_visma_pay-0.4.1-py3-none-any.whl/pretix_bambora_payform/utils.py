from pretix.base.settings import GlobalSettingsObject

def get_credentials(event):
    gs = GlobalSettingsObject()
    api_key_setting = 'payment_bambora_payform_test_api_key' if event.testmode else 'payment_bambora_payform_api_key'
    private_key_setting = 'payment_bambora_payform_test_private_key' if event.testmode else 'payment_bambora_payform_private_key'

    return {
        'api_key': gs.settings.get(api_key_setting),
        'private_key': gs.settings.get(private_key_setting)
    }
