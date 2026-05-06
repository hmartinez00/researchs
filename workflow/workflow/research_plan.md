```json
{
  "titulo": "Segmentación Semántica en Tiempo Real para Respuesta a Desastres: Aceleración de Emergencias mediante Visión por Computadora en Plataformas UAV",
  "abstract_preliminar": "La segmentación semántica en tiempo real de imágenes aéreas es fundamental para la respuesta rápida a desastres naturales como inundaciones, incendios y terremotos. Este trabajo presenta una revisión sistemática y framework metodológico para el despliegue eficiente de modelos de segmentación semántica ligeros en plataformas UAV y edge computing, priorizando métricas de precisión (mIoU, F1-score) y latencia (FPS, tiempo de inferencia). Se analizan arquitecturas como Fast-SCNN, BiSeNetV2 y variantes basadas en Transformers adaptadas a entornos de desastres, junto con datasets especializados como RescueNet y BlessemFlood21. Se discuten desafíos como variabilidad ambiental, robustez en condiciones adversas y optimizaciones para hardware embebido. Los resultados cuantitativos de benchmarks recientes (2023-2026) demuestran la viabilidad de inferencia en tiempo real (<30 ms por imagen) con mIoU superior a 0.65 en escenarios reales, contribuyendo a la aceleración de la toma de decisiones en operaciones de emergencia. Se proponen directrices para integración en sistemas de respuesta humanitaria.",
  "secciones": [
    {
      "nro": 1,
      "titulo_seccion": "Introducción y Motivación",
      "objetivos": ["Contextualizar la importancia de la segmentación semántica en respuesta a desastres", "Identificar brechas en sistemas de tiempo real actuales"],
      "subsecciones": ["1.1 Antecedentes en teledetección para emergencias", "1.2 Desafíos en entornos de desastres"],
      "insumos": ["Figura 1: Ejemplos de desastres", "Tabla 1: Comparación de tiempos de respuesta tradicionales vs IA"],
      "llaves_bibtex": ["Rahnemoonfar2023RescueNet", "Sharifi2026FastSCNN"]
    },
    {
      "nro": 2,
      "titulo_seccion": "Fundamentos de Segmentación Semántica",
      "objetivos": ["Revisar arquitecturas CNN y Transformers para segmentación", "Analizar trade-offs precisión vs eficiencia"],
      "subsecciones": ["2.1 Modelos convolucionales ligeros", "2.2 Enfoques basados en atención y Transformers", "2.3 Optimizaciones para edge computing"],
      "insumos": ["Eq. 1: Función de pérdida Dice + CE", "Tabla 2: Benchmarks de latencia"],
      "llaves_bibtex": ["Lee2024LightweightDisaster", "Jiang2023STDC", "Wang2025RWKV"]
    },
    {
      "nro": 3,
      "titulo_seccion": "Datasets y Benchmarks para Desastres",
      "objetivos": ["Catalogar datasets públicos relevantes", "Evaluar su representatividad para escenarios reales"],
      "subsecciones": ["3.1 Datasets UAV post-desastre", "3.2 Datasets de inundaciones y fuegos forestales", "3.3 Métricas de evaluación estandarizadas"],
      "insumos": ["Tabla 3: Resumen de datasets (resolución, clases, tamaño)", "Figura 2: Muestras anotadas"],
      "llaves_bibtex": ["Rahnemoonfar2023RescueNet", "Polushko2024BlessemFlood21", "Zhao2024RescueTarget"]
    },
    {
      "nro": 4,
      "titulo_seccion": "Aplicaciones en Respuesta a Emergencias en Tiempo Real",
      "objetivos": ["Demostrar casos de uso en inundaciones, incendios y búsqueda-rescate", "Analizar rendimiento en plataformas UAV"],
      "subsecciones": ["4.1 Mapeo de inundaciones y daños", "4.2 Detección de incendios y zonas seguras", "4.3 Integración con sistemas de comando de incidentes"],
      "insumos": ["Tabla 4: Resultados cuantitativos en escenarios reales", "Figura 3: Pipeline de despliegue UAV"],
      "llaves_bibtex": ["Sharifi2026FastSCNN", "Sui2025TDBOSegNet", "Lee2024LightweightDisaster", "Zulkifley2025BurnedForest"]
    },
    {
      "nro": 5,
      "titulo_seccion": "Desafíos, Optimizaciones y Direcciones Futuras",
      "objetivos": ["Identificar limitaciones actuales", "Proponer mejoras para robustez y escalabilidad"],
      "subsecciones": ["5.1 Robustez a condiciones adversas", "5.2 Compresión de modelos y cuantización", "5.3 Hacia sistemas multimodales y autónomos"],
      "insumos": ["Tabla 5: Comparativa de eficiencia energética", "Eq. 2: Fórmula de mIoU"],
      "llaves_bibtex": ["Shaheen2025AerialFlood", "Raju2026EcoDisasterLocNet", "Haubenstock2025UAVMapping"]
    }
  ]
}
```

**PARTE 2: BLOQUES BIBLIOGRÁFICOS SECCIONALES**

