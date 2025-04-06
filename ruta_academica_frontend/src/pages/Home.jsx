import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';

const Home = () => {
  return (
    <Container>
      <div className="text-center py-5">
        <h1 className="display-4 fw-bold">RutaAcadémica</h1>
        <p className="lead mb-4">
          Sistema de análisis de prerrequisitos académicos mediante grafos dirigidos
        </p>
        <Button 
          as={Link} 
          to="/ruta-academica" 
          variant="primary" 
          size="lg"
          className="mb-5"
        >
          Explorar Rutas Académicas
        </Button>
      </div>

      <Row className="g-4 py-4">
        <Col md={4}>
          <Card className="h-100">
            <Card.Body>
              <div className="text-center mb-3">
                <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <Card.Title className="text-center h4 mb-3">
                Pensums Digitalizados
              </Card.Title>
              <Card.Text>
                Accede a los pensums de diversas carreras universitarias en formato digital y 
                estructurado, facilitando la visualización y análisis de las estructuras curriculares.
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={4}>
          <Card className="h-100">
            <Card.Body>
              <div className="text-center mb-3">
                <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2L2 7l10 5 10-5-10-5z" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M2 17l10 5 10-5" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M2 12l10 5 10-5" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <Card.Title className="text-center h4 mb-3">
                Análisis de Prerrequisitos
              </Card.Title>
              <Card.Text>
                Visualiza todas las asignaturas previas necesarias para cursar una materia específica, 
                organizadas en niveles que reflejan el camino más eficiente a través del plan de estudios.
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={4}>
          <Card className="h-100">
            <Card.Body>
              <div className="text-center mb-3">
                <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <circle cx="12" cy="10" r="3" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <Card.Title className="text-center h4 mb-3">
                Visualización Intuitiva
              </Card.Title>
              <Card.Text>
                Explora los planes de estudio a través de visualizaciones interactivas basadas en grafos,
                que te permiten comprender fácilmente las relaciones entre asignaturas.
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <div className="text-center py-4">
        <Button as={Link} to="/about" variant="outline-primary">
          Conoce más sobre el proyecto
        </Button>
      </div>
    </Container>
  );
};

export default Home;