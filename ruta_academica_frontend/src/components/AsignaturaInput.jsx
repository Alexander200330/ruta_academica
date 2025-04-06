import React, { useState, useRef } from 'react';
import { Form, Button, Card, Alert } from 'react-bootstrap';

const AsignaturaInput = ({ pensum, onSearch, isLoading }) => {
  const [codigoAsignatura, setCodigoAsignatura] = useState('');
  const [error, setError] = useState(null);
  const formRef = useRef(null);
  
  const handleInputChange = (e) => {
    setCodigoAsignatura(e.target.value.toUpperCase());
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (codigoAsignatura.trim()) {
      onSearch(codigoAsignatura.trim());
    } else {
      setError('Por favor, ingresa un código de asignatura');
    }
  };
  
  if (!pensum) {
    return null;
  }
  
  return (
    <Card className="mb-4">
      <Card.Body>
        <h3 className="section-title">Buscar Asignatura</h3>
        
        {error && (
          <Alert variant="danger" onClose={() => setError(null)} dismissible>
            {error}
          </Alert>
        )}
        
        <Form ref={formRef} onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Código de la asignatura</Form.Label>
            <Form.Control
              type="text"
              placeholder="Ej: CBM201"
              value={codigoAsignatura}
              onChange={handleInputChange}
              autoComplete="off"
              disabled={isLoading}
            />
            <Form.Text className="text-muted">
              Ingresa el código exacto de la asignatura para ver su ruta académica.
            </Form.Text>
          </Form.Group>
          
          <Button 
            variant="primary" 
            type="submit" 
            className="w-100"
            disabled={!codigoAsignatura.trim() || isLoading}
          >
            {isLoading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Buscando...
              </>
            ) : (
              'Buscar Ruta Académica'
            )}
          </Button>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default AsignaturaInput;