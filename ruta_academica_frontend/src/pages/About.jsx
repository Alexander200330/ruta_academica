import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';

const About = () => {
  return (
    <Container>
      <h1 className="my-4">Acerca del Proyecto</h1>
      
      <Row className="mb-5">
        <Col>
          <Card>
            <Card.Body>
              <h2 className="section-title">RutaAcadémica: Sistema de Análisis de Prerrequisitos Académicos</h2>
              <p>
                Este proyecto implementa un sistema llamado "RutaAcadémica" que utiliza grafos dirigidos para identificar 
                todas las asignaturas previas necesarias para cursar una materia específica en diferentes planes de estudio 
                universitarios (pensums).
              </p>
              <p>
                La herramienta proporciona una visualización interactiva y clara de las relaciones entre asignaturas, 
                permitiendo a los estudiantes y personal académico comprender mejor la estructura curricular y planificar 
                eficientemente sus estudios.
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      
      <h2 className="mb-4">Características Principales</h2>
      <Row className="row-cols-1 row-cols-md-3 g-4 mb-5">
        <Col>
          <Card className="h-100">
            <Card.Body>
              <h3 className="h5 mb-3">Análisis de Prerrequisitos</h3>
              <p>
                Implementación de algoritmos de grafos para identificar todas las asignaturas previas 
                necesarias para cursar una materia específica.
              </p>
            </Card.Body>
          </Card>
        </Col>
        
        <Col>
          <Card className="h-100">
            <Card.Body>
              <h3 className="h5 mb-3">Visualización de Grafos</h3>
              <p>
                Representación visual intuitiva de las relaciones entre asignaturas mediante grafos 
                dirigidos interactivos.
              </p>
            </Card.Body>
          </Card>
        </Col>
        
        <Col>
          <Card className="h-100">
            <Card.Body>
              <h3 className="h5 mb-3">Soporte Multicarrera</h3>
              <p>
                Capacidad para manejar diferentes planes de estudio (pensums) para diversas carreras 
                universitarias simultáneamente.
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      
      <h2 className="mb-4">Tecnologías Utilizadas</h2>
      <Row className="mb-5">
        <Col md={6}>
          <Card className="h-100">
            <Card.Header className="bg-primary text-white">
              <h3 className="h5 mb-0">Backend</h3>
            </Card.Header>
            <Card.Body>
              <ul>
                <li><strong>Python:</strong> Lenguaje principal de programación</li>
                <li><strong>FastAPI:</strong> Framework para desarrollo de APIs</li>
                <li><strong>SQLAlchemy:</strong> ORM para interacción con base de datos</li>
                <li><strong>NetworkX:</strong> Biblioteca para manipulación de grafos</li>
                <li><strong>Pydantic:</strong> Validación de datos y esquemas</li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={6}>
          <Card className="h-100">
            <Card.Header className="bg-success text-white">
              <h3 className="h5 mb-0">Frontend</h3>
            </Card.Header>
            <Card.Body>
              <ul>
                <li><strong>React:</strong> Biblioteca para interfaces de usuario</li>
                <li><strong>Bootstrap:</strong> Framework CSS para diseño responsive</li>
                <li><strong>vis.js:</strong> Biblioteca para visualización de grafos</li>
                <li><strong>Axios:</strong> Cliente HTTP para comunicación con la API</li>
                <li><strong>React Router:</strong> Enrutamiento en aplicaciones React</li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      
      <h2 className="mb-4">Equipo de Desarrollo</h2>
      <Row>
        <Col>
          <Card>
            <Card.Body>
              <p>
                El Proyecto RutaAcadémica fue desarrollado como parte de la materia estructuras de datos 
                y algoritmos II, enfocándose en la aplicación práctica de teoría de grafos para resolver problemas 
                académicos reales.
              </p>
              <p className="mb-0">
                © 2025 RutaAcadémica - Todos los derechos reservados
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default About;