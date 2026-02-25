let charts = {};

function createOrUpdateChart(ctx, type, data, options) {
    if (charts[ctx.canvas.id]) {
        charts[ctx.canvas.id].data = data;
        charts[ctx.canvas.id].update();
    } else {
        charts[ctx.canvas.id] = new Chart(ctx, { type, data, options });
    }
}

function renderDashboard(data) {
    const d = data;
    let html = '<div class="grid">';

    // ---------- System Info ----------
    html += '<div class="card"><h3 class="card-title">System</h3>';
    html += `<p>Host: ${d.system.hostname}<br>OS: ${d.system.system}<br>`;
    html += `Uptime: ${Math.floor(d.system.uptime_seconds / 3600)}h ${Math.floor((d.system.uptime_seconds % 3600)/60)}m<br>`;
    html += `Boot: ${d.system.boot_time}<br>Users: ${d.system.users.length}</p></div>`;

    // ---------- CPU ----------
    html += '<div class="card"><h3 class="card-title">CPU</h3>';
    html += `<p>Overall: ${d.cpu.percent}%</p>`;
    html += '<div class="progress-bar"><div class="progress-fill" style="width:' + d.cpu.percent + '%">' + d.cpu.percent + '%</div></div>';
    html += '<canvas id="chart-cpu" class="chart-container"></canvas>';
    html += '</div>';

    // ---------- Memory ----------
    html += '<div class="card"><h3 class="card-title">Memory</h3>';
    let mem = d.memory.virtual;
    html += `<p>RAM: ${mem.percent}% used (${(mem.used/1e9).toFixed(2)}GB / ${(mem.total/1e9).toFixed(2)}GB)</p>`;
    html += '<div class="progress-bar"><div class="progress-fill" style="width:' + mem.percent + '%">' + mem.percent + '%</div></div>';
    if (d.memory.swap.total > 0) {
        html += `<p>Swap: ${d.memory.swap.percent}%</p>`;
    }
    html += '</div>';

    // ---------- Disk ----------
    html += '<div class="card"><h3 class="card-title">Disk</h3>';
    d.disk.partitions.forEach(p => {
        html += `<p><strong>${p.mountpoint}</strong> (${p.fstype})<br>`;
        html += `${p.percent}% used (${p.used} / ${p.total})</p>`;
        html += '<div class="progress-bar"><div class="progress-fill" style="width:' + p.percent + '%">' + p.percent + '%</div></div>';
    });
    html += '</div>';

    // ---------- Network ----------
    html += '<div class="card"><h3 class="card-title">Network</h3>';
    html += `<p>Bytes sent: ${(d.network.io.bytes_sent/1e6).toFixed(2)} MB<br>`;
    html += `Bytes recv: ${(d.network.io.bytes_recv/1e6).toFixed(2)} MB<br>`;
    html += `Active connections: ${d.network.connections}</p>`;
    html += '</div>';

    // ---------- Processes ----------
    html += '<div class="card"><h3 class="card-title">Top 5 CPU</h3><table><tr><th>PID</th><th>Name</th><th>CPU%</th></tr>';
    d.processes.cpu_top.forEach(p => {
        html += `<tr><td>${p.pid}</td><td>${p.name}</td><td>${p.cpu_percent.toFixed(1)}</td></tr>`;
    });
    html += '</table></div>';

    html += '<div class="card"><h3 class="card-title">Top 5 MEM</h3><table><tr><th>PID</th><th>Name</th><th>MEM%</th></tr>';
    d.processes.mem_top.forEach(p => {
        html += `<tr><td>${p.pid}</td><td>${p.name}</td><td>${p.memory_percent.toFixed(1)}</td></tr>`;
    });
    html += '</table></div>';

    // ---------- Sensors ----------
    if (d.sensors.temperatures) {
        html += '<div class="card"><h3 class="card-title">Temperatures</h3>';
        for (let [name, entries] of Object.entries(d.sensors.temperatures)) {
            entries.forEach(e => {
                html += `<p>${name}: ${e.current}°C</p>`;
            });
        }
        html += '</div>';
    }
    if (d.sensors.battery) {
        let b = d.sensors.battery;
        html += '<div class="card"><h3 class="card-title">Battery</h3>';
        html += `<p>${b.percent}% ${'power_plugged' in b ? (b.power_plugged ? '(charging)' : '(discharging)') : ''}</p>`;
        html += '</div>';
    }

    html += '</div>'; // close grid
    $('#dashboard').html(html);

    // Update charts after DOM is ready
    const cpuCtx = document.getElementById('chart-cpu')?.getContext('2d');
    if (cpuCtx) {
        createOrUpdateChart(cpuCtx, 'bar', {
            labels: d.cpu.per_cpu.map((_, i) => `Core ${i}`),
            datasets: [{
                label: 'CPU Usage %',
                data: d.cpu.per_cpu,
                backgroundColor: '#00ff00',
                borderColor: '#00aa00',
                borderWidth: 1
            }]
        }, {
            scales: { y: { beginAtZero: true, max: 100 } },
            plugins: { legend: { display: false } }
        });
    }
}

function fetchStats() {
    $.getJSON('/api/stats', renderDashboard);
}

$(document).ready(function() {
    fetchStats();
    setInterval(fetchStats, 2000);
});