```bibtex
@article{Rahnemoonfar2023RescueNet,
  author = {Rahnemoonfar, Maryam and others},
  title = {RescueNet: A High Resolution UAV Semantic Segmentation Dataset for Natural Disaster Damage Assessment},
  journal = {Scientific Data},
  year = {2023},
  volume = {10},
  doi = {10.1038/s41597-023-02799-4},
  url = {https://www.nature.com/articles/s41597-023-02799-4}
}

@article{Sharifi2026FastSCNN,
  author = {Sharifi, A. and others},
  title = {Benchmarking lightweight deep networks for real-time flood segmentation in unmanned aerial vehicle imagery},
  journal = {Applied Computing and Geosciences},
  year = {2026},
  volume = {29},
  pages = {100319},
  doi = {10.1016/j.acags.2026.100319},
  url = {https://www.sciencedirect.com/science/article/pii/S2590197426000030}
}
```

```bibtex
@article{Lee2024LightweightDisaster,
  author = {Lee, H. and others},
  title = {Lightweight Disaster Semantic Segmentation for UAV On-Device Intelligence},
  journal = {IEEE Conference Proceedings},
  year = {2024},
  doi = {10.1109/XXXX},
  url = {https://ieeexplore.ieee.org/document/10642893/}
}

@article{Jiang2023STDC,
  author = {Jiang, B. and others},
  title = {A Real-Time Semantic Segmentation Method Based on STDC for Emergency Landing Zone},
  journal = {Sensors (Basel)},
  year = {2023},
  doi = {10.3390/s231773xx},
  url = {https://pmc.ncbi.nlm.nih.gov/articles/PMC10386455/}
}

@article{Wang2025RWKV,
  author = {Wang, Q. and others},
  title = {Leveraging RWKV for Efficient Remote Sensing Semantic Segmentation},
  journal = {IEEE Journal},
  year = {2025},
  doi = {10.1109/XXXX},
  url = {https://ieeexplore.ieee.org/document/11214221/}
}
```

```bibtex
@article{Polushko2024BlessemFlood21,
  author = {Polushko, V. and others},
  title = {BlessemFlood21: Advancing Flood Analysis with a High-Resolution Georeferenced Dataset},
  journal = {IEEE Conference Proceedings},
  year = {2024},
  url = {https://ieeexplore.ieee.org/document/10737086/}
}

@article{Zhao2024RescueTarget,
  author = {Zhao, B. and others},
  title = {Real-time Rescue Target Detection Based on UAV Imagery for Flood Emergency Response},
  journal = {Journal of Geospatial Information Science},
  year = {2024},
  url = {https://www.sciopen.com/article/10.11947/j.JGGS.2024.0106}
}
```

```bibtex
@article{Sui2025TDBOSegNet,
  author = {Sui, Y. and others},
  title = {TDBOSegNet: A Semantic Segmentation Model for Typical Disaster-Bearing Objects in UAV Images of Flood Disasters},
  journal = {Canadian Journal of Remote Sensing},
  year = {2025},
  url = {https://www.tandfonline.com/doi/full/10.1080/07038992.2025.2589555}
}

@article{Zulkifley2025BurnedForest,
  author = {Zulkifley, M.A. and others},
  title = {Burned Forest Areas Mapping Using Semantic Segmentation},
  journal = {IEEE Conference Proceedings},
  year = {2025},
  url = {https://ieeexplore.ieee.org/document/10933135/}
}
```

```bibtex
@article{Shaheen2025AerialFlood,
  author = {Shaheen, M.T. and others},
  title = {Advancing Aerial Image Semantic Segmentation for Flood Monitoring},
  journal = {IEEE Conference Proceedings},
  year = {2025},
  url = {https://ieeexplore.ieee.org/document/10979465/}
}

@article{Raju2026EcoDisasterLocNet,
  author = {Raju, A.S.N. and others},
  title = {EcoDisasterLocNet: a sustainable AI framework for disaster classification and localisation},
  journal = {Journal of Big Data},
  year = {2026},
  url = {https://link.springer.com/article/10.1186/s40537-026-01368-x}
}

@article{Haubenstock2025UAVMapping,
  author = {Haubenstock, M. and others},
  title = {Advancements on Semantic Real-Time UAV Mapping},
  journal = {ISPRS Archives},
  year = {2025},
  url = {https://isprs-archives.copernicus.org/articles/XLVIII-2-W11-2025/111/2025/}
}
```

**PARTE 3: MAPA DE USO DE REFERENCIAS (POR SECCIÓN)**

```json
{
  "seccion_nro": 1,
  "titulo_seccion": "Introducción y Motivación",
  "mapa_uso": {
    "Rahnemoonfar2023RescueNet": {
      "razon_seleccion": "Dataset benchmark de alta resolución UAV para evaluación de daños post-desastre, ampliamente citado.",
      "guia_redaccion": "Usar en 1.1 para ilustrar la necesidad de datasets específicos y citar su tamaño y clases en motivación.",
      "subseccion_destino": "1.1"
    },
    "Sharifi2026FastSCNN": {
      "razon_seleccion": "Benchmark reciente de modelos ligeros para segmentación de inundaciones en UAV con métricas de tiempo real.",
      "guia_redaccion": "Usar en 1.2 para destacar brechas en bordes complejos y justificar aceleración vía IA.",
      "subseccion_destino": "1.2"
    }
  }
}
```

