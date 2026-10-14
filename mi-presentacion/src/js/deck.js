// Shared chrome for every slide: entrance-animation reveal, progress bar,
// home button, theme toggle (persisted across page loads since each slide is
// its own document), fullscreen toggle, and keyboard navigation.
// Import once per slide: <script type="module" src="../../js/deck.js"></script>

const THEME_KEY = "esp32-deck-theme";

function icon(name) {
	return `<svg class="icon" aria-hidden="true"><use href="/course-icons.svg#${name}"/></svg>`;
}

function reveal() {
	for (const el of document.querySelectorAll("[data-animate]")) {
		el.classList.add("is-visible");
	}
}

/* Posición de esta diapositiva dentro de su sesión, deducida del nombre del
   archivo (NN-...) y del total declarado en <body data-deck-total="NN">.
   Sin ese atributo la barra no se dibuja: prefiero no mostrar progreso a
   mostrar uno inventado. */
function deckPosition() {
	const file = window.location.pathname.split("/").pop() || "";
	const m = file.match(/^(\d+)-/);
	const total = Number(document.body.dataset.deckTotal);
	if (!m || !Number.isFinite(total) || total <= 0) return null;
	return { index: Number(m[1]), total };
}

function injectProgress() {
	const pos = deckPosition();
	if (!pos) return;

	const bar = document.createElement("div");
	bar.className = "deck-progress";
	bar.setAttribute("role", "progressbar");
	bar.setAttribute("aria-valuemin", "1");
	bar.setAttribute("aria-valuemax", String(pos.total));
	bar.setAttribute("aria-valuenow", String(pos.index));
	bar.setAttribute(
		"aria-label",
		`Diapositiva ${pos.index} de ${pos.total} de la sesión`,
	);

	const fill = document.createElement("div");
	fill.className = "deck-progress__fill";
	fill.style.setProperty("--p", `${(pos.index / pos.total) * 100}%`);

	bar.appendChild(fill);
	document.body.appendChild(bar);

	const count = document.createElement("span");
	count.className = "deck-progress__count";
	count.textContent = `${pos.index} / ${pos.total}`;
	document.body.appendChild(count);
}

function initTheme(themeBtn) {
	const stored = localStorage.getItem(THEME_KEY);
	if (stored === "dark" || stored === "light") {
		document.documentElement.dataset.theme = stored;
	}

	const render = () => {
		const isDark = document.documentElement.dataset.theme
			? document.documentElement.dataset.theme === "dark"
			: window.matchMedia("(prefers-color-scheme: dark)").matches;
		themeBtn.innerHTML = isDark ? icon("i-sun") : icon("i-moon");
		themeBtn.setAttribute(
			"aria-label",
			isDark ? "Cambiar a modo claro" : "Cambiar a modo oscuro",
		);
	};

	themeBtn.addEventListener("click", () => {
		const current = document.documentElement.dataset.theme
			? document.documentElement.dataset.theme === "dark"
			: window.matchMedia("(prefers-color-scheme: dark)").matches;
		const next = current ? "light" : "dark";
		document.documentElement.dataset.theme = next;
		localStorage.setItem(THEME_KEY, next);
		render();
	});

	render();
}

/* Documento sobre el que actúa la pantalla completa.

   La API de pantalla completa está atada al documento que la solicita, y cada
   diapositiva es un documento distinto: al navegar a la siguiente, el
   documento se destruye y el navegador sale de pantalla completa. Ese era el
   fallo. Dentro del marco de presentar.html, quien manda es el documento
   contenedor, que no se descarga nunca; ahí la pantalla completa sobrevive a
   los cambios de lámina. */
function documentoDeVisualizacion() {
	if (window.self === window.top) return null;
	try {
		// Mismo origen: la propiedad es legible. Si no lo fuera, lanza.
		window.parent.document.documentElement;
		return window.parent.document;
	} catch {
		return null;
	}
}

