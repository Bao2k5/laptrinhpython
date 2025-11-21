// API Configuration
const API_BASE_URL = 'https://flappybird-duatop.onrender.com';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStatistics();
    loadLeaderboard();
    setupDownloadButton();
});

// Load Statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/scores`);
        const scores = await response.json();

        if (scores && scores.length > 0) {
            // Calculate statistics
            const totalPlayers = new Set(scores.map(s => s.username)).size;
            const highestScore = Math.max(...scores.map(s => s.score));
            const totalGames = scores.length;

            // Animate numbers
            animateNumber('total-players', totalPlayers);
            animateNumber('highest-score', highestScore);
            animateNumber('total-games', totalGames);
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
        document.getElementById('total-players').textContent = '---';
        document.getElementById('highest-score').textContent = '---';
        document.getElementById('total-games').textContent = '---';
    }
}

// Load Leaderboard
async function loadLeaderboard() {
    const leaderboardList = document.getElementById('leaderboard-list');

    try {
        const response = await fetch(`${API_BASE_URL}/api/scores`);
        const scores = await response.json();

        if (!scores || scores.length === 0) {
            leaderboardList.innerHTML = '<div class="loading">Chưa có người chơi nào</div>';
            return;
        }

        // Get top 10 unique players by highest score
        const playerBest = {};
        scores.forEach(score => {
            if (!playerBest[score.username] || playerBest[score.username] < score.score) {
                playerBest[score.username] = score.score;
            }
        });

        const topPlayers = Object.entries(playerBest)
            .map(([username, score]) => ({ username, score }))
            .sort((a, b) => b.score - a.score)
            .slice(0, 10);

        // Render leaderboard
        leaderboardList.innerHTML = topPlayers.map((player, index) => {
            const rank = index + 1;
            const rankClass = rank <= 3 ? `rank-${rank}` : '';
            const medal = rank === 1 ? '🥇' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : '';

            return `
                <div class="leaderboard-item ${rankClass}">
                    <span class="rank-col">${medal} #${rank}</span>
                    <span class="name-col">${escapeHtml(player.username)}</span>
                    <span class="score-col">${player.score.toLocaleString()}</span>
                </div>
            `;
        }).join('');

    } catch (error) {
        console.error('Error loading leaderboard:', error);
        leaderboardList.innerHTML = '<div class="loading">Không thể tải bảng xếp hạng</div>';
    }
}

// Animate Number
function animateNumber(elementId, targetValue) {
    const element = document.getElementById(elementId);
    const duration = 2000; // 2 seconds
    const steps = 60;
    const stepValue = targetValue / steps;
    let currentValue = 0;
    let currentStep = 0;

    const interval = setInterval(() => {
        currentStep++;
        currentValue += stepValue;

        if (currentStep >= steps) {
            element.textContent = targetValue.toLocaleString();
            clearInterval(interval);
        } else {
            element.textContent = Math.floor(currentValue).toLocaleString();
        }
    }, duration / steps);
}

// Setup Download Button
function setupDownloadButton() {
    const downloadBtn = document.getElementById('download-btn');

    // Google Drive direct download link - v1.3 Fixed (Final Stable)
    const downloadLink = 'https://drive.google.com/uc?export=download&id=1N-PPrUYnd7s985aK3Up9XF1Vnow-YzDK';

    downloadBtn.addEventListener('click', (e) => {
        e.preventDefault();

        // Open download link in new tab
        window.open(downloadLink, '_blank');

        // Optional: Show success message
        console.log('Opening download link...');
    });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Auto-refresh leaderboard every 30 seconds
setInterval(loadLeaderboard, 30000);

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
