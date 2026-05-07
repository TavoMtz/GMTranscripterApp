Aquí tienes el prompt completo:

---

## Prompt: Plan de desarrollo — Deep Notes

**Contexto del producto:**
Deep Notes es una app web de transcripción y análisis de audio. El usuario graba audio directamente desde la app (conversaciones, entrevistas, clases), y la app genera dos outputs: una transcripción literal y unas "Deep Notes" (resumen + puntos clave). El nombre anterior era GM Transcripter — ya no se usa.

---

**Stack y arquitectura actual:**
Usemos lo que ya tenemos, si es necesario un cambio en el stack tecnologico no se realizara ahora.
---
 
**Layout general:**
La interfaz es un dashboard de dos columnas:

**Columna izquierda — Historial (sidebar fijo):**
- Logo "Deep Notes" en la parte superior con subtítulo "Audio intelligence"
- Lista de sesiones recientes, cada item muestra:
  - Título de la sesión
  - Etiqueta/tag coloreado (campo existente en DB, ej: Physics → violeta, Spanish → cyan, Software → amber, Research → rosa)
  - Fecha relativa (Hoy, May 5, etc.)
- Item activo tiene fondo con tinte cyan y borde sutil
- Sin scroll visible (scrollbar oculto)

**Columna derecha — Main area:**

*Topbar:*
- Título de la sesión activa + etiqueta tag a su lado
- Switch pill en la derecha con dos estados: "Transcripción" (izq) y "Deep Notes" (der)
- El switch NO son pestañas separadas — es un control tipo pill/toggle donde el botón activo tiene fondo elevado

*Área de contenido (scrollable):*
- Vista Transcripción: lista de líneas con timestamp (0:04, 0:22…) + texto del fragmento
- Vista Deep Notes:
  - Sección "Resumen" con label uppercase cyan, texto con borde izquierdo sutil cyan
  - Sección "Puntos clave" con items en cards individuales con punto violeta + texto

*Barra de grabación (fija al fondo):*
- Botón circular rojo de 48px — idle muestra ícono micrófono, recording muestra ícono stop
- Estado idle: sin animación. Estado recording: animación pulse (ring que se expande y desvanece en loop)
- Al lado del botón: texto de estado ("Listo para grabar" / "Grabando..." con punto parpadeante / "Grabación guardada → Procesando...")
- Waveform animado de 8 barras que solo aparece durante grabación (opacity 0 → 1)
- Cronómetro MM:SS en el extremo derecho, corre solo durante grabación

---

**Paleta de colores (CSS variables):**
```css
--dn-bg: #0a0d14;
--dn-surface: #111520;
--dn-surface2: #171c2b;
--dn-border: rgba(255,255,255,0.07);
--dn-border2: rgba(255,255,255,0.12);
--dn-cyan: #00e5c8;
--dn-violet: #7c5cfc;
--dn-text: #f0f2ff;
--dn-muted: #6a7290;
--dn-muted2: #8d95b8;
--dn-record: #ff4d6a;
```

**Tipografía:**
- Display / logo: `Syne` 700
- Body / UI: `DM Sans` 300–500
- Tamaños: logo 17px, labels uppercase 10px tracking 1.2px, body 13–13.5px, timestamps 11px

---

**Tags por categoría (colores):**
| Etiqueta | Color | Background token | Text token |
|----------|-------|-----------------|------------|
| Physics, cualquier ciencia | Violeta | rgba(124,92,252,0.18) | #a68fff |
| Spanish, idiomas | Cyan | rgba(0,229,200,0.12) | #00e5c8 |
| Software, tech | Amber | rgba(255,179,71,0.12) | #ffb347 |
| Research, académico | Pink | rgba(255,100,130,0.12) | #ff6482 |

---

**Estados del grabador:**

| Estado | Botón | Status text | Waveform | Timer |
|--------|-------|-------------|----------|-------|
| Idle | Mic icon, sin animación | "Listo para grabar" | oculto | 0:00 |
| Recording | Stop icon, pulse animation | "● Grabando..." (punto parpadea) | visible + animado | corriendo |
| Guardado | Mic icon | "Grabación guardada" → 2.5s → reset | oculto | 0:00 |

---

**Comportamiento del switch Transcripción / Deep Notes:**
- Es un contenedor pill con dos botones internos
- El botón activo recibe `background: var(--dn-surface2)` + border + color blanco
- El inactivo es transparente con texto muted
- Al cambiar, se hace `display:none` / `display:block` en el panel correspondiente (o con clase `.hidden`)
- No hay animación de transición requerida, pero se puede agregar un fade de 150ms si se desea

---

**Interacciones requeridas:**
1. Click en item del historial → marca ese item como activo (resalta con tinte cyan), carga título y tag en topbar
2. Click en botón grabar → inicia grabación (cambia ícono, activa pulse, inicia cronómetro, muestra waveform)
3. Click en botón stop → detiene grabación, muestra estado "Guardado → Procesando", resetea a idle tras 2.5s
4. Click en switch → alterna entre vista Transcripción y vista Deep Notes sin recargar

---
