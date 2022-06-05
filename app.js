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

app.get('/main', (req, res) => {
    res.render('main');
})

app.post('/busqueda',async(req, res) =>{
    const palabra = req.body.busqueda;
    console.log(palabra);
})

app.listen(3000,(req, res) =>{
    console.log('SERVER RUNNIG IN http://localhost:3000');
})