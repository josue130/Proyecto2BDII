const express = require('express');
const app = express();


// Se utiliza para obtener valores de la página
app.use(express.urlencoded({extends:false}));
app.use(express.json());

// Variables de entorno
const dotenv = require('dotenv');
dotenv.config({path:'./env/.env'})
var connection = require('./Database/db');
app.use('/resources', express.static('public'));
app.use('/resources', express.static(__dirname + '/public'));

// Establecer el motor de plantillas
app.set('view engine', 'ejs');
let prueba = [];


app.get('/main', (req, res) => {
    let resultados = []
    let resultados2 = []
    res.render('main',{resultados:resultados,resultados2:resultados2});
})
app.get('/all',(req, res)=>{
    let all = [];
    let all2 = [];
    connection.query('SELECT * from Apartado2A',async(error,results)=> {
        if (error){
            consoloe.log(error);
        }
        else{
            all = results;
        }
    })
    connection.query('SELECT * from Apartado2C',async(error,results)=> {
        if (error){
            consoloe.log(error);
        }
        else{
            all2 = results;
            res.render('all',{all:all,all2:all2});
            res.end();
        }
    })

    
})

app.post('/busqueda',async(req, res) =>{
    let palabra = req.body.busqueda;
   
    
    let resultados = [];
    let resultados2 = []

    console.log(palabra);
    connection.query('SELECT palabra,PorcentajeH1, PorcentajeSubH2,PorcentajeSubH3,parrafo FROM Apartado2C WHERE palabra = ? ',[palabra], async(error,results)=> {
        if (error){
            console.log(error);
        }
        else{
            resultados2 = results;
            console.log(resultados2)

                
            }
        })
    
    connection.query('SELECT pagina,palabra FROM Apartado2A WHERE palabra = ?',[palabra], async(error,results)=> {
        if (error){
            console.log(error);
        }
        else{
            resultados = results;
            res.render('main',{resultados:resultados,resultados2:resultados2})
            res.end()
                
            }
        })
    
})

app.listen(3000,(req, res) =>{
    console.log('SERVER RUNNIG IN http://localhost:3000');
})