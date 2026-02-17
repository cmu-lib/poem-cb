---
layout: null
permalink: /api/keyword
---
{% assign kw_param = page.k %}
{% assign keyword = site.data['poem-keywords'] | where: 'title', kw_param | first %}
