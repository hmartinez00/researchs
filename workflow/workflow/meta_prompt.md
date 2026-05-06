Actúa como Editor Jefe de IEEE. Para el tema de investigación **Segmentación Semántica Desastres (Acelera respuesta a emergencias en tiempo real.)**, genera un **Desglose Temático Detallado** siguiendo estrictamente este esquema de tres partes:

**PARTE 1: ESTRUCTURA JSON**
Entrega un único bloque de código JSON con la siguiente estructura:
```json
{
  "titulo": "Título técnico en español",
  "abstract_preliminar": "Resumen técnico de 150 palabras siguiendo normas IEEE",
  "secciones": [
    {
      "nro": 1,
      "titulo_seccion": "Nombre de la sección",
      "objetivos": ["objetivo 1", "objetivo 2"],
      "subsecciones": ["1.1...", "1.2..."],
      "insumos": ["Tabla 1", "Eq. 1"],
      "llaves_bibtex": ["Key1", "Key2"]
    }
  ]
}
```

**PARTE 2: BLOQUES BIBLIOGRÁFICOS SECCIONALES**
Para cada sección, entrega un bloque de código independiente con las entradas en formato `BibTeX`.
* Fuentes reales, **verificables** (Accesibles desde la web mediante url) y publicadas entre 2023 y 2026.
* La suma total de referencias en TODAS las secciones debe ser ≤ 30.
* Formato limpio, listo para copiar/pegar directamente en `references.bib`.

**PARTE 3: MAPA DE USO DE REFERENCIAS (POR SECCIÓN)**
Para cada sección, genera un bloque JSON independiente que funcione como diccionario asociativo. Debe conectar **textualmente** cada `llave_bibtex` de la PARTE 1 con su justificación y directrices de integración:
```json
{
  "seccion_nro": 1,
  "titulo_seccion": "Nombre exacto de la sección",
  "mapa_uso": {
    "Key1": {
      "razon_seleccion": "Justificación técnica o metodológica de la elección (máx. 1 oración).",
      "guia_redaccion": "Instrucción precisa sobre cómo integrarla (ej: 'Usar en 1.1 para contrastar X vs Y, citando resultados de eficiencia y destacando limitaciones en entornos reales').",
      "subseccion_destino": "1.1"
    },
    "Key2": { "..." : "..." }
  }
}
```

**🔒 INSTRUCCIONES CRÍTICAS:**
1. **Coherencia absoluta:** Las claves en `llaves_bibtex` (PARTE 1), en los bloques `.bib` (PARTE 2) y en `mapa_uso` (PARTE 3) deben coincidir carácter por carácter.
2. **Sin redacción aún:** No generes párrafos, introducciones ni conclusiones. Solo entrega los bloques de código solicitados.
3. **Formato estricto:** Cada parte debe ir en su propio bloque de código. No incluyas texto explicativo, saludos ni comentarios entre bloques.
4. **Enfoque IEEE:** Prioriza referencias de journals/conferencias indexados, métricas cuantitativas y metodologías reproducibles.