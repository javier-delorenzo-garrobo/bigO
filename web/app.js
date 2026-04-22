/* ═══════════════════════════════════════════════════════════
   app.js — Lógica del frontend
   
   Gestiona:
     - Selector de lenguaje
     - Editor con numeración de líneas
     - Carga de ficheros (botón y drag & drop)
     - Envío al backend y renderizado de resultados
   ═══════════════════════════════════════════════════════════ */

// ─── Elementos del DOM ──────────────────────────────────────
const langButtons     = document.querySelectorAll('.lang-btn');
const codeInput       = document.getElementById('code-input');
const lineNumbers     = document.getElementById('line-numbers');
const editorFilename  = document.getElementById('editor-filename');
const editorBody      = document.getElementById('editor-body');
const uploadBtn       = document.getElementById('upload-btn');
const fileInput       = document.getElementById('file-input');
const analyzeBtn      = document.getElementById('analyze-btn');
const analyzeBtnText  = analyzeBtn.querySelector('.analyze-btn__text');
const analyzeBtnIcon  = analyzeBtn.querySelector('.analyze-btn__icon');
const mainPanel       = document.getElementById('main-panel');
const dropzone        = document.getElementById('dropzone');
const resultsPanel    = document.getElementById('results-panel');
const errorPanel      = document.getElementById('error-panel');
const errorMessage    = document.getElementById('error-message');

// Elementos de resultado
const resultLanguage    = document.getElementById('result-language');
const functionsContainer = document.getElementById('functions-container');

// ─── Estado ─────────────────────────────────────────────────
/** Extensión seleccionada actualmente */
let currentExtension = '.py';

/** Mapa extensión → nombre de fichero ficticio para el editor */
const EXT_FILENAMES = {
    '.py':   'código.py',
    '.c':    'código.c',
    '.h':    'código.h',
    '.java': 'código.java',
    '.js':   'código.js',
};

/** Mapa extensión → extensión para detectar al cargar ficheros */
const EXT_MAP = {
    'py': '.py', 'c': '.c', 'h': '.h',
    'java': '.java', 'js': '.js',
};

// ─── Selector de lenguaje ───────────────────────────────────

langButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        // Desactivar todos y activar el pulsado
        langButtons.forEach(b => b.classList.remove('lang-btn--active'));
        btn.classList.add('lang-btn--active');

        currentExtension = btn.dataset.ext;
        editorFilename.textContent = EXT_FILENAMES[currentExtension] || 'código';
    });
});

// ─── Numeración de líneas ───────────────────────────────────

/**
 * Actualiza los números de línea del editor para que
 * coincidan con el contenido del textarea.
 */
function updateLineNumbers() {
    const lines = codeInput.value.split('\n');
    const count = lines.length || 1;

    // Construimos los números solo si ha cambiado la cantidad
    // para evitar repintados innecesarios
    const currentCount = lineNumbers.childElementCount || 
                         lineNumbers.textContent.split('\n').length;

    if (currentCount !== count) {
        lineNumbers.textContent = Array.from(
            { length: count },
            (_, i) => i + 1
        ).join('\n');
    }
}

codeInput.addEventListener('input', updateLineNumbers);

// Sincronizar scroll vertical entre textarea y números de línea
codeInput.addEventListener('scroll', () => {
    lineNumbers.style.transform = `translateY(-${codeInput.scrollTop}px)`;
});

// ─── Carga de ficheros ──────────────────────────────────────

uploadBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) loadFile(file);
    // Resetear para poder cargar el mismo fichero de nuevo
    fileInput.value = '';
});

/**
 * Lee un fichero y lo carga en el editor, detectando
 * automáticamente el lenguaje por su extensión.
 */
function loadFile(file) {
    const ext = file.name.split('.').pop().toLowerCase();
    const mappedExt = EXT_MAP[ext];

    if (!mappedExt) {
        showError(`Extensión ".${ext}" no soportada. Usa: .py, .c, .h, .java, .js`);
        return;
    }

    // Actualizar lenguaje seleccionado
    currentExtension = mappedExt;
    langButtons.forEach(btn => {
        btn.classList.toggle('lang-btn--active', btn.dataset.ext === mappedExt);
    });
    editorFilename.textContent = file.name;

    // Leer contenido
    const reader = new FileReader();
    reader.onload = (e) => {
        codeInput.value = e.target.result;
        updateLineNumbers();
    };
    reader.readAsText(file);
}

