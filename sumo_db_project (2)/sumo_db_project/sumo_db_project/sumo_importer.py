
#Importador de datos SUMO a PostgreSQL/TimescaleDB
#Versión corregida para Railway (sin TimescaleDB)


import xml.etree.ElementTree as ET
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import sys

class SumoImporter:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
        self.cur = self.conn.cursor()
        self.run_id = None
        self.simulation_start = datetime.now()
        
    def create_simulation_run(self, run_name, config_file=None):
        ##Crear registro de simulación
        self.cur.execute("""
            INSERT INTO simulation_runs (run_name, start_time, config_file, status)
            VALUES (%s, %s, %s, 'running')
            RETURNING run_id
        """, (run_name, self.simulation_start, config_file))
        
        self.run_id = self.cur.fetchone()[0]
        self.conn.commit()
        print(f"✓ Simulación creada: run_id={self.run_id}, name={run_name}")
        
    def get_period(self, hour):
        """Determinar período del día"""
        if 0 <= hour < 5:
            return 'MADRUGADA'
        elif 5 <= hour < 7:
            return 'MAÑANA'
        elif 7 <= hour < 9:
            return 'PICO_AM'
        elif 9 <= hour < 17:
            return 'DIA'
        elif 17 <= hour < 19:
            return 'PICO_PM'
        else:
            return 'NOCHE'
    
    def safe_float(self, value, default=0.0):
        """Convertir a float de forma segura"""
        if value is None or value == '':
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def safe_int(self, value, default=0):
        """Convertir a int de forma segura"""
        if value is None or value == '':
            return default
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return default
    
    def safe_bool(self, value):
        """Convertir a bool de forma segura"""
        if value is None:
            return False
        return str(value).lower() in ('true', '1', 'yes')
    
    def parse_tripinfo(self, xml_file):
        """Parsear tripinfos.xml"""
        print(f"→ Procesando {xml_file}...")
        
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except Exception as e:
            print(f"  ✗ Error leyendo XML: {e}")
            return
        
        trips = []
        
        for tripinfo in root.findall('tripinfo'):
            # Obtener depart y calcular timestamp
            depart = self.safe_float(tripinfo.get('depart'))
            trip_time = self.simulation_start + timedelta(seconds=depart)
            hour = trip_time.hour
            period = self.get_period(hour)
            
            trip_data = (
                trip_time,
                self.run_id,
                tripinfo.get('id', 'unknown'),
                tripinfo.get('vType', 'unknown'),
                depart,
                self.safe_float(tripinfo.get('arrival')),
                self.safe_float(tripinfo.get('duration')),
                self.safe_float(tripinfo.get('routeLength')),
                self.safe_float(tripinfo.get('waitingTime')),
                self.safe_float(tripinfo.get('timeLoss')),
                self.safe_float(tripinfo.get('speedFactor', 1.0)),  # avg_speed aproximado
                self.safe_float(tripinfo.get('vaporized', 0)),  # max_speed (no disponible)
                depart,  # departed (mismo que depart)
                self.safe_float(tripinfo.get('arrival')),  # arrived
                self.safe_bool(tripinfo.get('vaporized')),
                period,
                self.safe_float(tripinfo.get('departDelay')),
                self.safe_float(tripinfo.get('stopTime'))
            )
            
            trips.append(trip_data)
        
        if trips:
            self._insert_trips_batch(trips)
            print(f"  ✓ {len(trips)} viajes procesados exitosamente")
        else:
            print(f"  ⚠ No se encontraron viajes en el archivo")
    
    def _insert_trips_batch(self, trips):
        """Insertar viajes en batch"""
        execute_batch(self.cur, """
            INSERT INTO vehicle_trips (
                time, run_id, vehicle_id, vehicle_type, depart, arrival, duration,
                route_length, waiting_time, time_loss, avg_speed, max_speed,
                departed, arrived, vaporized, period, depart_delay, stop_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, trips)
        self.conn.commit()
    
    def parse_edge_data(self, xml_file):
        """Parsear edgeData.xml"""
        print(f"→ Procesando {xml_file}...")
        
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except Exception as e:
            print(f"  ✗ Error leyendo XML: {e}")
            return
        
        edge_records = []
        
        for interval in root.findall('interval'):
            begin = self.safe_float(interval.get('begin'))
            timestamp = self.simulation_start + timedelta(seconds=begin)
            
            for edge in interval.findall('edge'):
                edge_data = (
                    timestamp,
                    self.run_id,
                    edge.get('id'),
                    begin,
                    self.safe_float(interval.get('end', begin)),
                    self.safe_int(self.safe_float(edge.get('sampledSeconds', 0))),
                    self.safe_float(edge.get('speed')),
                    self.safe_float(edge.get('occupancy')),
                    self.safe_float(edge.get('density')),
                    self.safe_float(edge.get('waitingTime')),
                    self.safe_float(edge.get('traveltime'))
                )
                edge_records.append(edge_data)
        
        if edge_records:
            self._insert_edges_batch(edge_records)
            print(f"  ✓ {len(edge_records)} registros de calles procesados")
        else:
            print(f"  ⚠ No se encontraron datos de calles")
    
    def _insert_edges_batch(self, edges):
        """Insertar datos de edges en batch"""
        execute_batch(self.cur, """
            INSERT INTO edge_data (
                time, run_id, edge_id, begin_time, end_time, num_vehicles,
                avg_speed, avg_occupancy, avg_density, avg_waiting_time, avg_travel_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, edges)
        self.conn.commit()
    
    def parse_stats(self, xml_file):
        """Parsear stats.xml"""
        print(f"→ Procesando {xml_file}...")
        
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except Exception as e:
            print(f"  ✗ Error leyendo XML: {e}")
            return
        
        stats_records = []
        
        for step in root.findall('step'):
            step_time = self.safe_float(step.get('time'))
            timestamp = self.simulation_start + timedelta(seconds=step_time)
            
            stat_data = (
                timestamp,
                self.run_id,
                self.safe_int(step_time),
                self.safe_int(step.get('loaded')),
                self.safe_int(step.get('inserted')),
                self.safe_int(step.get('running')),
                self.safe_int(step.get('waiting')),
                self.safe_int(step.get('ended')),
                self.safe_int(step.get('arrived')),
                self.safe_int(step.get('collisions')),
                self.safe_int(step.get('teleports')),
                self.safe_float(step.get('totalTravelTime')),
                self.safe_float(step.get('totalWaitingTime'))
            )
            stats_records.append(stat_data)
        
        if stats_records:
            self._insert_stats_batch(stats_records)
            print(f"  ✓ {len(stats_records)} pasos de estadísticas procesados")
        else:
            print(f"  ⚠ No se encontraron estadísticas")
    
    def _insert_stats_batch(self, stats):
        """Insertar estadísticas en batch"""
        execute_batch(self.cur, """
            INSERT INTO simulation_stats (
                time, run_id, step, vehicles_loaded, vehicles_inserted,
                vehicles_running, vehicles_waiting, vehicles_ended, vehicles_arrived,
                vehicles_collisions, vehicles_teleports, total_travel_time, total_waiting_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, stats)
        self.conn.commit()
    
    def parse_stopinfo(self, xml_file):
        """Parsear stopinfos.xml"""
        print(f"→ Procesando {xml_file}...")
        
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except Exception as e:
            print(f"  ✗ Error leyendo XML: {e}")
            return
        
        stop_records = []
        
        for stopinfo in root.findall('stopinfo'):
            until = self.safe_float(stopinfo.get('until'))
            timestamp = self.simulation_start + timedelta(seconds=until)
            
            stop_data = (
                timestamp,
                self.run_id,
                stopinfo.get('id'),
                stopinfo.get('vehicle'),
                self.safe_float(stopinfo.get('delay')),
                self.safe_int(stopinfo.get('loaded')),
                self.safe_int(stopinfo.get('unloaded')),
                self.safe_int(stopinfo.get('loadedPersons'))
            )
            stop_records.append(stop_data)
        
        if stop_records:
            self._insert_stops_batch(stop_records)
            print(f"  ✓ {len(stop_records)} paradas procesadas")
        else:
            print(f"  ⚠ No se encontraron paradas de transporte público")
    
    def _insert_stops_batch(self, stops):
        """Insertar paradas en batch"""
        execute_batch(self.cur, """
            INSERT INTO pt_stops (
                time, run_id, stop_id, vehicle_id, delay,
                passengers_loaded, passengers_unloaded, passengers_count
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, stops)
        self.conn.commit()
    
    def finalize_simulation(self):
        """Finalizar simulación"""
        self.cur.execute("""
            UPDATE simulation_runs 
            SET end_time = %s, status = 'completed'
            WHERE run_id = %s
        """, (datetime.now(), self.run_id))
        self.conn.commit()
        print(f"✓ Simulación {self.run_id} finalizada")
    
    def close(self):
        """Cerrar conexión"""
        self.cur.close()
        self.conn.close()

def main():
    parser = argparse.ArgumentParser(description='Importar datos SUMO a PostgreSQL')
    parser.add_argument('--dir', required=True, help='Directorio con archivos XML de SUMO')
    parser.add_argument('--run-name', required=True, help='Nombre de la simulación')
    parser.add_argument('--host', default='localhost', help='Host de PostgreSQL')
    parser.add_argument('--port', default='5432', help='Puerto de PostgreSQL')
    parser.add_argument('--database', default='sumo_traffic', help='Nombre de la base de datos')
    parser.add_argument('--user', default='postgres', help='Usuario de PostgreSQL')
    parser.add_argument('--password', default='sumo123', help='Contraseña de PostgreSQL')
    
    args = parser.parse_args()
    
    db_config = {
        'host': args.host,
        'port': args.port,
        'database': args.database,
        'user': args.user,
        'password': args.password
    }
    
    data_dir = Path(args.dir)
    if not data_dir.exists():
        print(f"✗ ERROR: Directorio no existe: {data_dir}")
        sys.exit(1)
    
    files_to_parse = {
        'tripinfos.xml': 'parse_tripinfo',
        'edgeData.xml': 'parse_edge_data',
        'stats.xml': 'parse_stats',
        'stopinfos.xml': 'parse_stopinfo'
    }
    
    try:
        importer = SumoImporter(db_config)
        importer.create_simulation_run(args.run_name)
        
        for filename, parse_func in files_to_parse.items():
            file_path = data_dir / filename
            if file_path.exists():
                getattr(importer, parse_func)(str(file_path))
            else:
                print(f"  ⚠ Archivo no encontrado: {filename}")
        
        importer.finalize_simulation()
        
        print("\n" + "="*60)
        print("✓ IMPORTACIÓN COMPLETADA EXITOSAMENTE")
        print("="*60)
        print(f"\nPuedes ver los datos con:")
        print(f"  psql -h {args.host} -U {args.user} -d {args.database}")
        print(f"\nO conectarte a pgAdmin en http://localhost:5050")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        importer.close()

if __name__ == '__main__':
    main()