const DOC_PRESENTACION = documentoDeVisualizacion();
const ENMARCADA = DOC_PRESENTACION !== null;

function initFullscreen(fsBtn) {
	// Dentro del marco se consulta y se conmuta el documento contenedor; la
	// activación por gesto del usuario se propaga a los documentos que
	// contienen a este, así que la solicitud es válida desde aquí.
	const doc = DOC_PRESENTACION || document;

	const render = () => {
		const isFs = Boolean(doc.fullscreenElement);
		fsBtn.innerHTML = isFs ? icon("i-shrink") : icon("i-expand");
		fsBtn.setAttribute(
			"aria-label",
			isFs ? "Salir de pantalla completa" : "Pantalla completa",
		);
	};

	fsBtn.addEventListener("click", () => {
		if (doc.fullscreenElement) {
			doc.exitFullscreen();
			return;
		}
		if (!ENMARCADA) {
			/* Fuera del marco, pedir pantalla completa aquí duraría hasta la
			   siguiente lámina. Se entra al modo presentación por la lámina
			   actual: allí la pantalla completa se solicita en el primer gesto
			   —que será justamente el de avanzar— y ya no se pierde. */
			window.location.href = `/presentar.html#${window.location.pathname}`;
			return;
		}
		doc.documentElement.requestFullscreen().catch(() => {
			// Algunos navegadores la rechazan si no reconocen el gesto como
			// directo; el botón sigue funcionando en el siguiente clic.
		});
	});

	doc.addEventListener("fullscreenchange", render);
	render();
}

function injectControls() {
	const wrap = document.createElement("div");
	wrap.className = "deck-controls";

	// Volver al índice del curso, disponible desde cualquier diapositiva.
	const homeBtn = document.createElement("a");
	homeBtn.className = "deck-controls__btn";
	homeBtn.href = "/index.html";
	homeBtn.innerHTML = icon("i-home");
	homeBtn.setAttribute("aria-label", "Volver al índice del curso");

	const themeBtn = document.createElement("button");
	themeBtn.type = "button";
	themeBtn.className = "deck-controls__btn";

	const fsBtn = document.createElement("button");
	fsBtn.type = "button";
	fsBtn.className = "deck-controls__btn";

	wrap.append(homeBtn, themeBtn, fsBtn);
	document.body.appendChild(wrap);

	initTheme(themeBtn);
	initFullscreen(fsBtn);
}

/* Navegación con teclado: las flechas recorren la sesión siguiendo los
   enlaces que la propia diapositiva ya declara en .slide-nav, e Inicio
   vuelve al índice. No inventa rutas: si el enlace no existe, no hace nada. */
function initKeyboardNav() {
	const links = [...document.querySelectorAll(".slide-nav__link")];
	const prev = links[0]?.getAttribute("href");

	/* La portada no lleva franja de navegación: su avance es el botón
	   «Empezar». Sin esta salvedad, pulsar la flecha derecha sobre ella no
	   hacía nada y la sesión parecía atascada nada más abrirla, justo el
	   momento en que se está proyectando. */
	const next =
		links[1]?.getAttribute("href") ||
		document
			.querySelector(".slide__content a.btn--primary[href$='.html']")
			?.getAttribute("href");

	const pasos = initPasos();

	const avanzar = () => {
		if (pasos.siguiente()) return;
		if (next) window.location.href = next;
	};
	const retroceder = () => {
		if (pasos.anterior()) return;
		// La lámina anterior se abre con todos sus pasos ya visibles: se
		// vuelve a donde se dejó, no al principio de su secuencia.
		if (prev) window.location.href = `${prev}#fin`;
	};

	const ponente = initPonente(links, { avanzar, retroceder }, pasos);
	document.addEventListener("paso", ponente.anunciar);
	ponente.anunciar();

	document.addEventListener("keydown", (e) => {
		if (e.metaKey || e.ctrlKey || e.altKey) return;
		const tag = document.activeElement?.tagName;
		if (tag === "INPUT" || tag === "SELECT" || tag === "TEXTAREA") return;

		if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") {
			// El espacio sobre un botón o un enlace es su propia pulsación.
			if (e.key === " " && (tag === "BUTTON" || tag === "A")) return;
			e.preventDefault();
			avanzar();
		} else if (e.key === "ArrowLeft" || e.key === "PageUp") {
			e.preventDefault();
			retroceder();
		} else if (e.key === "Home") {
			window.location.href = "/index.html";
		} else if (e.key === "N" && e.shiftKey) {
			// Respaldo sin segunda pantalla: notas superpuestas en la lámina.
			document.body.classList.toggle("show-notas");
		} else if (e.key === "n") {
			ponente.abrir();
		} else if (e.key === "d" || e.key === "D") {
			const detalles = [...document.querySelectorAll("details.detalle")];
			const abrir = detalles.some((d) => !d.open);
			for (const d of detalles) d.open = abrir;
		}
	});
}

