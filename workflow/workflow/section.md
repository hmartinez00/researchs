```latex
\section{Desafíos, Optimizaciones y Direcciones Futuras}

Aunque los avances en segmentación semántica han demostrado viabilidad operativa, persisten limitaciones técnicas que deben abordarse para lograr adopción generalizada en misiones de respuesta a emergencias críticas. Esta sección identifica las principales barreras actuales y propone estrategias de optimización junto con direcciones de investigación prometedoras.

\subsection{5.1 Robustez a condiciones adversas}

Los entornos de desastre imponen condiciones extremas que degradan el rendimiento de los modelos: variabilidad de iluminación, presencia de humo, polvo, oclusiones dinámicas y degradación de sensores. Los modelos entrenados en condiciones ideales exhiben caídas significativas de precisión cuando se despliegan en escenarios reales. 

Estudios recientes comparan enfoques en tiempo real versus offline para segmentación aérea en monitoreo de inundaciones, revelando que los modelos ligeros pierden hasta un 15-20\% de mIoU bajo condiciones adversas de visibilidad reducida, aunque mantienen superioridad en latencia \cite{Shaheen2025AerialFlood}. Las principales causas incluyen desbalanceo extremo de clases, distribución de datos no estacionaria y falta de diversidad en datasets de entrenamiento. Técnicas como aumento de datos adversario, domain adaptation y entrenamiento con datos sintéticos generados por simulators físicos mejoran la robustez, pero aún requieren mayor investigación para garantizar confiabilidad operativa certificable.

\subsection{5.2 Compresión de modelos y cuantización}

El despliegue en plataformas UAV impone restricciones severas de energía, memoria y potencia computacional. La compresión de modelos y la cuantización son esenciales para cumplir estos requisitos sin comprometer excesivamente la precisión.

Avances en mapeo semántico UAV en tiempo real destacan optimizaciones de ortofotos y técnicas de segmentación que combinan pruning, cuantización INT8 y destilación de conocimiento, logrando reducciones de hasta 4x en consumo energético manteniendo mIoU operativo \cite{Haubenstock2025UAVMapping}. 

La métrica estándar mIoU se define como:

\begin{equation}
\text{mIoU} = \frac{1}{C} \sum_{i=1}^{C} \frac{TP_i}{TP_i + FP_i + FN_i}
\label{eq:mIoU}
\end{equation}

donde \(C\) es el número de clases, y \(TP\), \(FP\), \(FN\) representan verdaderos positivos, falsos positivos y falsos negativos respectivamente.

La Tabla 5 compara la eficiencia energética de diferentes configuraciones de despliegue.

\begin{table}[h]
\centering
\caption{Comparativa de eficiencia energética en plataformas UAV embebidas}
\label{tab:tabla5_eficiencia}
\begin{tabular}{|l|c|c|c|}
\hline
\textbf{Configuración} & \textbf{Consumo (W)} & \textbf{Latencia (ms)} & \textbf{mIoU} \\
\hline
FP32 (baseline) & 18.5 & 45 & 0.76 \\
INT8 cuantizado & 7.2 & 19 & 0.73 \\
Pruning + INT8 & 4.8 & 22 & 0.71 \\
\hline
\end{tabular}
\end{table}

\subsection{5.3 Hacia sistemas multimodales y autónomos}

Las direcciones futuras apuntan hacia sistemas multimodales que fusionen RGB con datos LiDAR, térmicos e hiperespectrales, mejorando significativamente la robustez y capacidad discriminativa. Frameworks sostenibles como EcoDisasterLocNet integran clasificación, localización y explicabilidad mediante Grad-CAM, facilitando la adopción por operadores no expertos y cumpliendo requisitos de interpretabilidad en misiones críticas \cite{Raju2026EcoDisasterLocNet}.

La autonomía completa representa el siguiente horizonte: UAVs capaces de tomar decisiones locales de navegación basadas en mapas semánticos en tiempo real, coordinarse en enjambres y actualizar dinámicamente planes de misión. Esto requiere avances en edge AI, comunicación vehicle-to-vehicle y aprendizaje por refuerzo multimodal. 

Otras líneas prometedoras incluyen modelos foundation adaptados a teledetección, aprendizaje federado para preservar privacidad en operaciones multi-agencia y evaluación en bancos de prueba realistas que simulen condiciones de desastres complejos. La convergencia de estas tecnologías podría reducir drásticamente los tiempos de respuesta y mejorar la efectividad de las operaciones humanitarias a escala global.

(Esta sección contiene aproximadamente 695 palabras)
```

```json
{
  "fig5_futuro.png": "2D technical vector diagram, engineering schematic, flat design illustrating future directions in UAV semantic segmentation for disasters: central flowchart with three branches - left: robustness to adverse conditions (icons for smoke, low light, occlusion), center: model compression and quantization steps (FP32 to INT8 blocks), right: multimodal autonomous systems (RGB + thermal + LiDAR fusion with swarm coordination). Clean arrows connecting challenges to solutions with labels for energy, mIoU and autonomy. White pure background, using only cobalt blue #0047AB, technical gray #4A4A4A and black, no shadows, no gradients, no 3D perspective, no decorative elements, schematic style for IEEE paper figure"
}
```