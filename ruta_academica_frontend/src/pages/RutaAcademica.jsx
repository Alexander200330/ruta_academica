import React, { useState } from 'react';
import { Container, Row, Col, Alert, Card } from 'react-bootstrap';
import { toast } from 'react-toastify';

import ProgressTracker from '../components/ProgressTracker';
import CarreraSelector from '../components/CarreraSelector';
import PensumSelector from '../components/PensumSelector';
import AsignaturaInput from '../components/AsignaturaInput';
import AsignaturaInfo from '../components/AsignaturaInfo';
import GraphVisualization from '../components/GraphVisualization';
import { prerrequisitosService } from '../services/api';
import { adaptRutaAcademicaData } from '../utils/dataAdapter';

const RutaAcademica = () => {
  // Estado para tracking de pasos
  const [currentStep, setCurrentStep] = useState(1);
  
  // Estado para selecciones del usuario
  const [selectedCarrera, setSelectedCarrera] = useState(null);
  const [selectedPensum, setSelectedPensum] = useState(null);
  
  // Estado para datos y carga
  const [rutaData, setRutaData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [ciclosDetectados, setCiclosDetectados] = useState([]);
  
  const handleSelectCarrera = (carrera) => {
    setSelectedCarrera(carrera);
    setSelectedPensum(null);
    setRutaData(null);
    setError(null);
    setCiclosDetectados([]);
    setCurrentStep(carrera ? 2 : 1);
  };
  
  const handleSelectPensum = (pensum) => {
    setSelectedPensum(pensum);
    setRutaData(null);
    setError(null);
    setCiclosDetectados([]);
    setCurrentStep(pensum ? 3 : 2);
  };
  
  const handleSearch = async (codigoAsignatura) => {
    if (!selectedPensum) {
      toast.warning("Por favor, selecciona un pensum primero.");
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      setCiclosDetectados([]);
      
      console.log(`Consultando ruta académica para ${codigoAsignatura} en pensum ${selectedPensum.id}`);
      const apiResponse = await prerrequisitosService.getRutaPorCodigo(codigoAsignatura, selectedPensum.id);
      
      // Adaptar los datos al formato esperado por los componentes
      const data = adaptRutaAcademicaData(apiResponse);
      
      // Verificar si hay errores en la respuesta
      if (data.error) {
        setError(data.error);
        setRutaData(null);
        toast.error(`Error: ${data.error}`);
        
        // Si hay ciclos detectados, mostrarlos
        if (data.ciclos && data.ciclos.length > 0) {
          setCiclosDetectados(data.ciclos);
        }
      } else {
        setRutaData(data);
        setCurrentStep(4);
        toast.success("Ruta académica cargada exitosamente");
      }
    } catch (err) {
      console.error("Error al buscar la ruta académica:", err);
      setError(err.userMessage || "Error al cargar la ruta académica. Por favor, intente nuevamente.");
      setRutaData(null);
      toast.error("Error al cargar la ruta académica");
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <Container className="py-4">
      <h1 className="mb-4">Ruta Académica</h1>
      <p className="lead mb-4">
        Visualiza las asignaturas previas requeridas para cursar una materia específica en tu plan de estudios.
      </p>
      
      <ProgressTracker currentStep={currentStep} />
      
      <Row className="g-4">
        <Col lg={4}>
          <CarreraSelector onSelectCarrera={handleSelectCarrera} />
          
          {selectedCarrera && (
            <PensumSelector carrera={selectedCarrera} onSelectPensum={handleSelectPensum} />
          )}
          
          {selectedPensum && (
            <AsignaturaInput pensum={selectedPensum} onSearch={handleSearch} isLoading={loading} />
          )}
          
          {error && (
            <Alert variant="danger" className="mb-4">
              <Alert.Heading>Error</Alert.Heading>
              <p>{error}</p>
            </Alert>
          )}
          
          {ciclosDetectados.length > 0 && (
            <Card className="mb-4 border-warning">
              <Card.Header className="bg-warning text-dark">
                <strong>¡Atención! Se detectaron ciclos en los prerrequisitos</strong>
              </Card.Header>
              <Card.Body>
                <p>
                  Se han encontrado ciclos en la estructura de prerrequisitos, lo que indica inconsistencias
                  en el pensum. Estos ciclos hacen imposible cumplir con todos los requisitos.
                </p>
                
                {ciclosDetectados.map((ciclo, idx) => (
                  <div key={idx} className="mb-3">
                    <h6>Ciclo {idx + 1}:</h6>
                    <ul className="list-group">
                      {ciclo.map((asig, i) => (
                        <li key={i} className="list-group-item list-group-item-warning">
                          <strong>{asig.codigo}</strong> - {asig.nombre}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </Card.Body>
            </Card>
          )}
          
          {rutaData && <AsignaturaInfo data={rutaData} />}
        </Col>
        
        <Col lg={8}>
          {loading && (
            <Card className="mb-4">
              <Card.Body className="text-center p-5">
                <div className="loader">
                  <div className="loader-spinner"></div>
                </div>
                <p className="mt-3">Cargando ruta académica...</p>
              </Card.Body>
            </Card>
          )}
          
          {!loading && rutaData && (
            <GraphVisualization data={rutaData} />
          )}
          
          {!rutaData && !loading && (
            <Card>
              <Card.Body className="text-center p-5">
                <svg width="100" height="100" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="mb-3 text-muted">
                  <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8h5z" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <h3 className="text-muted">Selecciona una carrera, pensum y asignatura</h3>
                <p className="text-muted">
                  Sigue los pasos en el panel izquierdo para visualizar la ruta académica de una asignatura.
                </p>
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default RutaAcademica;