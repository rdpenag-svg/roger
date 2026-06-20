#!/bin/bash

# Variables (configuración fácil de cambiar)
DB_FILE="database.db"
BACKUP_DIR="backups"
RETENTION_DAYS=7
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="backup_${TIMESTAMP}.tar.gz"

# Función para imprimir mensajes con hora
log() {
    echo "[ $(date +"%H:%M:%S")] $1"
}

log "Iniciando backup..."

# Verificar que la base de datos exista
if [ ! -f "$DB_FILE" ]; then
    log "ERROR: No se encontró $DB_FILE"
    exit 1
fi

# Crear carpeta de backups si no existe
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
fi

# Crear el backup comprimido
tar -czf "$BACKUP_DIR/$BACKUP_FILE" "$DB_FILE"

# Verificar si la compresión fue exitosa
if [ $? -eq 0 ]; then
    log "OK: Backup creado exitosamente."
else
    log "ERROR: Falló la creación del backup."
    exit 1
fi

# Limpiar backups de más de 7 días
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
log "Limpieza completada. Backups existentes: $(ls $BACKUP_DIR/*.tar.gz 2>/dev/null | wc -l)"
log "Proceso finalizado."
exit 0
