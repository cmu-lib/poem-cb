---
layout: null
permalink: /api/related-kws
---
{% assign kw_param = page.k %}
{% assign kw_list = site.data['poem'] | where: 'keyword',  kw_param %}
