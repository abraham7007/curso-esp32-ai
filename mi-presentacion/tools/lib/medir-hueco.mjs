/* Medición del espacio vertical que una lámina deja sin usar.
 *
 * Vive aparte porque la usan dos herramientas: `check-huecos.mjs`, que informa
 * del estado, y `proponer-stretch.mjs`, que prueba variantes y compara. Tener
 * dos copias de la medición significaría que un día dejan de coincidir y las
 * comparaciones dejan de valer sin que nada avise.
 *
 * QUÉ SE MIDE, y por qué así. Lo que un espectador llama «espacio que no se
 * aprovecha» es una BANDA HORIZONTAL de la lámina sin nada escrito. Ese es el
 * modelo que se implementa aquí: se recogen las cajas del contenido —el texto,
 * las figuras, las celdas— y se busca la franja de altura mayor que ninguna
 * cruza.
 *
 * Dos formas de medir se descartaron por dar respuestas falsas:
 *
 *   · el hueco al pie del contenido. Con un bloque estirado el pie se llena y
 *     el vacío reaparece en el centro: una lámina pasó de 282 a 297 px de vacío
 *     real mientras su hueco inferior bajaba a cero.
 *
 *   · la mayor separación entre hermanos en el árbol. Falla en dos sentidos
 *     opuestos. Penalizaba una columna de texto corta al lado de una tabla a
 *     alto completo, donde no hay nada que corregir; y no veía tres tarjetas
 *     estiradas y huecas por dentro, porque cada una es estrecha y su vacío se
 *     descartaba por no cruzar la lámina. La banda no se equivoca en ninguno de
 *     los dos: bajo la tabla hay celdas, y dentro de las tarjetas huecas no hay
 *     nada a ninguna altura.
 */

/** Congela la entrada escalonada. Sin esto los bloques que aún no han
 *  aparecido miden cero y todo hueco sale inflado. */
export async function prepararLamina(pagina) {
	await pagina.waitForTimeout(650);
	await pagina.evaluate(() => {
		for (const el of document.querySelectorAll("*")) {
			el.style.animation = "none";
			el.style.transition = "none";
		}
		for (const el of document.querySelectorAll("[data-animate]")) {
			el.classList.add("is-visible");
			el.style.opacity = "1";
			el.style.transform = "none";
		}
	});
	await pagina.waitForTimeout(120);
}

/** Banda horizontal más alta de la lámina sin contenido que la cruce.
 *  Devuelve `{px, donde, alto}`, o null si la lámina no tiene contenido. */
