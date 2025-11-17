# Diagramas de Casos de Uso - Sistema Antivirus

## 🎯 Diagrama General de Casos de Uso

```plantuml
@startuml caso_uso_general
!define ICONURL https://raw.githubusercontent.com/tupadr3/plantuml-icon-font-sprites/master
!includeurl ICONURL/common.puml
!includeurl ICONURL/font-awesome-5/shield_alt.puml
!includeurl ICONURL/font-awesome-5/user.puml
!includeurl ICONURL/font-awesome-5/cog.puml

title Diagrama General de Casos de Uso - Sistema Antivirus

' Actores
:Usuario: as usuario
:Administrador: as admin
:Sistema: as sistema

' Casos de uso principales
rectangle "Sistema Antivirus Profesional" {
    
    ' Protección Core
    (Escaneo en Tiempo Real) as scan
    (Detección de Keylogger) as keylogger
    (Análisis de Comportamiento) as behavior
    (Respuesta a Incidentes) as response
    
    ' Gestión de Amenazas
    (Cuarentena de Archivos) as quarantine
    (Gestión de Amenazas) as threats
    (Whitelist/Blacklist) as lists
    
    ' Administración
    (Configuración del Sistema) as config
    (Actualización de Firmas) as updates
    (Generación de Reportes) as reports
}

' Relaciones Usuario
usuario --> threats
usuario --> quarantine
usuario --> lists
usuario --> reports

' Relaciones Administrador
admin --> config
admin --> reports
admin --> lists

' Relaciones Sistema
sistema --> scan
sistema --> keylogger
sistema --> behavior
sistema --> response
sistema --> updates

' Inclusiones
scan .> keylogger : <<include>>
scan .> behavior : <<include>>
threats .> quarantine : <<include>>
response .> quarantine : <<include>>

' Extensiones
keylogger .> response : <<extend>>
behavior .> response : <<extend>>
scan .> reports : <<extend>>

@enduml
```

---

## 🔍 CU-01: Escaneo en Tiempo Real

```plantuml
@startuml cu01_escaneo_tiempo_real
title CU-01: Escaneo en Tiempo Real

actor "Sistema" as sistema
participant "Motor Antivirus" as engine
participant "Detector Keylogger" as keydet
participant "Detector Comportamiento" as behdet
participant "Detector ML" as mldet
participant "Monitor Sistema" as monitor
participant "Interface Usuario" as ui

sistema -> engine : iniciar_escaneo()
activate engine

engine -> keydet : inicializar()
engine -> behdet : inicializar()
engine -> mldet : inicializar()
engine -> monitor : iniciar_monitoreo()

loop Monitoreo Continuo
    monitor -> engine : evento_sistema(proceso, archivo, red)
    
    par Análisis Paralelo
        engine -> keydet : analizar_evento(evento)
        keydet -> engine : score_keylogger
    and
        engine -> behdet : analizar_comportamiento(evento)
        behdet -> engine : score_comportamiento
    and
        engine -> mldet : predecir_amenaza(evento)
        mldet -> engine : score_ml
    end
    
    engine -> engine : calcular_score_total()
    
    alt Score > Umbral
        engine -> ui : mostrar_alerta(amenaza)
        engine -> sistema : ejecutar_respuesta()
    else Score Normal
        engine -> ui : actualizar_estadisticas()
    end
end

deactivate engine
@enduml
```

---

## 🔑 CU-02: Detección de Keylogger

```plantuml
@startuml cu02_deteccion_keylogger
title CU-02: Detección de Keylogger

actor "Sistema" as sistema
participant "Detector Keylogger" as detector
participant "Monitor Procesos" as procmon
participant "Analizador Archivos" as fileanalizer
participant "ML Engine" as ml
participant "Base Conocimiento" as kb

sistema -> detector : detectar_keyloggers()
activate detector

detector -> procmon : obtener_procesos_activos()
procmon -> detector : lista_procesos[]

loop Para cada proceso
    detector -> procmon : analizar_apis_proceso(pid)
    procmon -> detector : apis_utilizadas[]
    
    detector -> detector : verificar_hooks_teclado()
    detector -> detector : verificar_apis_sospechosas()
    
    alt APIs sospechosas detectadas
        detector -> fileanalizer : analizar_ejecutable(ruta)
        fileanalizer -> detector : metadata_archivo
        
        detector -> ml : predecir_keylogger(features)
        ml -> detector : probabilidad_malware
        
        detector -> kb : consultar_firmas(hash)
        kb -> detector : resultado_busqueda
        
        detector -> detector : calcular_score_final()
        
        alt Score > Umbral
            detector -> sistema : amenaza_detectada(keylogger_info)
        end
    end
end

deactivate detector
@enduml
```

