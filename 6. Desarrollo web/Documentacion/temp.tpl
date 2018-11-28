% include('header.tpl', title='Temperaturas '+name)
    <h1>{{name}}</h1>
		<p>Temperatura máxima:{{max}}ºC</p>
		<p>temperatura mínima:{{min}}ºC</p>
		<a href="..">Volver</a>
% include('footer.tpl')