<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">

    <head>
        <title>Información sobre museos</title>
        <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
        <link rel="stylesheet" type="text/css" href="static/style/style.css" />
        <style>
            * {
                padding: 0;
                margin: 0;
            }

            a, input[type=submit] {
                width: 260px;
                color: white;
                height: 30px;
                border-radius: 8px;
                background: #A55BBE;
                text-decoration: none;
                text-align: center;
                margin-top: 4%;

                 /* Para centrar el texto */
                display: flex;
                justify-content: center;
                align-items: center;
            }

            h1 {
                text-align: center;
            }

            form {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                align-items: center;
            }

            .seleccion_museo {
                padding-top: 20px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
        </style>
    
    </head>
  
    <body>
        <div class="seleccion_museo">
            <h1> CONSULTAR DESCRIPCION DE UN EDIFICIO </h1>
            <form method="post" action="/mostrar_museo_seleccionado">
                <select name="museo">
                    % i = 1
                    % for edificio in edificios:
                        <option value="{{i}}">{{edificio.nombre}}</option> 
                        % i += 1
                    % end
                </select>
                <input value="Enviar" type="submit"/>
            </form>
            <a href="/">Volver</a>
        </div>
    </body>
</html>