---

## 🔒 CU-03: Cuarentena de Archivos

```plantuml
@startuml cu03_cuarentena_archivos
title CU-03: Cuarentena de Archivos

actor "Usuario/Sistema" as actor
participant "Handler Cuarentena" as handler
participant "Sistema Archivos" as fs
participant "Base Datos" as db
participant "Compresor" as zip
participant "Logger" as log

actor -> handler : cuarentena_archivo(ruta, razon)
activate handler

handler -> fs : verificar_archivo_existe(ruta)
alt Archivo no existe
    fs -> handler : error_no_existe
    handler -> actor : error("Archivo no encontrado")
else Archivo existe
    fs -> handler : archivo_valido
    
    handler -> fs : calcular_hash(archivo)
    fs -> handler : hash_sha256
    
    handler -> handler : generar_id_cuarentena()
    handler -> fs : crear_directorio_cuarentena(id)
    
    alt Compresion habilitada
        handler -> zip : comprimir_archivo(ruta)
        zip -> handler : archivo_comprimido
        handler -> fs : mover_a_cuarentena(archivo_comprimido)
    else Sin compresion
        handler -> fs : copiar_a_cuarentena(ruta)
    end
    
    handler -> db : guardar_metadata(id, ruta_original, hash, fecha, razon)
    handler -> fs : eliminar_archivo_original()
    handler -> log : registrar_cuarentena(detalles)
    
    handler -> actor : exito("Archivo en cuarentena")
end

deactivate handler
@enduml
```

---

## 🛡️ CU-04: Gestión de Amenazas

```plantuml
@startuml cu04_gestion_amenazas
title CU-04: Gestión de Amenazas

actor "Usuario" as usuario
participant "Threat Viewer" as viewer
participant "Motor Backend" as backend
participant "Handler Cuarentena" as quarantine
participant "Process Manager" as procmgr

usuario -> viewer : abrir_visor_amenazas()
activate viewer

viewer -> backend : obtener_amenazas_detectadas()
backend -> viewer : lista_amenazas[]

viewer -> usuario : mostrar_amenazas(lista)

usuario -> viewer : seleccionar_amenaza(id)
viewer -> backend : obtener_detalles_amenaza(id)
backend -> viewer : detalles_completos

viewer -> usuario : mostrar_opciones_accion()

alt Detener Proceso
    usuario -> viewer : detener_proceso()
    viewer -> procmgr : kill_process(pid)
    procmgr -> viewer : resultado_operacion
    
else Cuarentena
    usuario -> viewer : poner_cuarentena()
    viewer -> quarantine : cuarentena_archivo(ruta)
    quarantine -> viewer : resultado_cuarentena
    
else Agregar Whitelist
    usuario -> viewer : agregar_whitelist()
    viewer -> backend : actualizar_whitelist(elemento)
    backend -> viewer : whitelist_actualizada
    
else Ver Detalles
    usuario -> viewer : ver_detalles_tecnicos()
    viewer -> backend : obtener_analisis_completo(id)
    backend -> viewer : analisis_detallado
    viewer -> usuario : mostrar_analisis()
end

viewer -> backend : actualizar_estado_amenaza(id, accion)
viewer -> usuario : confirmar_accion_completada()

deactivate viewer
@enduml
```

---

## ⚙️ CU-05: Configuración del Sistema

