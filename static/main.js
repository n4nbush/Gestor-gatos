console.log("✅ Script cargado correctamente");

        function establecerFechaHoraActual() {
            console.log("🕒 Estableciendo fecha/hora actual");
            try {
                const ahora = new Date();

                // Formatear a YYYY-MM-DDTHH:MM
                const año = ahora.getFullYear();
                const mes = String(ahora.getMonth() + 1).padStart(2, '0');
                const dia = String(ahora.getDate()).padStart(2, '0');
                const horas = String(ahora.getHours()).padStart(2, '0');
                const minutos = String(ahora.getMinutes()).padStart(2, '0');

                const fechaHoraActual = `${año}-${mes}-${dia}T${horas}:${minutos}`;
                document.getElementById('fecha_hora').value = fechaHoraActual;
                console.log("✅ Fecha/hora establecida:", fechaHoraActual);
            } catch (error) {
                console.error("❌ Error estableciendo fecha/hora:", error);
            }
        }

        function actualizarMotivos() {
            console.log("🔄 Actualizando motivos...");
            try {
                const tipo = document.getElementById('tipo').value;
                const motivoSelect = document.getElementById('motivo');

                console.log("📝 Tipo seleccionado:", tipo);
                console.log("🎯 Elemento motivo encontrado:", motivoSelect);

                // Limpiar opciones anteriores
                motivoSelect.innerHTML = '';

                let motivos = [];

                if (tipo === 'Gasto' || tipo === 'Tarjeta') {
                    console.log("💰 Cargando motivos de gasto");
                    motivos = [
                        'Internet',
                        'Luz',
                        'Celular',
                        'Ferretería',
                        'Servicios Digitales',
                        'Moto',
                        'SUBE',
                        'Uber',
                        'Clio',
                        'Deuda Viejo',
                        'Tarjeta Master',
                        'Tarjeta Visa',
                        'Deuda Banco',
                        'Almacén',
                        'Comida Trabajo',
                        'Gastos Hormiga',
                        'Agustina',
                        'Boris',
                        'Niñera',
                        'Ropa',
                        'Psicóloga',
                        'Gustos',
                        'Peluquería',
                        'Farmacia',
                        'GIM',
                        'Indoor',
                        'Otros gastos'
                    ];
                } else if (tipo === 'Ingreso') {
                    console.log("💵 Cargando motivos de ingreso");
                    motivos = [
                        'Salario',
                        'Inversiones',
                        'Regalo',
                        'Reembolso',
                        'Otros ingresos'
                    ];
                }

                // Agregar opción por defecto
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = `Selecciona un motivo de ${tipo.toLowerCase()}`;
                motivoSelect.appendChild(defaultOption);

                // Agregar motivos
                motivos.forEach(motivo => {
                    const option = document.createElement('option');
                    option.value = motivo;
                    option.textContent = motivo;
                    motivoSelect.appendChild(option);
                });

                console.log(`✅ ${motivos.length} motivos cargados para: ${tipo}`);

            } catch (error) {
                console.error("❌ Error actualizando motivos:", error);
            }
        }

        // Configurar eventos cuando el DOM esté listo
        document.addEventListener('DOMContentLoaded', function() {
            console.log("📄 DOM completamente cargado");

            try {
                // Establecer fecha/hora actual
                establecerFechaHoraActual();

                // Cargar motivos iniciales
                actualizarMotivos();

                // Escuchar cambios en el tipo
                const tipoSelect = document.getElementById('tipo');
                if (tipoSelect) {
                    tipoSelect.addEventListener('change', actualizarMotivos);
                    console.log("🎧 Event listener agregado al select tipo");
                } else {
                    console.error("❌ No se encontró el elemento #tipo");
                }

            } catch (error) {
                console.error("❌ Error en DOMContentLoaded:", error);
            }
        });

        // También ejecutar cuando la ventana se carga completamente
        window.addEventListener('load', function() {
            console.log("🖼️ Ventana completamente cargada");
        });
        function toggleFiltros(){
            console.log("mostrando filtros avanzados")
            document.getElementById('filtros_avanzados').classList.toggle('oculto');
        }