export function medirHueco(pagina) {
	return pagina.evaluate(() => {
		const raiz = document.querySelector(".slide__content");
		if (!raiz) return null;

		const caja = raiz.getBoundingClientRect();
		const s = getComputedStyle(raiz);
		const arriba = Math.round(caja.top + Number.parseFloat(s.paddingTop || 0));
		const abajo = Math.round(
			caja.bottom - Number.parseFloat(s.paddingBottom || 0),
		);
		if (abajo <= arriba) return null;

		/* Contenido = las hojas del árbol. Un contenedor no cuenta como
		   contenido: una tarjeta con borde y fondo ocupa 460 px de alto aunque
		   solo tenga tres renglones escritos, y contarla haría invisible
		   exactamente el defecto que se busca.

		   Un componente propio —los `wokwi-*` de las placas— pinta por su árbol
		   sombra y desborda su propia caja: la placa de la portada declara 39 px
		   mientras ocupa 400 en pantalla. Por eso el padre de un componente
		   propio cuenta como hoja, y el componente no. */
		const esHoja = (el) => {
			const hijos = [...el.children];
			if (!hijos.length) return true;
			return hijos.every((h) => h.tagName.includes("-") || h.shadowRoot);
		};

		const cubierto = new Uint8Array(abajo - arriba);
		let hojas = 0;

		const marcar = (top, bottom) => {
			const y0 = Math.max(arriba, Math.round(top)) - arriba;
			const y1 = Math.min(abajo, Math.round(bottom)) - arriba;
			for (let y = y0; y < y1; y++) cubierto[y] = 1;
		};

		/* Texto suelto dentro de un elemento que SÍ tiene hijos. Sin esto, un
		   <pre> con dos líneas resaltadas y ocho sin resaltar solo contaba las
		   dos: las otras ocho no son elementos, y el recorrido por hijos no las
		   ve. El resultado era una banda «vacía» de 144 px justo encima de un
		   bloque de código lleno. Se miden con un Range, que da la caja real de
		   cada renglón. */
		const marcarTexto = (el) => {
			for (const nodo of el.childNodes) {
				if (nodo.nodeType !== Node.TEXT_NODE || !nodo.textContent.trim())
					continue;
				const rango = document.createRange();
				rango.selectNodeContents(nodo);
				for (const r of rango.getClientRects()) {
					if (r.height > 0) {
						hojas++;
						marcar(r.top, r.bottom);
					}
				}
			}
		};

		const recorrer = (el) => {
			const r = el.getBoundingClientRect();
			const cs = getComputedStyle(el);
			if (
				r.height <= 0 ||
				r.width <= 0 ||
				cs.display === "none" ||
				cs.visibility === "hidden"
			)
				return;

			if (esHoja(el)) {
				hojas++;
				marcar(r.top, r.bottom);
				return;
			}
			marcarTexto(el);
			for (const h of el.children) recorrer(h);
		};
		for (const h of raiz.children) recorrer(h);
		if (!hojas) return null;

		/* Franja libre más alta, y qué la delimita — el «dónde» es lo que hace
		   accionable el informe. */
		let mejor = { px: 0, y0: 0, y1: 0 };
		let inicio = -1;
		for (let y = 0; y <= cubierto.length; y++) {
			const libre = y < cubierto.length && !cubierto[y];
			if (libre && inicio === -1) inicio = y;
			if (!libre && inicio !== -1) {
				if (y - inicio > mejor.px)
					mejor = { px: y - inicio, y0: inicio, y1: y };
				inicio = -1;
			}
		}

		/* El borde de la banda casi siempre es una hoja sin interés —un <code>,
		   un <b>, una celda—. Lo que sirve para actuar es el bloque al que
		   pertenece, así que se sube al primer antepasado con clase. */
		const etq = (x) => {
			if (!x) return "el borde";
			let e = x;
			while (
				e &&
				e !== raiz &&
				!(typeof e.className === "string" && e.className.trim())
			)
				e = e.parentElement;
			if (!e || e === raiz) return x.tagName.toLowerCase();
			return `${e.tagName.toLowerCase()}.${e.className.trim().split(/\s+/)[0]}`;
		};
		const enY = (y) =>
			[...raiz.querySelectorAll("*")]
				.filter((e) => {
					const r = e.getBoundingClientRect();
					return r.height > 0 && Math.abs(r.bottom - (arriba + y)) < 3;
				})
				.pop();
		const debajoDeY = (y) =>
			[...raiz.querySelectorAll("*")]
				.filter((e) => {
					const r = e.getBoundingClientRect();
					return r.height > 0 && Math.abs(r.top - (arriba + y)) < 3;
				})
				.pop();

		const donde =
			mejor.px === 0
				? "sin banda libre"
				: mejor.y1 >= cubierto.length
					? `tras ${etq(enY(mejor.y0))}`
					: mejor.y0 === 0
						? `antes de ${etq(debajoDeY(mejor.y1))}`
						: `entre ${etq(enY(mejor.y0))} y ${etq(debajoDeY(mejor.y1))}`;

		return { px: mejor.px, donde, alto: Math.round(caja.height) };
	});
}

/* Umbral por omisión: 140 px sobre 900 es ~15 % del alto. Por debajo de eso
   el hueco se lee como respiración deliberada y no como lámina a medio
   llenar. */
export const UMBRAL_POR_OMISION = 140;
