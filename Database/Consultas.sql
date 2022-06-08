drop database if exists Consultas;
create database Consultas;
use Consultas;

create table if not exists Apartado1A(
	pagina varchar(300),
    CantidadTitulos int
);
create table Apartado_C(
  titulo varchar(350),
  cantidad_links int,
    cantidad_links_activos int
);


create table Apartado_D(
  titulo varchar(350),
  numero_link int,
    cantidad_veces_link int
);
create table if not exists Apartado1B(
	pagina varchar(300),
    PalabrasDistintas int
);

create table if not exists Apartado1E(
	pagina varchar(300),
    CantidadAlt int,
    PalabrasDistintas int

);
create table if not exists Apartado1F(
	pagina varchar(300),
    PalabraComun varchar(100),
    Aparece varchar(100)
);

create table if not exists Apartado2A(
	pagina varchar(300),
    palabra varchar(100),
    cantidad int
    
	
);
create table if not exists Apartado2B(
	pagina varchar(300),
    palabra varchar(100),
    porcentaje float
    
	
);
create table if not exists Apartado2C(
	palabra varchar(100),
    PorcentajeH1 float,
    PorcentajeSubH2 float,
    PorcentajeSubH3 float,
    parrafo float,
    PorcentajeLI float
);


select * from Apartado1A; 
select * from Apartado1F;
select * from Apartado1B;
select * from Apartado1E;
select * from Apartado2C;
select * from Apartado2B;
select * from Apartado2A;