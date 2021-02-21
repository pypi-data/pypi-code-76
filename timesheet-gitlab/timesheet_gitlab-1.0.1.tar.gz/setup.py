from setuptools import setup

setup(name='timesheet_gitlab',
      version='1.0.1',
      description='produce timesheets using activity data from GitLab API calls',
      url='https://gitlab.com/oliversmart/timesheet_gitlab',
      author='Oliver Smart',
      author_email='oliver.s.smart@gmail.com',
      license='Apache License 2.0.',
      python_requires='>=3.6',
      packages=['timesheet_gitlab'],
      scripts=['bin/timesheet_gitlab'],
      zip_safe=False,
      include_package_data=True,
      install_requires=['python-gitlab', 'grip']
      )
