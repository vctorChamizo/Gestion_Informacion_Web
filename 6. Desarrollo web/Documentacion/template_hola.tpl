<!DOCTYPE html>
<html lang="es">
<head>
<title>Bienvenido {{nombre}}</title>
<meta charset="utf-8" />
</head>
 
<body>
    <header>
       <h1>Este es mi sitio web</h1>
       <p>Esta creado con tecnología bottle</p>
    </header>
    <h2>Bienvenido</h2>
    % if nombre=="Mundo":
      <p> Hola <strong>{{nombre}}</strong></p>
    %else:
      <h1>Hola {{nombre.title()}}!</h1>
      <p>¿Cómo estás?
    %end
</body>
</html>