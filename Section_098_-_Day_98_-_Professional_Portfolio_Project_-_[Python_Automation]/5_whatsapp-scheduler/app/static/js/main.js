// Show/hide fields based on schedule type
document.addEventListener('DOMContentLoaded', function() {
    const scheduleRadios = document.querySelectorAll('input[name="schedule_type"]');
    const onceDailyDiv = document.getElementById('once-daily-fields');
    const intervalDiv = document.getElementById('interval-fields');

    function toggleFields() {
        const selected = document.querySelector('input[name="schedule_type"]:checked').value;
        onceDailyDiv.style.display = (selected === 'once' || selected === 'daily') ? 'block' : 'none';
        intervalDiv.style.display = (selected === 'interval') ? 'block' : 'none';
    }

    scheduleRadios.forEach(radio => {
        radio.addEventListener('change', toggleFields);
    });
    toggleFields(); // initial call
});

// Text formatting for WhatsApp
function formatText(type) {
    const textarea = document.getElementById('messageBox');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selected = textarea.value.substring(start, end);
    let replacement = '';

    switch(type) {
        case 'bold':
            replacement = `*${selected}*`;
            break;
        case 'italic':
            replacement = `_${selected}_`;
            break;
        case 'strike':
            replacement = `~${selected}~`;
            break;
        case 'code':
            replacement = `\`\`\`${selected}\`\`\``;
            break;
        default:
            return;
    }

    textarea.value = textarea.value.substring(0, start) + replacement + textarea.value.substring(end);
    textarea.selectionStart = start;
    textarea.selectionEnd = start + replacement.length;
    textarea.focus();
}