// ─── Drag & Drop ────────────────────────────────────────────

// Contador para manejar eventos de drag anidados (hijos del panel)
let dragCounter = 0;

mainPanel.addEventListener('dragenter', (e) => {
    e.preventDefault();
    dragCounter++;
    dropzone.classList.add('dropzone--visible');
});

mainPanel.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dragCounter--;
    if (dragCounter === 0) {
        dropzone.classList.remove('dropzone--visible');
    }
});

mainPanel.addEventListener('dragover', (e) => {
    e.preventDefault();
});

mainPanel.addEventListener('drop', (e) => {
    e.preventDefault();
    dragCounter = 0;
    dropzone.classList.remove('dropzone--visible');

    const file = e.dataTransfer.files[0];
    if (file) loadFile(file);
});

// ─── Análisis ───────────────────────────────────────────────

analyzeBtn.addEventListener('click', analyze);

// También lanzar con Ctrl+Enter / Cmd+Enter
codeInput.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        analyze();
    }
});

/**
 * Envía el código al backend, recibe el resultado
 * y lo muestra en el panel de resultados.
 */
async function analyze() {
    const code = codeInput.value.trim();

    if (!code) {
        showError('Escribe o pega código antes de analizar.');
        return;
    }

    // Estado de carga
    setLoading(true);
    hideError();
    hideResults();

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                code: codeInput.value,
                language: currentExtension,
            }),
        });

        const data = await response.json();

        if (!data.success) {
            showError(data.error || 'Error desconocido del servidor.');
            return;
        }

        showResults(data);

    } catch (err) {
        showError('No se pudo conectar con el servidor. ¿Está ejecutándose server.py?');
        console.error('Error de red:', err);
    } finally {
        setLoading(false);
    }
}

// ─── Renderizado de resultados ──────────────────────────────

/**
 * Muestra los resultados del análisis en el panel con
 * animaciones de entrada.
 */
function showResults(data) {
    resultLanguage.textContent = data.language;
    functionsContainer.innerHTML = '';

    const funcs = data.functions || [];
    
    funcs.forEach((func, index) => {
        const depth = func.max_depth;
        const depthStr = `${depth} nivel${depth !== 1 ? 'es' : ''}`;
        const recursiveStr = func.is_recursive ? 'Sí' : 'No';

        const card = document.createElement('div');
        card.className = 'complexity-hero';
        card.style.marginBottom = '0';
        card.style.animationDelay = `${index * 0.1}s`;

        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <span class="complexity-hero__label" style="margin: 0;">Función: <strong>${func.name}</strong></span>
                <div style="display: flex; gap: 1rem; font-size: 0.9rem;">
                    <span title="Anidamiento">📐 ${depthStr}</span>
                    <span title="Recursividad">🔄 ${recursiveStr}</span>
                </div>
            </div>
            <span class="complexity-hero__value" style="font-size: 2.5rem; margin-bottom: 0.5rem;">${func.complexity}</span>
            <span class="complexity-hero__explanation">${func.explanation}</span>
            ${func.warning ? `<div class="warning-badge">⚠ ${func.warning}</div>` : ''}
        `;
        functionsContainer.appendChild(card);
    });

    // Mostrar panel con animación
    resultsPanel.classList.remove('hidden');

    // Scroll suave al resultado
    resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideResults() {
    resultsPanel.classList.add('hidden');
}

// ─── Errores ────────────────────────────────────────────────

function showError(message) {
    errorMessage.textContent = message;
    errorPanel.classList.remove('hidden');

    // Re-animar el shake
    errorPanel.style.animation = 'none';
    void errorPanel.offsetHeight;
    errorPanel.style.animation = '';
}

function hideError() {
    errorPanel.classList.add('hidden');
}

// ─── Estado de carga ────────────────────────────────────────

function setLoading(loading) {
    if (loading) {
        analyzeBtn.classList.add('analyze-btn--loading');
        analyzeBtnText.textContent = 'Analizando...';
        analyzeBtnIcon.textContent = '⏳';
    } else {
        analyzeBtn.classList.remove('analyze-btn--loading');
        analyzeBtnText.textContent = 'Analizar complejidad';
        analyzeBtnIcon.textContent = '🔍';
    }
}

// ─── Inicialización ─────────────────────────────────────────
updateLineNumbers();
