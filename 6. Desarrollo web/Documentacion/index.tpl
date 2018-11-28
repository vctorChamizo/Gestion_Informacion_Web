% include('header.tpl', title='Temperaturas')
<h1>Municipios de Madrid</h1>
	<ul>
	% for m in mun:
		<li><a href="/{{m.attrib["value"][-5:]}}/{{m.text}}">{{m.text}}</a></li>
	%end
	</ul>
% include('footer.tpl')