/* Vista del ponente (ponente.html). La tecla N la abre en otra ventana, que
   se lleva a la pantalla del portátil: las notas no se proyectan nunca. La
   lámina le anuncia su estado por un BroadcastChannel cada vez que carga o
   revela un paso, y obedece sus órdenes de avanzar y retroceder. */
function initPonente(links, acciones, pasos) {
	const canal =
		"BroadcastChannel" in window ? new BroadcastChannel("esp32-ponente") : null;
	const anunciar = () => {
		if (!canal) return;
		const { mostrados: pasosMostrados, total: pasosTotal } = pasos.estado();
		const pos = deckPosition();
		canal.postMessage({
			tipo: "estado",
			titulo:
				document.querySelector(".slide__title, .code-hour__title")?.innerText ||
				document.title,
			notas: document.querySelector(".notas")?.innerHTML || "",
			posicion: pos ? `${pos.index} / ${pos.total}` : "",
			pasosMostrados,
			pasosTotal,
			siguiente: links[1]?.innerText.trim() || "",
		});
	};

	canal?.addEventListener("message", ({ data }) => {
		if (data?.tipo === "pedir-estado") anunciar();
		if (data?.tipo === "orden" && data.orden === "avanzar") acciones.avanzar();
		if (data?.tipo === "orden" && data.orden === "retroceder")
			acciones.retroceder();
	});

	return {
		anunciar,
		abrir() {
			window.open("/ponente.html", "esp32-ponente", "width=960,height=720");
		},
	};
}

/* Revelado por pasos. Los elementos con data-paso="N" empiezan ocultos y se
   muestran por grupos, en orden de N, con → / AvPág / espacio. Mientras
   quede un paso por mostrar, avanzar no cambia de lámina; retroceder oculta
   el último grupo mostrado. Sin elementos data-paso, no hace nada y el
   teclado navega como siempre. */
function initPasos() {
	const elementos = [...document.querySelectorAll("[data-paso]")];
	const grupos = [...new Set(elementos.map((el) => Number(el.dataset.paso)))]
		.filter(Number.isFinite)
		.sort((a, b) => a - b);
	let mostrados = 0;

	const aplicar = () => {
		const visibles = new Set(grupos.slice(0, mostrados));
		for (const el of elementos) {
			el.classList.toggle("is-shown", visibles.has(Number(el.dataset.paso)));
		}
		document.dispatchEvent(
			new CustomEvent("paso", { detail: { mostrados, total: grupos.length } }),
		);
	};

	if (window.location.hash === "#fin") mostrados = grupos.length;
	aplicar();

	// Al imprimir o exportar a PDF no se puede pulsar: se muestra todo.
	window.addEventListener("beforeprint", () => {
		mostrados = grupos.length;
		aplicar();
	});

	return {
		estado: () => ({ mostrados, total: grupos.length }),
		siguiente() {
			if (mostrados >= grupos.length) return false;
			mostrados += 1;
			aplicar();
			return true;
		},
		anterior() {
			if (mostrados <= 0) return false;
			mostrados -= 1;
			aplicar();
			return true;
		},
	};
}

