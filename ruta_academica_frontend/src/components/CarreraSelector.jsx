import React, { useState, useEffect } from 'react';
import { Form, Card } from 'react-bootstrap';
import { carrerasService } from '../services/api';

const CarreraSelector = ({ onSelectCarrera }) => {
  const [carreras, setCarreras] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchCarreras = async () => {
      try {
        setLoading(true);
        const data = await carrerasService.getAll();
        setCarreras(data);
        setError(null);
      } catch (err) {
        setError('Error al cargar las carreras. Por favor, intente nuevamente.');
        console.error('Error al cargar carreras:', err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchCarreras();
  }, []);
  
  const handleChange = (e) => {
    const carreraId = parseInt(e.target.value);
    if (carreraId) {
      const selectedCarrera = carreras.find(c => c.id === carreraId);
      if (selectedCarrera) {
        onSelectCarrera(selectedCarrera);
      }
    } else {
      onSelectCarrera(null);
    }
  };
  
  return (
    <Card className="mb-4">
      <Card.Body>
        <h3 className="section-title">Selecciona una Carrera</h3>
        {loading ? (
          <div className="loader">
            <div className="loader-spinner"></div>
          </div>
        ) : error ? (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        ) : (
          <Form.Group>
            <Form.Label>Carrera</Form.Label>
            <Form.Select onChange={handleChange} defaultValue="">
              <option value="">Seleccionar carrera...</option>
              {carreras.map(carrera => (
                <option key={carrera.id} value={carrera.id}>
                  {carrera.nombre} ({carrera.codigo})
                </option>
              ))}
            </Form.Select>
            <Form.Text className="text-muted">
              Selecciona una carrera para ver sus pensums y asignaturas disponibles.
            </Form.Text>
          </Form.Group>
        )}
      </Card.Body>
    </Card>
  );
};

export default CarreraSelector;