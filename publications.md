---
layout: page
title: publications
permalink: /publications/
---

<p class="publications-intro">Des poèmes et des récits à lire librement.</p>

{% assign creation_cats = site.data.categories | where: "kind", "creation" %}
{% assign has_creations = false %}

{% for cat in creation_cats %}
  {% assign posts_in_cat = site.categories[cat.slug] %}
  {% if posts_in_cat and posts_in_cat.size > 0 %}
    {% assign has_creations = true %}
    <h2 class="year-heading">{{ cat.name }}</h2>
    <ul class="list-posts list-posts--creations">
      {% assign sorted_posts = posts_in_cat | sort: "date" | reverse %}
      {% for post in sorted_posts %}
        {% assign date_english = post.date | date: "%d %B %Y" %}
        {% include date-french.html %}
        <li class="post-teaser post-teaser--creation">
          <a href="{{ post.url | prepend: site.baseurl }}">
            <span class="post-teaser__title">{{ post.title }}</span>
            <span class="post-teaser__date">{{ date_french }}</span>
          </a>
        </li>
      {% endfor %}
    </ul>
  {% endif %}
{% endfor %}

{% unless has_creations %}
<p class="empty-message">Les premiers poèmes et récits s'en viennent.</p>
{% endunless %}
