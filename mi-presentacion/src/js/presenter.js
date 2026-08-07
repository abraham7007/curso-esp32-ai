/* Marco del modo presentación (presentar.html).

   Solo hace tres cosas:
     1. Cargar en el marco interior la diapositiva indicada tras la almohadilla
        de la dirección: /presentar.html#/src/slides/clase-01/01-portada.html
     2. Mantener esa dirección sincronizada cuando la diapositiva de dentro
        navega, para que recargar la página no devuelva al principio.
     3. Entrar en pantalla completa en el primer gesto del usuario, venga de
        este documento o del de dentro.

   Lo que NO hace: gobernar la navegación entre diapositivas. Cada diapositiva
   sigue navegando por sí misma con sus propios enlaces, exactamente igual que
   fuera de este marco. Es precisamente lo que arregla el problema: la
   navegación ocurre dentro del marco y este documento nunca se descarga, así
   que la pantalla completa se conserva. */

const RUTA_POR_DEFECTO = "/src/slides/clase-01/01-portada.html";
const marco = document.getElementById("marco");

/* Solo se aceptan rutas internas del propio mazo. Sin esta comprobación, la
   parte de la dirección posterior a la almohadilla —que cualquiera puede
   escribir o enviar en un enlace— podría cargar un sitio ajeno dentro del
   marco, con la apariencia de ser parte de la presentación. */
function rutaSegura(bruta) {
	const ruta = decodeURIComponent(bruta || "").trim();
	if (ruta.includes("..") || !ruta.endsWith(".html")) return RUTA_POR_DEFECTO;
	// El índice del curso también se puede mostrar dentro del marco: así,
	// volver al inicio para cambiar de sesión no obliga a salir de pantalla
	// completa y volver a entrar.
	if (ruta === "/index.html") return ruta;
	if (!ruta.startsWith("/src/slides/")) return RUTA_POR_DEFECTO;
	return ruta;
}

function rutaPedida() {
	return rutaSegura(window.location.hash.slice(1));
}

function cargar(ruta) {
	if (marco.getAttribute("src") !== ruta) marco.setAttribute("src", ruta);
}

/* ---------------------------------------------------------------------- */

/* Al llegar aquí desde una diapositiva suelta, la intención era ver la
   presentación a pantalla completa; pero una solicitud de pantalla completa
   solo se atiende si nace de un gesto del usuario, y una redirección no lo
   es. Así que se queda armada y entra con el primer gesto, que en la práctica
   es el mismo con el que se avanza de lámina.

   El gesto puede ocurrir dentro del marco. Como el marco es del mismo origen,
   la activación por parte del usuario se propaga al documento contenedor y la
   solicitud resulta válida desde aquí. */
let pendiente = true;
const armados = new Set();

async function alGesto() {
	if (!pendiente || document.fullscreenElement) return;
	try {
		await document.documentElement.requestFullscreen();
		pendiente = false;
		desarmar();
	} catch {
		// Rechazada: se deja armado para el siguiente gesto en vez de perder
		// la intención. Un oyente `once` se habría consumido aquí.
	}
}

function desarmar() {
	for (const doc of armados) {
		for (const evento of ["pointerdown", "keydown"]) {
			doc.removeEventListener(evento, alGesto, true);
		}
	}
	armados.clear();
}

function armarPrimerGesto(doc) {
	if (!doc || !pendiente || armados.has(doc)) return;
	armados.add(doc);
	for (const evento of ["pointerdown", "keydown"]) {
		doc.addEventListener(evento, alGesto, true);
	}
}

/* ---------------------------------------------------------------------- */

marco.addEventListener("load", () => {
	let interior = null;
	try {
		interior = marco.contentWindow;
	} catch {
		// Un documento de otro origen no debería llegar aquí (rutaSegura lo
		// impide), pero si llegara, no se toca.
		return;
	}
	if (!interior) return;

	// La dirección del contenedor sigue a la de dentro, sin apilar entradas
	// nuevas en el historial: el historial de la presentación es el del marco.
	const ruta = interior.location.pathname;
	if (ruta && `#${ruta}` !== window.location.hash) {
		history.replaceState(null, "", `#${ruta}`);
	}

	document.title = `${interior.document.title} · Presentación`;

	/* El teclado lo atiende la diapositiva, no este marco. Si el foco se
	   quedara en el documento contenedor, las flechas no llegarían a ninguna
	   parte y la presentación parecería atascada. Se devuelve el foco al
	   interior en cada carga. */
	interior.focus();

	// Cada lámina trae un documento nuevo: si la solicitud sigue pendiente,
	// hay que volver a armarla sobre él.
	armarPrimerGesto(interior.document);
});

/* Al entrar o salir de pantalla completa el navegador puede mover el foco al
   documento que hizo la solicitud, que es este. Se devuelve. */
document.addEventListener("fullscreenchange", () => {
	try {
		marco.contentWindow?.focus();
	} catch {
		// Marco de otro origen: no debería ocurrir, y no hay nada que hacer.
	}
});

window.addEventListener("hashchange", () => {
	cargar(rutaPedida());
});

armarPrimerGesto(document);
cargar(rutaPedida());
