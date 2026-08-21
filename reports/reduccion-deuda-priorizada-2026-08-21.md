# Reducción de deuda priorizada — 21 de agosto de 2026

## Alcance cerrado

Este lote reduce deuda reproducible sin promover fuentes, alterar contenido jurídico ni convertir la wiki en un servicio transaccional. Se aplicaron cambios en tres frentes: contratos entre repositorios, accesibilidad de componentes progresivos y transparencia editorial en descubrimiento.

| Frente | Corrección aplicada | Evidencia de cierre |
|---|---|---|
| `arancel-mx` | Se añadió un contrato `release_bundle` que fija el repositorio canónico, commit observado, release `data-2026.08.17`, schema v2, seis assets verificables y fallback textual. | El validador offline exige identidad, release, commit y lista exacta de assets; no incorpora tablas arancelarias locales. |
| `dof-diff-lab` | Se añadió un contrato `monitor_state` que fija el estado diario, hash normalizado, revisión humana obligatoria y límite de interpretación. | El contrato declara explícitamente que un cambio detectado no equivale a vigencia jurídica. |
| Validador | `validate_data_contracts.py` ahora valida contratos geoespaciales, bundles de release y estados de monitor; ignora el modelo unificado local, que no es una integración externa. | Las pruebas cubren AduanaMap, arancel-mx, dof-diff-lab y el comando de validación completo. |
| Dashboard ANAM | Ante una falla de JSON con JavaScript activo, se muestra un resumen publicado de cuatro indicadores, sin ocultar la fuente primaria ni fabricar datos. | Prueba de regresión y sintaxis JavaScript correctas. |
| Explorador mundial | Una consulta sin coincidencias muestra un mensaje contextual dentro de la región de resultados. | Prueba de regresión y sintaxis JavaScript correctas. |
| Herramientas | El catálogo expone una tabla de estado editorial, fecha de corte visible y fuente o contrato por ruta. | El patrón enlaza al registro canónico y al modelo de estados sin promover contenidos. |

## Límites preservados

El contrato de `arancel-mx` no habilita una copia o sincronización automática de TIGIE/NICO en la wiki. El contrato de `dof-diff-lab` no vuelve un diff, hash o etiqueta de monitorización una determinación jurídica. AduanaMap permanece en modo textual hasta que exista un artefacto geoespacial público, inmutable, atribuible y verificable.

## Validación

La suite de contratos y la compilación normal con verificación de sitio pasan. El perfil offline también compila correctamente. El verificador de sitio no se ejecuta contra la salida offline porque exige rutas legacy que dicho perfil no genera; esta diferencia es una limitación conocida del procedimiento de auditoría, no un enlace roto del contenido.

## Deuda restante priorizada

| Prioridad | Pendiente | Condición de cierre |
|---|---|---|
| P1 | Lockfile o hashes de artefactes para dependencias de documentación. | Acordar política de actualización y generar artefacto reproducible sin añadir dependencias runtime. |
| P1 | Pruebas manuales de móvil, contraste y lector de pantalla con contenido real. | Ejecutar matriz de viewport, teclado y lector de pantalla documentada. |
| P1 | Estados por tarjeta derivados automáticamente de metadatos canónicos. | Definir un esquema de superficie de descubrimiento que no duplique ni promueva estados. |
| P2 | Artefacto geoespacial público para AduanaMap. | Release inmutable, hash, atribución, licencia y presupuesto de rendimiento. |
| P2 | Integración operativa de arancel-mx o dof-diff-lab. | Decisión de producto, consumo de release/payload real y pruebas de compatibilidad end-to-end. |
