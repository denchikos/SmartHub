const neuralCanvas = document.getElementById("neural-canvas");
const nctx = neuralCanvas.getContext("2d");

function resizeNeural() {
    neuralCanvas.width = window.innerWidth;
    neuralCanvas.height = window.innerHeight;
}
resizeNeural();
window.addEventListener("resize", resizeNeural);

// Вузли сітки
const nodes = [];
const NODE_COUNT = 35;     // Покращена розріджена сітка (OpenAI style)
const LINK_DISTANCE = 220;

class Node {
    constructor() {
        this.x = Math.random() * neuralCanvas.width;
        this.y = Math.random() * neuralCanvas.height;
        this.vx = (Math.random() - 0.5) * 0.2;
        this.vy = (Math.random() - 0.5) * 0.2;
    }

    move() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > neuralCanvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > neuralCanvas.height) this.vy *= -1;
    }
}

function initNodes() {
    nodes.length = 0;
    for (let i = 0; i < NODE_COUNT; i++) {
        nodes.push(new Node());
    }
}
initNodes();

// Графічна логіка
function drawNeural() {
    const isLight = document.body.classList.contains("light-theme");

    nctx.clearRect(0, 0, neuralCanvas.width, neuralCanvas.height);

    // Лінії
    for (let a = 0; a < nodes.length; a++) {
        for (let b = a + 1; b < nodes.length; b++) {
            const dx = nodes[a].x - nodes[b].x;
            const dy = nodes[a].y - nodes[b].y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < LINK_DISTANCE) {
                const alpha = 1 - dist / LINK_DISTANCE;

                nctx.strokeStyle = isLight
                    ? `rgba(20,40,80, ${alpha * 0.2})`
                    : `rgba(0,150,255, ${alpha * 0.2})`;

                nctx.lineWidth = 1;
                nctx.beginPath();
                nctx.moveTo(nodes[a].x, nodes[a].y);
                nctx.lineTo(nodes[b].x, nodes[b].y);
                nctx.stroke();
            }
        }
    }

    // Вузли
    nodes.forEach(n => {
        nctx.fillStyle = isLight
            ? "rgba(20,40,80,0.4)"
            : "rgba(0,150,255,0.8)";
        nctx.beginPath();
        nctx.arc(n.x, n.y, 2.2, 0, Math.PI * 2);
        nctx.fill();
        n.move();
    });

    requestAnimationFrame(drawNeural);
}

drawNeural();