```plantuml
@startuml cu05_configuracion_sistema
title CU-05: Configuración del Sistema

actor "Administrador" as admin
participant "Panel Config" as panel
participant "Validador Config" as validator
participant "Motor Antivirus" as engine
participant "Archivo Config" as config
participant "Logger" as log

admin -> panel : acceder_configuracion()
activate panel

panel -> config : cargar_configuracion_actual()
config -> panel : parametros_actuales

panel -> admin : mostrar_panel_configuracion()

admin -> panel : modificar_parametros(nuevos_valores)

panel -> validator : validar_configuracion(parametros)
activate validator

validator -> validator : verificar_rangos_valores()
validator -> validator : verificar_compatibilidad()
validator -> validator : estimar_impacto_rendimiento()

alt Configuracion Valida
    validator -> panel : configuracion_valida
    
    panel -> engine : aplicar_configuracion_runtime(parametros)
    engine -> panel : configuracion_aplicada
    
    panel -> config : guardar_configuracion_persistente()
    config -> panel : guardado_exitoso
    
    panel -> log : registrar_cambio_configuracion(admin, cambios)
    panel -> admin : exito("Configuración aplicada correctamente")
    
else Configuracion Invalida
    validator -> panel : errores_validacion[]
    panel -> admin : mostrar_errores(errores)
    panel -> admin : sugerir_correcciones()
end

deactivate validator
deactivate panel
@enduml
```

---

## 🧠 CU-06: Análisis de Comportamiento

```plantuml
@startuml cu06_analisis_comportamiento
title CU-06: Análisis de Comportamiento

actor "Sistema" as sistema
participant "Detector Comportamiento" as detector
participant "Recolector Métricas" as collector
participant "Analizador ML" as ml
participant "Base Patrones" as patterns
participant "Calculador Anomalías" as anomaly

sistema -> detector : iniciar_analisis_comportamiento()
activate detector

loop Análisis Continuo
    detector -> collector : recopilar_metricas_procesos()
    collector -> detector : metricas_sistema
    
    detector -> patterns : obtener_baseline_comportamiento()
    patterns -> detector : patrones_normales
    
    detector -> anomaly : detectar_anomalias(metricas, baseline)
    activate anomaly
    
    anomaly -> anomaly : calcular_desviaciones_estadisticas()
    anomaly -> anomaly : identificar_patrones_anormales()
    anomaly -> detector : score_anomalia
    
    deactivate anomaly
    
    detector -> ml : predecir_malware(features_comportamiento)
    ml -> detector : probabilidad_amenaza
    
    detector -> detector : combinar_scores(anomalia, ml)
    
    alt Score > Umbral Alto
        detector -> sistema : alerta_critica(detalles_comportamiento)
    else Score > Umbral Medio
        detector -> sistema : alerta_sospecha(detalles_comportamiento)
    else Score Normal
        detector -> patterns : actualizar_baseline(nuevas_metricas)
    end
end

deactivate detector
@enduml
```

---

## 📊 CU-07: Generación de Reportes

```plantuml
@startuml cu07_generacion_reportes
title CU-07: Generación de Reportes

actor "Usuario" as usuario
participant "Generator Reportes" as generator
participant "Base Datos Logs" as db
participant "Procesador Datos" as processor
participant "Visualizador" as visualizer
participant "Exportador" as exporter

usuario -> generator : solicitar_reporte(parametros)
activate generator

generator -> generator : validar_parametros(periodo, tipo, formato)

generator -> db : consultar_datos(filtros)
db -> generator : datos_brutos[]

generator -> processor : procesar_y_agregar(datos)
activate processor

processor -> processor : calcular_estadisticas()
processor -> processor : identificar_tendencias()
processor -> processor : generar_resumen_ejecutivo()
processor -> generator : datos_procesados

deactivate processor

generator -> visualizer : crear_visualizaciones(datos)
activate visualizer

visualizer -> visualizer : generar_graficos_amenazas()
visualizer -> visualizer : crear_tablas_estadisticas()
visualizer -> visualizer : diseñar_dashboard()
visualizer -> generator : elementos_visuales

deactivate visualizer

alt Formato HTML
    generator -> exporter : generar_html(datos, visuales)
    exporter -> generator : reporte_html
else Formato PDF
    generator -> exporter : generar_pdf(datos, visuales)
    exporter -> generator : reporte_pdf
else Formato JSON
    generator -> exporter : generar_json(datos)
    exporter -> generator : reporte_json
end

generator -> usuario : entregar_reporte(archivo_generado)
generator -> db : registrar_generacion_reporte(usuario, timestamp)

deactivate generator
@enduml
```

---

## 🔄 CU-08: Actualización de Firmas

