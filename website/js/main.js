document.addEventListener('DOMContentLoaded', () => {
    // Initial load
    fetchStats();
    fetchLeaderboard();

    // Auto refresh leaderboard every 30s
    setInterval(fetchLeaderboard, 30000);

    // Initialize parallax effect
    initParallax();
});

// --- API FUNCTIONS ---
const API_URL = window.location.hostname === 'localhost' ? 'http://localhost:5000/api' : 'https://flappybird-duatop.onrender.com/api';

async function fetchStats() {
    try {
        const response = await fetch(`${API_URL}/stats`);
        const data = await response.json();

        animateValue("total-players", 0, data.total_players, 2000);
        animateValue("total-games", 0, data.total_games, 2000);

        // Update highest score separately (no animation for now or simple text)
        document.getElementById('highest-score').textContent = data.highest_score;

    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

async function fetchLeaderboard() {
    try {
        const response = await fetch(`${API_URL}/scores`);
        const data = await response.json();
        renderLeaderboard(data);
    } catch (error) {
        console.error('Error fetching leaderboard:', error);
        document.getElementById('leaderboard-list').innerHTML = `
            <tr><td colspan="4" class="text-center">Không thể tải bảng xếp hạng</td></tr>
        `;
    }
}

// --- UI FUNCTIONS ---

function renderLeaderboard(data) {
    const list = document.getElementById('leaderboard-list');
    list.innerHTML = '';

    if (data.length === 0) {
        list.innerHTML = '<tr><td colspan="4" style="text-align:center">Chưa có dữ liệu</td></tr>';
        return;
    }

    data.forEach((player, index) => {
        const rank = index + 1;
        let rankClass = '';
        let medal = '';

        if (rank === 1) {
            rankClass = 'rank-1';
            medal = '<i class="fa-solid fa-medal" style="color: #FFD700;"></i>';
        } else if (rank === 2) {
            rankClass = 'rank-2';
            medal = '<i class="fa-solid fa-medal" style="color: #C0C0C0;"></i>';
        } else if (rank === 3) {
            rankClass = 'rank-3';
            medal = '<i class="fa-solid fa-medal" style="color: #CD7F32;"></i>';
        }

        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="${rankClass}">#${rank}</td>
            <td style="font-weight: 600;">${player.username}</td>
            <td style="font-family: 'Press Start 2P'; font-size: 0.8rem; color: var(--primary);">${player.score}</td>
            <td>${medal}</td>
        `;
        list.appendChild(row);
    });
}

// --- ANIMATION UTILS ---
function animateValue(id, start, end, duration) {
    if (start === end) return;
    const obj = document.getElementById(id);
    const range = end - start;
    const minTimer = 50;
    let stepTime = Math.abs(Math.floor(duration / range));

    stepTime = Math.max(stepTime, minTimer);

    let startTime = new Date().getTime();
    let endTime = startTime + duration;
    let timer;

    function run() {
        let now = new Date().getTime();
        let remaining = Math.max((endTime - now) / duration, 0);
        let value = Math.round(end - (remaining * range));
        obj.innerHTML = value;
        if (value == end) {
            clearInterval(timer);
        }
    }

    timer = setInterval(run, stepTime);
    run();
}

// --- PARALLAX EFFECT ---
function initParallax() {
    const stars = document.querySelectorAll('.star');
    const bird = document.querySelector('.bird-float');

    document.addEventListener('mousemove', (e) => {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;

        // Move stars in opposite direction (subtle)
        stars.forEach((star, index) => {
            const speed = (index + 1) * 0.5;
            const x = (mouseX - 0.5) * speed * -20;
            const y = (mouseY - 0.5) * speed * -20;
            star.style.transform = `translate(${x}px, ${y}px)`;
        });

        // Move bird slightly
        if (bird) {
            const x = (mouseX - 0.5) * 10;
            document.addEventListener('DOMContentLoaded', () => {
                // Initial load
                fetchStats();
                fetchLeaderboard();

                // Auto refresh leaderboard every 30s
                setInterval(fetchLeaderboard, 30000);

                // Initialize parallax effect
                initParallax();
            });

            // --- API FUNCTIONS ---
            const API_URL = window.location.hostname === 'localhost' ? 'http://localhost:5000/api' : 'https://flappybird-duatop.onrender.com/api';

            async function fetchStats() {
                try {
                    const response = await fetch(`${API_URL}/stats`);
                    const data = await response.json();

                    animateValue("total-players", 0, data.total_players, 2000);
                    animateValue("total-games", 0, data.total_games, 2000);

                    // Update highest score separately (no animation for now or simple text)
                    document.getElementById('highest-score').textContent = data.highest_score;

                } catch (error) {
                    console.error('Error fetching stats:', error);
                }
            }

            async function fetchLeaderboard() {
                try {
                    const response = await fetch(`${API_URL}/scores`);
                    const data = await response.json();
                    renderLeaderboard(data);
                } catch (error) {
                    console.error('Error fetching leaderboard:', error);
                    document.getElementById('leaderboard-list').innerHTML = `
            <tr><td colspan="4" class="text-center">Không thể tải bảng xếp hạng</td></tr>
        `;
                }
            }

            // --- UI FUNCTIONS ---

            function renderLeaderboard(data) {
                const list = document.getElementById('leaderboard-list');
                list.innerHTML = '';

                if (data.length === 0) {
                    list.innerHTML = '<tr><td colspan="4" style="text-align:center">Chưa có dữ liệu</td></tr>';
                    return;
                }

                data.forEach((player, index) => {
                    const rank = index + 1;
                    let rankClass = '';
                    let medal = '';

                    if (rank === 1) {
                        rankClass = 'rank-1';
                        medal = '<i class="fa-solid fa-medal" style="color: #FFD700;"></i>';
                    } else if (rank === 2) {
                        rankClass = 'rank-2';
                        medal = '<i class="fa-solid fa-medal" style="color: #C0C0C0;"></i>';
                    } else if (rank === 3) {
                        rankClass = 'rank-3';
                        medal = '<i class="fa-solid fa-medal" style="color: #CD7F32;"></i>';
                    }

                    const row = document.createElement('tr');
                    row.innerHTML = `
            <td class="${rankClass}">#${rank}</td>
            <td style="font-weight: 600;">${player.username}</td>
            <td style="font-family: 'Press Start 2P'; font-size: 0.8rem; color: var(--primary);">${player.score}</td>
            <td>${medal}</td>
        `;
                    list.appendChild(row);
                });
            }

            // --- ANIMATION UTILS ---
            function animateValue(id, start, end, duration) {
                if (start === end) return;
                const obj = document.getElementById(id);
                const range = end - start;
                const minTimer = 50;
                let stepTime = Math.abs(Math.floor(duration / range));

                stepTime = Math.max(stepTime, minTimer);

                let startTime = new Date().getTime();
                let endTime = startTime + duration;
                let timer;

                function run() {
                    let now = new Date().getTime();
                    let remaining = Math.max((endTime - now) / duration, 0);
                    let value = Math.round(end - (remaining * range));
                    obj.innerHTML = value;
                    if (value == end) {
                        clearInterval(timer);
                    }
                }

                timer = setInterval(run, stepTime);
                run();
            }

            // --- PARALLAX EFFECT ---
            function initParallax() {
                const stars = document.querySelectorAll('.star');
                const bird = document.querySelector('.bird-float');

                document.addEventListener('mousemove', (e) => {
                    const mouseX = e.clientX / window.innerWidth;
                    const mouseY = e.clientY / window.innerHeight;

                    // Move stars in opposite direction (subtle)
                    stars.forEach((star, index) => {
                        const speed = (index + 1) * 0.5;
                        const x = (mouseX - 0.5) * speed * -20;
                        const y = (mouseY - 0.5) * speed * -20;
                        star.style.transform = `translate(${x}px, ${y}px)`;
                    });

                    // Move bird slightly
                    if (bird) {
                        const x = (mouseX - 0.5) * 10;
                        const y = (mouseY - 0.5) * 10;
                        bird.style.transform = `translate(${x}px, ${y}px)`;
                    }
                });
            }

            // --- SMOOTH CURSOR TRAIL EFFECT ---
            let cursorGlow;
            let lastTrailTime = 0;
            const trailDelay = 30; // milliseconds between trail dots

            // Create main cursor glow
            document.addEventListener('DOMContentLoaded', () => {
                cursorGlow = document.createElement('div');
                cursorGlow.className = 'cursor-glow';
                document.body.appendChild(cursorGlow);
            });

            document.addEventListener('mousemove', (e) => {
                // Move main glow
                if (cursorGlow) {
                    cursorGlow.style.left = (e.clientX - 10) + 'px';
                    cursorGlow.style.top = (e.clientY - 10) + 'px';
                }

                // Create trail dots
                const now = Date.now();
                if (now - lastTrailTime < trailDelay) return;
                lastTrailTime = now;

                createTrailDot(e.clientX, e.clientY);
            });

            function createTrailDot(x, y) {
                const trail = document.createElement('div');
                trail.className = 'cursor-trail';
                trail.style.left = (x - 3) + 'px';
                trail.style.top = (y - 3) + 'px';

                document.body.appendChild(trail);

                // Remove trail after animation
                setTimeout(() => {
                    trail.remove();
                }, 600);
            }
