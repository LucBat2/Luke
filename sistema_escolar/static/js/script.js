function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Login successful") {
            document.getElementById('login-container').style.display = 'none';
            document.getElementById('main-container').style.display = 'block';
        } else {
            document.getElementById('login-message').textContent = data.message;
        }
    });
}

function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.style.display = 'none');
    document.getElementById(tabName).style.display = 'block';
}

function savePresence() {
    const presenceData = [
        { Aluno: "Aluno 1", Matrícula: "12345", Data: "2025-01-17", Status: true },
        { Aluno: "Aluno 2", Matrícula: "67890", Data: "2025-01-17", Status: false }
    ];
    
    fetch('/presence', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(presenceData)
    })
    .then(response => response.json())
    .then(data => alert(data.message));
}

function saveObservations() {
    const observationsData = [
        { Aluno: "Aluno 1", Matrícula: "12345", Data: "2025-01-17", Status: "Participou bem" },
        { Aluno: "Aluno 2", Matrícula: "67890", Data: "2025-01-17", Status: "Faltou" }
    ];
    
    fetch('/observations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(observationsData)
    })
    .then(response => response.json())
    .then(data => alert(data.message));
}

function saveActivities() {
    const activitiesData = [
        { Aluno: "Aluno 1", Matrícula: "12345", Data: "2025-01-17", Status: "Atividade 1" },
        { Aluno: "Aluno 2", Matrícula: "67890", Data: "2025-01-17", Status: "Atividade 2" }
    ];
    
    fetch('/activities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(activitiesData)
    })
    .then(response => response.json())
    .then(data => alert(data.message));
}

function generateReport() {
    fetch('/report')
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('report-chart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(item => item.Aluno),
                datasets: [{
                    label: 'Presença',
                    data: data.map(item => item.Status),
                    backgroundColor: 'rgba(0, 123, 255, 0.5)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
}