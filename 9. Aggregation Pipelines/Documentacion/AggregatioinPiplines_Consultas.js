/**
 * Consultas práctica 9 Aggregation Piplines GIW.
 */

//Aggregation 1
db.getCollection('usuarios').aggregate([
   
    {$group: {
        _id: "$pais",
        count: {$sum: "?"}}
    },
    {$project: {
        _id: 0,
        pais: "$_id",
        total_usuarios: "$count"}
    }
]);


//Aggregation 2
db.getCollection('pedidos').aggregate([

   {$unwind: "$lineas"},
   {$match: {"lineas.precio": {$gte: "?"}}},
   {$group: {
       _id: "$lineas.nombre",
       num_uni: {$sum: "$lineas.cantidad"}
   }},
   {$project: {
       _id: 0,
       nombre_producto: "$_id",
       numero_unidades: "$num_uni",
       precio_unitario: "$lineas.precio"
   }}
]);


//Aggregation 3
db.getCollection('usuarios').aggregate([

    {$group: {
        _id: "$pais",
        count: {$sum: 1},
        max_age: {$max: "$edad"},
        min_age: {$min: "$edad"}
    }},
    {$match: {count: {$gt: "?"}}},
    {$project: {
        _id: 0,
        pais: "$_id",
        rango_edades: {$subtract: ["$max_age", "$min_age"]}
    }}
]);


//Aggregation 4
db.getCollection('pedidos').aggregate([

   {$lookup: {
       from: "usuarios",
       localField: "cliente",
       foreignField: "_id",
       as: "usuarios"}
   },
   {$group: {
       _id: "$usuarios.pais",
       lp: {$avg: {$size: "$lineas"}}}
   },
   {$project: {
       _id: 0,
       pais: "$_id",
       promedio_lineas_pedidos: "$lp"}
   }
]);


//Aggregation 5
db.getCollection('pedidos').aggregate([
   
    {$lookup: {
       from: "usuarios",
       localField: "cliente",
       foreignField: "_id",
       as: "usuarios"}
   },
   {$group: {
       _id: "$usuarios.pais",
       gasto: {$sum: "$total"}}
   },
   {$match: {_id: "?"}},
   {$project: {
       _id: 0,
       pais: "$_id",
       gasto_total: "$gasto"}
   }
]);