```plantuml
@startuml cu08_actualizacion_firmas
title CU-08: Actualización de Firmas

actor "Sistema" as sistema
participant "Update Manager" as updater
participant "Servidor Central" as server
participant "Validador Integridad" as validator
participant "Aplicador Updates" as applier
participant "Motor Detección" as detector

sistema -> updater : verificar_actualizaciones_automaticas()
activate updater

updater -> updater : verificar_horario_programado()

alt Es hora de actualizar
    updater -> server : consultar_nuevas_definiciones()
    server -> updater : lista_actualizaciones_disponibles
    
    updater -> updater : comparar_versiones_locales()
    
    alt Hay actualizaciones
        loop Para cada actualización
            updater -> server : descargar_definicion(id)
            server -> updater : archivo_definicion
            
            updater -> validator : verificar_integridad(archivo, checksum)
            validator -> updater : validacion_resultado
            
            alt Archivo válido
                updater -> applier : aplicar_definicion(archivo)
                applier -> detector : recargar_detector(tipo)
                detector -> applier : detector_actualizado
                applier -> updater : aplicacion_exitosa
            else Archivo corrupto
                updater -> server : reportar_corrupcion(id)
                updater -> updater : intentar_descarga_backup()
            end
        end
        
        updater -> sistema : notificar_actualizacion_completa()
    else Sin actualizaciones
        updater -> sistema : sistema_actualizado()
    end
else Fuera de horario
    updater -> sistema : programar_proximo_intento()
end

deactivate updater
@enduml
```

---

## 📄 CU-09: Whitelist/Blacklist

```plantuml
@startuml cu09_whitelist_blacklist
title CU-09: Gestión de Whitelist/Blacklist

actor "Usuario" as usuario
participant "List Manager" as manager
participant "Validador Elementos" as validator
participant "Motor Detección" as detector
participant "Archivo Config" as config

usuario -> manager : acceder_gestion_listas()
activate manager

manager -> config : cargar_listas_actuales()
config -> manager : whitelist[], blacklist[]

manager -> usuario : mostrar_listas_existentes()

usuario -> manager : seleccionar_accion(tipo_accion, tipo_lista)

alt Agregar elemento
    usuario -> manager : agregar_elemento(ruta_o_hash, lista)
    
    manager -> validator : validar_elemento(elemento)
    activate validator
    
    validator -> validator : verificar_formato()
    validator -> validator : verificar_existencia()
    validator -> validator : verificar_no_critico_sistema()
    
    alt Elemento válido
        validator -> manager : elemento_valido
        
        manager -> config : actualizar_lista(elemento, lista)
        config -> manager : lista_actualizada
        
        manager -> detector : recargar_listas()
        detector -> manager : listas_sincronizadas
        
        manager -> usuario : exito("Elemento agregado")
    else Elemento inválido
        validator -> manager : errores_validacion[]
        manager -> usuario : mostrar_errores(errores)
    end
    
    deactivate validator
    
else Remover elemento
    usuario -> manager : remover_elemento(id, lista)
    
    manager -> config : eliminar_de_lista(id, lista)
    manager -> detector : recargar_listas()
    manager -> usuario : exito("Elemento removido")
    
else Modificar elemento
    usuario -> manager : modificar_elemento(id, nuevos_criterios)
    
    manager -> validator : validar_criterios(criterios)
    manager -> config : actualizar_elemento(id, criterios)
    manager -> detector : recargar_listas()
    manager -> usuario : exito("Elemento modificado")
end

deactivate manager
@enduml
```

---

## 🚨 CU-10: Respuesta a Incidentes

```plantuml
@startuml cu10_respuesta_incidentes
title CU-10: Respuesta a Incidentes

actor "Detector" as detector
participant "Response Engine" as engine
participant "Policy Manager" as policy
participant "Action Executor" as executor
participant "Quarantine Handler" as quarantine
participant "Process Manager" as procmgr
participant "Notificador" as notifier
participant "Logger" as log

detector -> engine : amenaza_detectada(amenaza_info)
activate engine

engine -> policy : obtener_politica_respuesta(tipo_amenaza, severidad)
policy -> engine : acciones_configuradas[]

engine -> engine : priorizar_acciones(acciones)

loop Para cada acción
    alt Acción: Cuarentena
        engine -> quarantine : cuarentena_automatica(archivo)
        quarantine -> engine : resultado_cuarentena
        
    else Acción: Detener Proceso
        engine -> procmgr : terminar_proceso(pid)
        procmgr -> engine : proceso_terminado
        
    else Acción: Bloquear Red
        engine -> executor : bloquear_conexiones(proceso)
        executor -> engine : conexiones_bloqueadas
        
    else Acción: Notificar Usuario
        engine -> notifier : enviar_alerta(detalles_amenaza)
        notifier -> engine : notificacion_enviada
        
    else Acción: Escalamiento
        engine -> notifier : notificar_administrador(incidente_critico)
        notifier -> engine : escalamiento_enviado
    end
    
    engine -> log : registrar_accion(accion, resultado, timestamp)
end

engine -> engine : generar_resumen_respuesta()
engine -> log : registrar_incidente_completo(resumen)

alt Respuesta exitosa
    engine -> detector : incidente_resuelto(id)
else Respuesta parcial
    engine -> detector : incidente_contenido(acciones_fallidas)
    engine -> notifier : solicitar_intervencion_manual()
end

deactivate engine
@enduml
```