/* Figuras generadas con Python. El marcado solo declara cuál quiere:

     <div class="figure__frame" data-figure="adc-transferencia"></div>

   y aquí se trae public/figures/<nombre>.svg y se inserta EN LÍNEA. Se
   inserta en vez de usar <img src> porque un SVG cargado como imagen vive
   en su propio documento y no ve las variables de color de la página: en
   línea, el mismo archivo se dibuja con la tinta del tema activo y cambia
   solo al conmutar a oscuro, sin mantener dos versiones de cada figura.

   Se cachea por nombre porque una diapositiva puede mostrar la misma figura
   dos veces (por ejemplo, un detalle ampliado junto a la vista completa). */
const figureCache = new Map();

function loadFigure(host) {
	const name = host.dataset.figure;
	if (!name) return;

	const url = `/figures/${name}.svg`;
	if (!figureCache.has(name)) {
		figureCache.set(
			name,
			fetch(url).then((r) => {
				if (!r.ok) throw new Error(`figura ${name}: HTTP ${r.status}`);
				return r.text();
			}),
		);
	}

	figureCache
		.get(name)
		.then((svg) => {
			host.innerHTML = svg;
			// La figura es ilustración de un texto que ya está en la lámina;
			// anunciarla otra vez al lector de pantalla solo duplica.
			const el = host.querySelector("svg");
			if (el) el.setAttribute("aria-hidden", "true");
		})
		.catch((err) => {
			// Un fallo de figura no debe dejar un hueco mudo: se dice cuál
			// falta, que es lo único accionable.
			host.textContent = `No se pudo cargar la figura «${name}».`;
			host.classList.add("figure__frame--error");
			console.error(err);
		});
}

function injectFigures() {
	for (const host of document.querySelectorAll("[data-figure]")) {
		loadFigure(host);
	}
}

/* Botón de copiar en cada prompt de «La hora del código». El prompt está
   para pegarlo en el asistente: transcribirlo a mano desde una proyección es
   justo donde se pierden las comillas angulares y los acentos, y el prompt
   deja de pedir lo que dice pedir. Se inyecta desde aquí para que ninguna
   diapositiva tenga que repetir el marcado del botón. */
function injectPromptCopy() {
	for (const box of document.querySelectorAll(".prompt-box")) {
		// Se lee el texto ANTES de meter el botón dentro del bloque: si se
		// leyera al pulsar, la palabra «Copiar» viajaría dentro del prompt.
		// innerText y no textContent porque respeta los saltos de línea.
		const texto = box.innerText.trim();

		const btn = document.createElement("button");
		btn.type = "button";
		btn.className = "prompt-box__copy";
		btn.textContent = "Copiar";
		btn.setAttribute("aria-label", "Copiar el prompt al portapapeles");

		btn.addEventListener("click", async () => {
			try {
				await navigator.clipboard.writeText(texto);
				btn.textContent = "Copiado";
				btn.classList.add("is-done");
			} catch {
				// Sin permiso de portapapeles (http en LAN, por ejemplo) se
				// deja el texto seleccionado para copiar con el teclado.
				const sel = window.getSelection();
				const range = document.createRange();
				range.selectNodeContents(box);
				sel.removeAllRanges();
				sel.addRange(range);
				btn.textContent = "Selecciona y copia";
			}
			setTimeout(() => {
				btn.textContent = "Copiar";
				btn.classList.remove("is-done");
			}, 2200);
		});

		box.appendChild(btn);
	}
}

reveal();
injectProgress();
injectControls();
initKeyboardNav();
injectFigures();
injectPromptCopy();
