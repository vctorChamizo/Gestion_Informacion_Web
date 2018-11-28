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

            input[type=text] {
                margin-top: 5%;
                height: 30px;
                width: 220px;
                background: rgba(116, 111, 111, 0.6);
                border: none;
                text-indent: 3%;
            }

            input[type=text]:focus { /* Cambiar el color de resaltado al pulsar en un input */
                outline: 2px solid #A55BBE;         
            }

            ::placeholder {
                color: rgb(0, 0, 0);
            }

            form {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                align-items: center;
            }

            .contenedor {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
        </style>
    
    </head>
  
    <body>
        <div class="contenedor">
            <h1> CONSULTAR MUSEOS MAS CERCANOS  </h1>
                <form method="post" action="/mostrar_edificios_cercanos">
                    <input name="calle" placeholder="Calle" type="text"/>
                    <input name="numero" placeholder="Numero" type="text"/>
                    <input name="distancia" placeholder="Distancia en km" type="text"/>
                    <input value="Enviar" type="submit"/>
                </form>

                <a href="/">Volver</a>

            </div>
        
    </body>
</html>