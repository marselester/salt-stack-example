development:
  '*':
    - user
    - website.static_files
    - website.webserver

production:
  '*':
    - user
    - website.static_files
    - website.webserver
