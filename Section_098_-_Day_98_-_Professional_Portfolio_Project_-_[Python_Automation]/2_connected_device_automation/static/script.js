// static/script.js
let currentFilter = 'all';

function formatMac(mac) {
    return mac.toUpperCase().match(/.{1,2}/g).join(':');
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString();
}

function createDeviceCard(device) {
    const statusClass = device.status === 'connected' ? 'connected' : 'disconnected';
    
    return `
        <div class="device-card ${statusClass}">
            <div class="device-header">
                <span class="device-name">${device.hostname || 'Unknown Device'}</span>
                <span class="status-badge ${statusClass}">${device.status}</span>
            </div>
            <div class="device-details">
                <div class="detail-row">
                    <span class="detail-label">MAC:</span>
                    <span class="detail-value">${formatMac(device.mac)}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">IP:</span>
                    <span class="detail-value">${device.ip}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Vendor:</span>
                    <span class="detail-value"><span class="vendor-badge">${device.vendor}</span></span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">First Seen:</span>
                    <span class="detail-value">${formatDate(device.first_seen)}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Last Seen:</span>
                    <span class="detail-value">${formatDate(device.last_seen)}</span>
                </div>
            </div>
            <div class="device-footer">
                <span>Connections: ${device.connection_count}</span>
                <span>${device.ip_history.length > 1 ? '⚠️ IP changed' : ''}</span>
            </div>
        </div>
    `;
}

function filterDevices(devices) {
    if (currentFilter === 'connected') {
        return devices.filter(d => d.status === 'connected');
    } else if (currentFilter === 'disconnected') {
        return devices.filter(d => d.status === 'disconnected');
    }
    return devices;
}

function updateDisplay() {
    fetch('/api/devices')
        .then(response => response.json())
        .then(data => {
            // Update stats
            document.getElementById('total-devices').textContent = data.stats.total_devices;
            document.getElementById('connected-devices').textContent = data.stats.connected_devices;
            document.getElementById('disconnected-devices').textContent = data.stats.disconnected_devices;
            document.getElementById('last-scan').textContent = formatDate(data.stats.last_scan);

            // Update device grid
            const filteredDevices = filterDevices(data.devices);
            const grid = document.getElementById('device-grid');
            
            if (filteredDevices.length === 0) {
                grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 50px; background: #0a0a0a; border: 2px solid #ffd700; color: #ffd700; font-family: Courier New, monospace; border-radius: 0px; box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);">> NO DEVICES FOUND</div>';
            } else {
                grid.innerHTML = filteredDevices.map(createDeviceCard).join('');
            }
        })
        .catch(error => {
            console.error('Error fetching devices:', error);
        });
}

// Filter buttons
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        currentFilter = this.dataset.filter;
        updateDisplay();
    });
});

// Update every 2 seconds
setInterval(updateDisplay, 2000);
updateDisplay(); // Initial update