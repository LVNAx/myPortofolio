Education Section
'''
/* Bagian Education */
.education {
    padding: 4rem 0 5rem;
}

.timeline {
    position: relative;
    max-width: 100%;
    margin: 0 auto;
}

.timeline::after {
    content: "";
    position: absolute;
    width: 4px;
    height: 100%;
    top: 0;
    left: 50%;
    margin-left: -2px;
    background: var(--accent);
    border-radius: 999px;
    z-index: 0;
    animation: moveline 1.2s ease-out forwards;
}

.container-timeline {
    position: relative;
    width: 50%;
    padding: 10px 45px;
    opacity: 0;
    animation: movedown 0.6s ease-out forwards;
}

.left-container {
    left: 0;
}

.right-container {
    left: 50%;
}

.container-timeline:nth-child(1) { animation-delay: 0.2s; }
.container-timeline:nth-child(2) { animation-delay: 0.45s; }
.container-timeline:nth-child(3) { animation-delay: 0.7s; }
.container-timeline:nth-child(4) { animation-delay: 0.95s; }
.container-timeline:nth-child(5) { animation-delay: 1.2s; }

.timeline-avatar {
    position: absolute;
    top: 30px;
    right: -20px;
    width: 40px;
    height: 40px;
    object-fit: cover;
    border-radius: 50%;
    border: 2px solid var(--ink);
    background-color: var(--paper);
    z-index: 10;
}

.right-container .timeline-avatar {
    left: -20px;
    right: auto;
}

.text-box {
    position: relative;
    padding: 1.25rem 1.5rem;
    background-color: #fff;
    border: 1px solid var(--line);
    border-radius: calc(var(--radius) * 4);
    font-size: 0.95rem;
}

.text-box h2 {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1.3;
}

.text-box small {
    display: inline-block;
    margin-bottom: 0.6rem;
    font-size: 0.85rem;
    color: var(--text-muted);
}

.text-box p {
    color: var(--ink);
}

.left-container-arrow,
.right-container-arrow {
    position: absolute;
    top: 26px;
    width: 0;
    height: 0;
    border-top: 12px solid transparent;
    border-bottom: 12px solid transparent;
    z-index: 1;
}

.left-container-arrow {
    right: -12px;
    border-left: 12px solid #fff;
}

.right-container-arrow {
    left: -12px;
    border-right: 12px solid #fff;
}

@keyframes movedown {
    0% {
        opacity: 0;
        transform: translateY(-24px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes moveline {
    0%   { height: 0; }
    100% { height: 100%; }
}

@media (max-width: 600px) {
    .timeline::after {
        left: 20px;
        margin-left: 0;
    }

    .container-timeline,
    .right-container {
        width: 100%;
        left: 0;
        padding-left: 60px;
        padding-right: 0;
    }

    .timeline-avatar,
    .right-container .timeline-avatar {
        left: 2px;
        right: auto;
    }

    .left-container-arrow,
    .right-container-arrow {
        left: -12px;
        right: auto;
        border-left: 0;
        border-right: 12px solid #fff;
    }
}

@media (prefers-reduced-motion: reduce) {
    .container-timeline,
    .timeline::after {
        animation: none;
        opacity: 1;
        height: 100%;
    }
}

<section class="education">
        <div class="container">
            <p class="section-kicker">Pendidikan</p>
            <h2 class="section-title">Education</h2>

            <div class="timeline">
                <div class="container-timeline left-container">
                    <img class="timeline-avatar" src="/static/img/nugraha.png" alt="Logo SMP Islam Al Azhar 17 Pontianak" width="40" height="40">
                    <div class="text-box">
                        <h2>SMP Islam Al-Azhar 17 Pontianak</h2>
                        <small>2019 sampai 2022</small>
                        <p>Rank no.1</p>
                        <span class="left-container-arrow"></span>
                    </div>
                </div>

                <div class="container-timeline right-container">
                    <img class="timeline-avatar" src="/static/img/nugraha.png" alt="Logo SMA Negeri 1 Pontianak" width="40" height="40">
                    <div class="text-box">
                        <h2>SMA Negeri 1 Pontianak</h2>
                        <small>2022 sampai 2025</small>
                        <p>Rank no.11</p>
                        <span class="right-container-arrow"></span>
                    </div>
                </div>

                <div class="container-timeline left-container">
                    <img class="timeline-avatar" src="/static/img/nugraha.png" alt="Logo Universitas Indonesia" width="40" height="40">
                    <div class="text-box">
                        <h2>Universitas Indonesia</h2>
                        <small>2025 sampai sekarang</small>
                        <p>lapar</p>
                        <span class="left-container-arrow"></span>
                    </div>
                </div>
            </div>
        </div>
    </section>
'''