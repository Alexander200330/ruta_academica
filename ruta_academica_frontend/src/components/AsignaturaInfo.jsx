import React from 'react';
import { Card, Row, Col, Badge } from 'react-bootstrap';

const AsignaturaInfo = ({ data }) => {
  if (!data || !data.asignatura_objetivo) {
    return null;
  }
  
  const { asignatura_objetivo, total_asignaturas_previas, creditos_requeridos_total } = data;
  
  return (
    <Card className="mb-4">
      <Card.Body>
        <h3 className="section-title">Información de la Asignatura</h3>
        
        <div className="asignatura-card p-3 mb-4">
          <h4 className="mb-3">
            {asignatura_objetivo.codigo} - {asignatura_objetivo.nombre}
          </h4>
          
          <Row className="g-3">
            <Col md={6}>
              <div className="d-flex">
                <div className="me-2">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 5H5v14h14V5z" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M16 2v3M8 2v3M3 10h18" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
                <div>
                  <div className="text-muted small">Trimestre</div>
                  <div className="fw-bold">{asignatura_objetivo.trimestre || 'No especificado'}</div>
                </div>
              </div>
            </Col>
            
            <Col md={6}>
              <div className="d-flex">
                <div className="me-2">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 1v22M17 5H9.5a3.5 3.5 0 1 0 0 7h5a3.5 3.5 0 1 1 0 7H6" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
                <div>
                  <div className="text-muted small">Créditos</div>
                  <div className="fw-bold">{asignatura_objetivo.creditos}</div>
                </div>
              </div>
            </Col>
          </Row>
        </div>
        
        <Row className="g-4 text-center">
          <Col md={6}>
            <Card className="h-100 bg-light">
              <Card.Body>
                <h2 className="display-4 fw-bold text-primary mb-0">{total_asignaturas_previas}</h2>
                <p className="text-muted">Asignaturas Previas</p>
              </Card.Body>
            </Card>
          </Col>
          
          <Col md={6}>
            <Card className="h-100 bg-light">
              <Card.Body>
                <h2 className="display-4 fw-bold text-primary mb-0">{creditos_requeridos_total}</h2>
                <p className="text-muted">Créditos Requeridos</p>
              </Card.Body>
            </Card>
          </Col>
        </Row>
        
        {data.requisitos_especiales && data.requisitos_especiales.length > 0 && (
          <div className="mt-4">
            <h5>Requisitos Especiales</h5>
            <ul className="list-unstyled">
              {data.requisitos_especiales.map((req, index) => (
                <li key={index} className="mb-2">
                  <Badge bg="warning" text="dark" className="me-2">Especial</Badge>
                  {req}
                </li>
              ))}
            </ul>
          </div>
        )}
      </Card.Body>
    </Card>
  );
};

export default AsignaturaInfo;