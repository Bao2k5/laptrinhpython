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
function initCursorTrail() {
    let cursorGlow;
    let lastTrailTime = 0;
    const trailDelay = 30;

    // Create main cursor glow
    cursorGlow = document.createElement('div');
    cursorGlow.className = 'cursor-glow';
    document.body.appendChild(cursorGlow);

    document.addEventListener('mousemove', (e) => {
        // Move main glow
        cursorGlow.style.left = (e.clientX - 10) + 'px';
        cursorGlow.style.top = (e.clientY - 10) + 'px';

        // Create trail dots
        const now = Date.now();
        if (now - lastTrailTime < trailDelay) return;
        lastTrailTime = now;

        const trail = document.createElement('div');
        trail.className = 'cursor-trail';
        trail.style.left = (e.clientX - 3) + 'px';
        trail.style.top = (e.clientY - 3) + 'px';

        document.body.appendChild(trail);

        setTimeout(() => trail.remove(), 600);
    });
}

// ========================================
// PREMIUM SCROLL REVEAL ANIMATIONS
// ========================================
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.feature-card, .leaderboard-wrapper, .download-card');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('scroll-reveal', 'revealed');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    });

    revealElements.forEach(el => {
        el.classList.add('scroll-reveal');
        revealObserver.observe(el);
    });
}

// ========================================
// 3D CARD TILT EFFECT
// ========================================
function init3DCardTilt() {
    const cards = document.querySelectorAll('.feature-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;

            card.style.transform = perspective(1000px) rotateX(c: \Users\Bao\Desktop\LaptrinhPy{ rotateX }deg) rotateY(c: \Users\Bao\Desktop\LaptrinhPy{ rotateY }deg) translateY(-10px);
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
    });
}

// ========================================
// SMOOTH BUTTON RIPPLE EFFECT
// ========================================
function initButtonRipple() {
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-download-large');

    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple-effect');

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });
}
