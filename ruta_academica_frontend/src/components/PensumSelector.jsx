import React, { useState, useEffect } from 'react';
import { Form, Card } from 'react-bootstrap';
import { pensumsService } from '../services/api';

const PensumSelector = ({ carrera, onSelectPensum }) => {
  const [pensums, setPensums] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchPensums = async () => {
      if (!carrera) {
        setPensums([]);
        return;
      }
      
      try {
        setLoading(true);
        const data = await pensumsService.getByCarrera(carrera.id);
        setPensums(data);
        setError(null);
      } catch (err) {
        setError('Error al cargar los pensums. Por favor, intente nuevamente.');
        console.error('Error al cargar pensums:', err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchPensums();
  }, [carrera]);
  
  const handleChange = (e) => {
    const pensumId = parseInt(e.target.value);
    if (pensumId) {
      const selectedPensum = pensums.find(p => p.id === pensumId);
      if (selectedPensum) {
        onSelectPensum(selectedPensum);
      }
    } else {
      onSelectPensum(null);
    }
  };
  
  if (!carrera) {
    return null;
  }
  
  return (
    <Card className="mb-4">
      <Card.Body>
        <h3 className="section-title">Selecciona un Pensum</h3>
        {loading ? (
          <div className="loader">
            <div className="loader-spinner"></div>
          </div>
        ) : error ? (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        ) : pensums.length === 0 ? (
          <div className="alert alert-info" role="alert">
            No hay pensums disponibles para esta carrera.
          </div>
        ) : (
          <Form.Group>
            <Form.Label>Pensum</Form.Label>
            <Form.Select onChange={handleChange} defaultValue="">
              <option value="">Seleccionar pensum...</option>
              {pensums.map(pensum => (
                <option key={pensum.id} value={pensum.id}>
                  {pensum.codigo} - {pensum.descripcion} ({pensum.año})
                </option>
              ))}
            </Form.Select>
            <Form.Text className="text-muted">
              Selecciona un pensum para ver sus asignaturas disponibles.
            </Form.Text>
          </Form.Group>
        )}
      </Card.Body>
    </Card>
  );
};

export default PensumSelector;