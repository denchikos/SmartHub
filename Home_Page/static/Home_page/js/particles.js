// Canvas
const canvas = document.getElementById("particles-canvas");
const ctx = canvas.getContext("2d");

// Resize
function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resize();
window.addEventListener("resize", resize);

// PARAMETERS
const NODES = 70;             // кількість вузлів
const LINK_DISTANCE = 220;    // відстань для ліній
const nodes = [];

// NODE CLASS
class Node {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;

        this.vx = (Math.random() - 0.5) * 0.2; // повільний рух (AI style)
        this.vy = (Math.random() - 0.5) * 0.2;
    }

    move() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }
}

// INIT
function init() {
    nodes.length = 0;
    for (let i = 0; i < NODES; i++) {
        nodes.push(new Node());
    }
}
init();

// DRAW
function drawNeuralNetwork() {

    const isLight = document.body.classList.contains("light-theme");

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // LINES
    for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {

            const dx = nodes[i].x - nodes[j].x;
            const dy = nodes[i].y - nodes[j].y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < LINK_DISTANCE) {
                const alpha = 1 - dist / LINK_DISTANCE;

                ctx.strokeStyle = isLight
                    ? `rgba(20, 40, 80, ${alpha * 0.22})`
                    : `rgba(0, 150, 255, ${alpha * 0.25})`;

                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(nodes[i].x, nodes[i].y);
                ctx.lineTo(nodes[j].x, nodes[j].y);
                ctx.stroke();
            }
        }
    }

    // DOTS
    nodes.forEach(n => {
        ctx.fillStyle = isLight
            ? "rgba(20,40,80,0.45)"
            : "rgba(0,150,255,0.8)";

        ctx.beginPath();
        ctx.arc(n.x, n.y, 2.3, 0, Math.PI * 2);
        ctx.fill();

        n.move();
    });

    requestAnimationFrame(drawNeuralNetwork);
}

drawNeuralNetwork();
