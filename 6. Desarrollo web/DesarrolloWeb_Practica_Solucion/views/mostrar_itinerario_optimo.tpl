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

            a {
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

            .contenedor {
                display: flex;
                flex-direction: column;
                align-items: center;
                
            }
        </style>
    
    </head>
  
    <body>
        <div class="contenedor">
            <ul style="list-style-type:disc; padding-left: 30px">
                <li>Fecha: {{ruta.fecha}}</li>
                <li>Hora de inicio: {{ruta.horaInicio}}</li>
                <li>Hora estimada de llegada: {{ruta.horaEstimadaLlegada}}</li>
                <li>Numero de trasbordos: {{ruta.numeroDeTrasbordos}}</li>
                <li>Duracion del viaje: {{ruta.duracion}}</li>
                <li>Descripcion textal de la ruta: 
                    <ul style="list-style-type:disc; padding-left: 30px">
                    % for seccion in ruta.descripcionTextual:
                        <li> {{seccion}} </li>
                    % end
                    </ul>
                </li>
            </ul> 

            <a href="/">Volver</a>

        </div>
        
    </body>
</html>