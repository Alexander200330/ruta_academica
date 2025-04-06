import React from 'react';
import { Card } from 'react-bootstrap';

const ProgressTracker = ({ currentStep }) => {
  // Pasos del proceso
  const steps = [
    { number: 1, title: 'Seleccionar Carrera' },
    { number: 2, title: 'Seleccionar Pensum' },
    { number: 3, title: 'Buscar Asignatura' },
    { number: 4, title: 'Visualizar Ruta' }
  ];
  
  return (
    <Card className="mb-3 py-0">
      <Card.Body className="py-2">
        <div className="d-flex justify-content-between align-items-center compact-steps">
          {steps.map(step => (
            <div 
              key={step.number} 
              className={`step ${step.number < currentStep ? 'completed' : ''} ${step.number === currentStep ? 'active' : ''}`}
            >
              <div className="step-number">{step.number}</div>
              <div className="step-title small">{step.title}</div>
            </div>
          ))}
        </div>
      </Card.Body>
    </Card>
  );
};

export default ProgressTracker;