<h1> Libros que se encuentran en la libreria </h1>
<table>
<tr> <th> Item </th><th> Cantidad </th></tr>
%for row in rows: 
    <tr>
    %for col in row:
        <td> {{col}}</td>
    %end
    </tr>
%end
</table>