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

            .servicios {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
        </style>
    
    </head>
  
    <body>
        
        <div class="servicios">
            <h1>INFORMACION SOBRE MUSEOS</h1>
            <a href="/mostrar_museos" >Mostrar informacion sobre un museo</a>
            <a href="/obtener_datos_calculo_itinerario" >Obtener itinerario óptimo</a>
            <a href="/obtener_datos_museos_cercanos" >Museos más cercanos</a>
        </div>
        
    </body>
</html>