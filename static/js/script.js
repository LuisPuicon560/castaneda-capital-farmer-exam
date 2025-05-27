document.getElementById("cotizacionForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  
  // Obtener elementos del DOM
  const submitBtn = e.target.querySelector('button[type="submit"]');
  const resultadoDiv = document.getElementById("resultado");
  
  // Deshabilitar botón y mostrar estado de carga
  submitBtn.disabled = true;
  submitBtn.innerHTML = `
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    Procesando...
  `;
  
  try {
    // Obtener datos del formulario
    const formData = new FormData(e.target);
    
    // Enviar petición al backend
    const response = await fetch("/generar-cotizacion", {
      method: "POST",
      body: formData,
    });
    
    // Verificar si la respuesta es exitosa
    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`);
    }
    
    // Procesar la respuesta en formato JSON
    const data = await response.json();
    console.log(data)
    
    // Mostrar resultados
    resultadoDiv.innerHTML = `
      <div class="alert alert-success">
        <h2>Cotización #${data.numero}</h2>
        <p><strong>Precio:</strong> S/ ${data.precio.toFixed(2)}</p>
        <p><strong>Complejidad:</strong> ${data.complejidad}</p>
        ${data.ajuste ? `<p><strong>Ajuste aplicado:</strong> ${data.ajuste}</p>` : ''}
        <div class="propuesta-ia">
          <h4>Propuesta:</h4>
          <p>${data.propuesta}</p>
        </div>
      </div>
    `;
    
  } catch (error) {
    // Manejo de errores
    console.error("Error al enviar el formulario:", error);
    resultadoDiv.innerHTML = `
      <div class="alert alert-danger">
        <h4>Error al procesar la cotización</h4>
        <p>${error.message}</p>
        <p>Por favor, inténtelo nuevamente.</p>
      </div>
    `;
    
  } finally {
    // Reestablecer boton cuando termine el proceso.
    submitBtn.disabled = false;
    submitBtn.textContent = "Generar Cotización";
  }
});