```json
{
  "seccion_nro": 2,
  "titulo_seccion": "Fundamentos de Segmentación Semántica",
  "mapa_uso": {
    "Lee2024LightweightDisaster": {
      "razon_seleccion": "Modelo ligero específico para segmentación de desastres en dispositivos UAV.",
      "guia_redaccion": "Usar en 2.1 para comparar con baselines y citar resultados de on-device inference.",
      "subseccion_destino": "2.1"
    },
    "Jiang2023STDC": {
      "razon_seleccion": "Método STDC para segmentación en tiempo real en escenarios de emergencia UAV.",
      "guia_redaccion": "Usar en 2.1 para detallar arquitecturas eficientes y ecuaciones de pérdida.",
      "subseccion_destino": "2.1"
    },
    "Wang2025RWKV": {
      "razon_seleccion": "Enfoque eficiente con RWKV para segmentación en teledetección de alta resolución.",
      "guia_redaccion": "Usar en 2.2 para contrastar con CNNs tradicionales destacando eficiencia.",
      "subseccion_destino": "2.2"
    }
  }
}
```

```json
{
  "seccion_nro": 3,
  "titulo_seccion": "Datasets y Benchmarks para Desastres",
  "mapa_uso": {
    "Rahnemoonfar2023RescueNet": {
      "razon_seleccion": "Principal dataset de referencia para daños post-huracán con anotaciones semánticas detalladas.",
      "guia_redaccion": "Usar en 3.1 para tabla comparativa y describir clases de daños.",
      "subseccion_destino": "3.1"
    },
    "Polushko2024BlessemFlood21": {
      "razon_seleccion": "Dataset georreferenciado de alta resolución para segmentación de agua en inundaciones.",
      "guia_redaccion": "Usar en 3.2 para ejemplos de inundaciones fluviales y métricas de evaluación.",
      "subseccion_destino": "3.2"
    },
    "Zhao2024RescueTarget": {
      "razon_seleccion": "Enfoque de detección y segmentación para objetivos de rescate en inundaciones.",
      "guia_redaccion": "Usar en 3.3 para métricas IoU en extracción de agua y targets.",
      "subseccion_destino": "3.3"
    }
  }
}
```

```json
{
  "seccion_nro": 4,
  "titulo_seccion": "Aplicaciones en Respuesta a Emergencias en Tiempo Real",
  "mapa_uso": {
    "Sharifi2026FastSCNN": {
      "razon_seleccion": "Evaluación exhaustiva de Fast-SCNN y BiSeNetV2 en segmentación de inundaciones UAV.",
      "guia_redaccion": "Usar en 4.1 para resultados cuantitativos (F1, IoU) y limitaciones cualitativas.",
      "subseccion_destino": "4.1"
    },
    "Sui2025TDBOSegNet": {
      "razon_seleccion": "Modelo especializado en objetos portadores de desastre en imágenes de inundación UAV.",
      "guia_redaccion": "Usar en 4.1 para evaluación de daños en objetos típicos.",
      "subseccion_destino": "4.1"
    },
    "Lee2024LightweightDisaster": {
      "razon_seleccion": "Implementación on-device para inteligencia en UAV de desastres.",
      "guia_redaccion": "Usar en 4.3 para pipeline de despliegue y consideraciones de hardware.",
      "subseccion_destino": "4.3"
    },
    "Zulkifley2025BurnedForest": {
      "razon_seleccion": "Segmentación para mapeo de áreas quemadas en incendios forestales.",
      "guia_redaccion": "Usar en 4.2 para aplicación específica en detección de incendios.",
      "subseccion_destino": "4.2"
    }
  }
}
```

```json
{
  "seccion_nro": 5,
  "titulo_seccion": "Desafíos, Optimizaciones y Direcciones Futuras",
  "mapa_uso": {
    "Shaheen2025AerialFlood": {
      "razon_seleccion": "Avances en segmentación aérea para monitoreo de inundaciones comparando real-time vs offline.",
      "guia_redaccion": "Usar en 5.1 para discutir robustez y comparación de modelos.",
      "subseccion_destino": "5.1"
    },
    "Raju2026EcoDisasterLocNet": {
      "razon_seleccion": "Framework sostenible para clasificación y localización de desastres con interpretabilidad.",
      "guia_redaccion": "Usar en 5.3 para enfoques multimodales y Grad-CAM en futuras direcciones.",
      "subseccion_destino": "5.3"
    },
    "Haubenstock2025UAVMapping": {
      "razon_seleccion": "Avances en mapeo semántico UAV en tiempo real para gestión de crisis.",
      "guia_redaccion": "Usar en 5.2 para optimizaciones de ortofotos y segmentación en tiempo real.",
      "subseccion_destino": "5.2"
    }
  }
}
```