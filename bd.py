{% block body %}

    <div class="row marketing">
        <div class="col-lg-6">
            {% if session.logged_in %}
            <form action="{{ url_for('add_post') }}" method=post class=add-entry>
                    <dl>
                      <dt>Title:
                      <dd><input type=text size=30 name=title>
                      <dt>Text:
                      <dd><textarea name=text rows=5 cols=40></textarea>
                      <dd><input type=submit value=Share>
                    </dl>
                  </form>
            <h2>Sua linha do tempo Personalizada</h2><p>
            {% else %}
            <h2>Postagens Publicas</h2><p>
            {% endif %} 
            <ul class=entries>
            {% for entry in entries %}
            <li><h4> {{ entry[0] }} {{ entry[1] }} {{ entry[2] }} - {{ entry[3] }} {{ entry[4] }} </h4><b>{{ entry[6] }}</b>: {{ entry[5] |safe }}
            {% else %}
            <li><em>Não há postagens novas</em>
            {% endfor %}

            </ul> 
        </div>
        <div class="col-lg-6">
          blabla
        </div>

      </div>


    
{% endblock %}
