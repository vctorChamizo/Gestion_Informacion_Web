
<!-- 
ASIGNATURA : GESTIÓN DE INFORMACIÓN EN LA WEB
PRÁCTICA Aggregation Pipelines
GRUPO 10
AUTORES: Victor Chamizo Rodriguez, Pablo García Hernandez, Fernando López Carrión, Irene Martín Berlanga y Sergio Martín Gómez

Victor Chamizo Rodriguez, Pablo García Hernandez, Fernando López Carrión, Irene Martín Berlanga y Sergio Martín Gómez declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

-->

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">

    <head>
        <title>Resultado consulta</title>
        <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
        
        <style>
            * {
                padding: 0;
                margin: 0;
            }

            table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }

            td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }

            tr:nth-child(even) {
                background-color: #dddddd;
            }

            ul {
                list-style-type: none;
            }
            
        </style>
    
    </head>
  
    <body>

    <div class="contenedor">
        
        <table>
            <tr>
                <th>Producto</th>
                <th>Unidades vendidas</th>
                <th>Precio unitario</th>
            </tr>

            % for producto in resultadoQuery:
                <tr>
                    <td>{{producto['_id']}}</td>
                    <td>{{producto['numeroDeUnidadesVendidas']}}</td>
                    <td>{{producto['precioUnitario']}}</td>
                </tr>
            % end 
        </table>

        <h3>La búsqueda ha devuelto {{numeroDeDocumentos}} documentos.</h3>
        </div>
    </body>
</html>