---

## 🔄 Diagrama de Interacciones entre Casos de Uso

```plantuml
@startuml interacciones_casos_uso
title Interacciones entre Casos de Uso

' Casos de uso
(Escaneo Tiempo Real) as scan
(Detección Keylogger) as keylogger
(Análisis Comportamiento) as behavior
(Respuesta Incidentes) as response
(Cuarentena Archivos) as quarantine
(Gestión Amenazas) as threats
(Configuración Sistema) as config
(Actualización Firmas) as updates
(Whitelist/Blacklist) as lists
(Generación Reportes) as reports

' Interacciones principales
scan --> keylogger : activa
scan --> behavior : activa
keylogger --> response : dispara
behavior --> response : dispara
response --> quarantine : ejecuta
response --> threats : notifica
threats --> quarantine : solicita
threats --> lists : modifica
config --> scan : configura
config --> keylogger : ajusta umbrales
config --> behavior : define parámetros
updates --> keylogger : actualiza firmas
updates --> behavior : actualiza modelos
lists --> keylogger : aplica exclusiones
lists --> behavior : aplica exclusiones
scan --> reports : genera datos
threats --> reports : aporta estadísticas
response --> reports : contribuye métricas

' Dependencias
scan ..> config : depende
keylogger ..> updates : depende
behavior ..> updates : depende
quarantine ..> config : depende
response ..> config : depende

@enduml
```

---

## 📈 Métricas y KPIs de Casos de Uso

```plantuml
@startuml metricas_casos_uso
!define RECTANGLE class

title Métricas de Rendimiento por Caso de Uso

RECTANGLE "CU-01: Escaneo Tiempo Real" {
  + Uptime: >99.5%
  + CPU Usage: <5%
  + Memory Usage: <200MB
  + Response Time: <2s
}

RECTANGLE "CU-02: Detección Keylogger" {
  + Detection Rate: >95%
  + False Positives: <5%
  + Analysis Time: <1s
  + Coverage: 25+ indicators
}

RECTANGLE "CU-03: Cuarentena" {
  + Quarantine Time: <5s
  + Storage Efficiency: 70%
  + Recovery Success: >99%
  + Integrity Check: SHA256
}

RECTANGLE "CU-04: Gestión Amenazas" {
  + UI Response: <2s
  + Action Success: >98%
  + User Satisfaction: >4.5/5
  + Workflow Time: <30s
}

RECTANGLE "CU-05: Configuración" {
  + Apply Time: <1s
  + Validation Accuracy: 100%
  + Rollback Success: >99%
  + User Errors: <2%
}

RECTANGLE "CU-06: Análisis Comportamiento" {
  + Anomaly Detection: >90%
  + False Positives: <10%
  + Processing Delay: <3s
  + Pattern Recognition: ML-based
}

RECTANGLE "CU-07: Reportes" {
  + Generation Time: <30s
  + Data Accuracy: >99%
  + Export Success: >98%
  + Format Support: 3 types
}

RECTANGLE "CU-08: Updates" {
  + Update Frequency: Daily
  + Download Success: >99%
  + Apply Time: <60s
  + Rollback Capability: Yes
}

RECTANGLE "CU-09: Lists Management" {
  + Rule Application: Immediate
  + Validation Accuracy: 100%
  + Performance Impact: <1%
  + User Flexibility: High
}

RECTANGLE "CU-10: Respuesta Incidentes" {
  + Response Time: <3s
  + Action Success: >95%
  + Escalation Rate: <5%
  + Recovery Time: <10s
}

@enduml
```