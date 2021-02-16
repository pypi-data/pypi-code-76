from magicapi import g

# email_body = f'<html><a href="<LINK>" target=“_blank”>Click here to sign in to {g.settings.company_name}.</a></html>'

email_body = '''
<html>
  Hello,
  <p>
    We received a request to sign in to <COMPANY_NAME> using this email address. If you want to sign in with your <EMAIL_ADDRESS> account, click this link:
  </p>
  <p>
    <a
    href="<LINK>"
    target="“_blank”"
    >Click here to sign in to <COMPANY_NAME>.</a
  >
  </p>
  <p>
      If you did not request this link, you can safely ignore this email.
  </p>
  <p>
      Thanks,
  </p>
  <p>
      Your <COMPANY_NAME> team
  </p>
</html>
'''

subject = f"Sign in to {g.settings.company_name}"


def make_template_and_subject(email_address: str, magic_link: str):
    new_body = email_body.replace("<LINK>", magic_link).replace(
        "<EMAIL_ADDRESS>", email_address
    ).replace('<COMPANY_NAME>', g.settings.company_name)
    return new_body, subject
