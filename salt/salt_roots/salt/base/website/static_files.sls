directory served by nginx:
  file:
    - directory
    - name: {{ pillar['website_static_dir'] }}
    - user: simon
    - group: simon

index file:
  file:
    - managed
    - name: {{ pillar['website_static_dir'] }}/index.html
    - source: salt://website/index.html
    - user: simon
    - group: simon
    - require:
      - file: directory served by nginx

background image:
  file:
    - managed
    - name: {{ pillar['website_static_dir'] }}/bg.gif
    - source: salt://website/bg.gif
    - user: simon
    - group: simon
    - require:
      - file: directory served by nginx
