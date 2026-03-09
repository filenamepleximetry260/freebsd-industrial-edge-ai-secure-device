# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: 
import graphviz
import os

# Adicionamos cd no root do projeto se rodado via linha de comando
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

dot = graphviz.Digraph(comment='System Architecture')
dot.graph_attr['rankdir'] = 'TD'

with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Emulated Edge Device\\n[FreeBSD ARM64 (QEMU Virtual Machine)]')
    c.node('sim_data', '/tmp/sensor_data.txt\\n(Machine Simulator)', shape='cylinder')
    with c.subgraph(name='cluster_1') as c1:
        c1.attr(label='Embedded C Layer')
        c1.node('SR', 'sensor_reader')
        c1.node('TD', 'telemetry_daemon')
        c1.node('SM', 'security_monitor')
    
    c.edge('sim_data', 'SR', label='Reads', style='dashed')
    c.edge('SR', 'TD', label='Pipe')
    c.edge('TD', 'SM', label='Check Rules', style='dashed')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Host Linux Environment\\n[Ubuntu / Debian Host]')
    with c.subgraph(name='cluster_3') as c3:
        c3.attr(label='Python Backend')
        c3.node('TS', 'telemetry_server.py')
        c3.node('DP', 'data_processor.py')
        c3.node('DB', 'telemetry.db\\n(SQLite3)', shape='cylinder')
    with c.subgraph(name='cluster_4') as c4:
        c4.attr(label='AI / Analytics Layer')
        c4.node('AD', 'anomaly_detection.py\\n(Isolation Forest)')
        c4.node('ATK', 'attack_detection.py\\n(Heuristics)')
    with c.subgraph(name='cluster_5') as c5:
        c5.attr(label='Red Team / Simulation')
        c5.node('MS', 'machine_sim.py')
        c5.node('SS', 'sensor_spoof.py')
        c5.node('TI', 'telemetry_injection.py')

dot.edge('TD', 'TS', label='TCP Port 8080 (JSON Packet)')
dot.edge('TS', 'DP')
dot.edge('DP', 'DB')
dot.edge('DP', 'AD', label='Real-time triggers')
dot.edge('DP', 'ATK', label='Real-time triggers')

dot.edge('MS', 'sim_data', label='Generates data', style='dashed')
dot.edge('SS', 'sim_data', label='Spoofs data', style='dashed')
dot.edge('TI', 'TS', label='Malicious Injection TCP 8080')

dot.render('docs/architecture', format='png', cleanup=True)
