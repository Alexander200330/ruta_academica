/**
 * Adaptador para transformar los datos de la API a la estructura esperada por los componentes
 */

/**
 * Adapta los datos de la respuesta de la API a la estructura esperada por los componentes
 * de visualización.
 * 
 * @param {Object} apiResponse - Respuesta original de la API
 * @returns {Object} Datos adaptados para los componentes
 */
export const adaptRutaAcademicaData = (apiResponse) => {
    // Si hay un error, mantener la estructura de error
    if (apiResponse.error) {
      return apiResponse;
    }
  
    // Verificar que la respuesta tenga la estructura mínima necesaria
    if (!apiResponse.asignatura_objetivo) {
      return {
        error: 'La respuesta de la API no contiene información de la asignatura objetivo'
      };
    }
  
    // No es necesario transformar la estructura si ya tiene el formato adecuado
    return apiResponse;
  };
  
  export default {
    adaptRutaAcademicaData
  };