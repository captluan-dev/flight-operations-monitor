#!/bin/bash

echo "Iniciando coleta automática..."

cd /home/baianooo/Documentos/GitHub/flight-operations-monitor

export $(grep -v '^#' .env | xargs)

/home/baianooo/Documentos/GitHub/flight-operations-monitor/venv/bin/python collector/run_auto.py

echo "Finalizado!"