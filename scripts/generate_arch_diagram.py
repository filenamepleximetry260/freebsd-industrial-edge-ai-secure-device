# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: Generates an updated architecture diagram for current project runtime.
import os

import graphviz


os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

dot = graphviz.Digraph(comment='Industrial Edge AI SOC - Architecture')
dot.attr(rankdir='LR', fontname='Arial', bgcolor='white', splines='spline')
dot.attr('node', fontname='Arial', fontsize='10', shape='box', style='rounded,filled', fillcolor='white')
dot.attr('edge', fontname='Arial', fontsize='9', color='#4B5563')


def cluster_attr(subgraph, label, color, fill):
    subgraph.attr(
        label=label,
        color=color,
        style='filled,rounded',
        fillcolor=fill,
        fontname='Arial',
        fontsize='12',
        penwidth='1.8',
    )


with dot.subgraph(name='cluster_edge') as c:
    cluster_attr(
        c,
        'Edge Runtime\nFreeBSD ARM64 in QEMU',
        '#1D4ED8',
        '#DBEAFE',
    )
    c.node('SIMFILE', '/tmp/sensor_data.txt\n(sensor feed)', fillcolor='#EFF6FF')
    c.node('SR', 'sensor_reader\n(C)', fillcolor='#EFF6FF')
    c.node('SM', 'security_monitor\n(C rules)', fillcolor='#EFF6FF')
    c.node('TD', 'telemetry_daemon\n(C sender)', fillcolor='#EFF6FF')
    c.edge('SIMFILE', 'SR', label='[4] read sensor file')
    c.edge('SR', 'SM', label='[5] pipe telemetry')
    c.edge('SM', 'TD', label='[6] validated JSON')

with dot.subgraph(name='cluster_platform') as c:
    cluster_attr(
        c,
        'Container Platform\nDocker Compose',
        '#0F766E',
        '#CCFBF1',
    )
    c.node('BACKEND', 'edge_ai_backend\ntelemetry_server:8080\nFastAPI:8000', fillcolor='#ECFEFF')
    c.node('FRONTEND', 'edge_ai_frontend\nVite Dashboard:3000', fillcolor='#ECFEFF')
    c.node('REDTEAM', 'edge_ai_redteam\nAdversarial Runtime', fillcolor='#ECFEFF')
    c.node('DB', 'SQLite\ndata/telemetry.db', shape='cylinder', fillcolor='#ECFEFF')
    c.edge('BACKEND', 'DB', label='[9] persist telemetry')
    c.edge('FRONTEND', 'BACKEND', label='[12] query REST /api')
    c.edge('REDTEAM', 'BACKEND', label='[11] attack simulation :8080')

with dot.subgraph(name='cluster_ai') as c:
    cluster_attr(
        c,
        'AI Detection Layer\nPython Modules',
        '#7C3AED',
        '#F3E8FF',
    )
    c.node('DP', 'data_processor.py', fillcolor='#FAF5FF')
    c.node('AD', 'anomaly_detection.py\nIsolation Forest', fillcolor='#FAF5FF')
    c.node('ATK', 'attack_detection.py\nHeuristic Rules', fillcolor='#FAF5FF')
    c.node('MODEL', 'data/isolation_forest.pkl', shape='cylinder', fillcolor='#FAF5FF')
    c.edge('DP', 'AD', label='[10a] anomaly scoring')
    c.edge('DP', 'ATK', label='[10b] attack checks')
    c.edge('AD', 'MODEL', label='[3] train/load model')

with dot.subgraph(name='cluster_ops') as c:
    cluster_attr(
        c,
        'Orchestration & Simulation\nHost Linux',
        '#B45309',
        '#FEF3C7',
    )
    c.node('ALLINONE', 'all_in_one.sh', fillcolor='#FFFBEB')
    c.node('SIM', 'simulation/machine_sim.py', fillcolor='#FFFBEB')
    c.node('DASH', 'scripts/run_dashboard.sh', fillcolor='#FFFBEB')
    c.node('REDRUN', 'scripts/run_redteam.sh', fillcolor='#FFFBEB')
    c.edge('ALLINONE', 'DASH', label='[1] start docker stack')
    c.edge('ALLINONE', 'REDRUN', label='[11] trigger redteam')
    c.edge('SIM', 'SIMFILE', label='[2] sensor updates', style='dashed')

dot.edge('TD', 'BACKEND', label='[7] TCP JSON :8080', color='#1E40AF', penwidth='1.4')
dot.edge('BACKEND', 'DP', label='[8] ingest pipeline', color='#7C3AED', penwidth='1.4')
dot.edge('DP', 'DB', label='[9b] stored records', color='#6B7280', penwidth='1.2')
dot.edge('ALLINONE', 'SR', label='[3b] QEMU automation', style='dashed', color='#92400E')
dot.edge('ALLINONE', 'BACKEND', label='[1b] compose up', style='dashed', color='#0F766E')

dot.render('docs/architecture', format='png', cleanup=True)
print('Generated docs/architecture.png with color-coded domains and Arial font.')
