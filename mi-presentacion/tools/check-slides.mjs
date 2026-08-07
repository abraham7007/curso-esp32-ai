/* Verificación automática de las diapositivas contra el servidor de
   desarrollo. Sustituye a mirar capturas una por una, que es donde se
   escapan las regresiones: un cambio de tipografía global rompe el encaje
   de diapositivas que nadie estaba revisando en ese momento.

   Comprueba, para cada archivo de src/slides/:
     · desbordamiento     — .slide__content con más contenido del que cabe
     · errores de consola — figuras que no cargan, módulos que fallan
     · figuras            — que cada [data-figure] haya recibido su SVG
     · cadena de navegación — que prev/next apunten a archivos existentes

   Uso:  node tools/check-slides.mjs [clase-01]
         node tools/check-slides.mjs --shot clase-01/15-xtensa-vs-riscv

   IMPORTANTE: el complemento de Tailwind para Vite solo mira los archivos
   que existían al arrancar `npm run dev`. Si se creó o renombró una
   diapositiva después, hay que reiniciar el servidor antes de verificar o
   el resultado no significa nada. */

import { existsSync, mkdirSync, readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { chromium } from "playwright";
import { asegurarServidor } from "./lib/servidor.mjs";

const RAIZ = path.resolve(import.meta.dirname, "..");
const BASE = "http://localhost:5173";
const SLIDES = path.join(RAIZ, "src", "slides");
const CAPTURAS = path.join(RAIZ, ".capturas");

// Holgura antes de declarar desbordamiento. Un par de píxeles vienen del
// redondeo subpíxel del navegador y no son contenido perdido de verdad.
const TOLERANCIA_PX = 12;

const args = process.argv.slice(2);
const soloCaptura = args.includes("--shot");
const filtro = args.find((a) => !a.startsWith("--"));

function listarDiapositivas() {
	const salida = [];
	for (const clase of readdirSync(SLIDES).sort()) {
		const dir = path.join(SLIDES, clase);
		for (const archivo of readdirSync(dir).sort()) {
			if (!archivo.endsWith(".html")) continue;
			const rel = `${clase}/${archivo}`;
			if (filtro && !rel.startsWith(filtro) && !rel.includes(filtro)) continue;
			salida.push({ clase, archivo, rel });
		}
	}
	return salida;
}

await asegurarServidor();

const navegador = await chromium.launch({ channel: "chrome" });
const pagina = await navegador.newPage({
	viewport: { width: 1440, height: 900 },
});

const problemas = [];
const diapositivas = listarDiapositivas();

if (soloCaptura) mkdirSync(CAPTURAS, { recursive: true });

// Errores de consola de la diapositiva en curso. Los oyentes se registran una
// sola vez fuera del bucle: engancharlos en cada vuelta los iba acumulando y
// terminaba atribuyendo a una diapositiva los errores de todas las anteriores.
let errores = [];
pagina.on("console", (msg) => {
	if (msg.type() === "error") errores.push(msg.text());
});
pagina.on("pageerror", (e) => errores.push(String(e)));

for (const d of diapositivas) {
	errores = [];

	await pagina.goto(`${BASE}/src/slides/${d.rel}`, {
		waitUntil: "networkidle",
	});
	/* Las tipografías se cargan de Google Fonts. Mientras no están, el
	   navegador compone con la de reserva, que tiene otras métricas, y el alto
	   medido no es el que verá nadie: en una pasada completa del mazo eso
	   producía desbordes fantasma de unos pocos píxeles que desaparecían al
	   revisar la misma lámina por separado. Se espera a que estén listas. */
	await pagina.evaluate(() => document.fonts.ready).catch(() => {});

	/* CAUSA DE LOS DESBORDES FANTASMA, documentada aquí porque costó
	   encontrarla: la animación de entrada desplaza cada bloque con
	   `transform: translateY(...)`, y el área de desplazamiento de un
	   contenedor **incluye la caja transformada de sus descendientes**. Medida
	   a mitad de animación, la lámina parecía desbordar exactamente lo que
	   quedaba de recorrido —un renglón— y el resultado cambiaba de lámina en
	   cada pasada según el momento en que caía la medición, sobre un mazo que
	   en reposo cabe entero.

	   Se mide, por tanto, la maquetación EN REPOSO: se anulan animaciones,
	   transiciones y transformaciones antes de medir. Es el estado que ve
	   quien está mirando la diapositiva, que es el que importa. La animación
	   de entrada se revisa a ojo en las capturas, no aquí. */
	await pagina.addStyleTag({
		content:
			"*, *::before, *::after { animation: none !important;" +
			" transition: none !important; transform: none !important; }" +
			/* Los bloques con [data-animate] arrancan en opacity:0 y es la
			   propia animación la que los revela. Al anularla se quedaban
			   invisibles y las capturas salían en blanco: hay que devolverles
			   la opacidad a mano. */
			" [data-animate] { opacity: 1 !important; }",
	});
	// Las figuras llegan por fetch; sin esta espera se miden marcos vacíos.
	await pagina.waitForTimeout(300);

	// Si el documento se recarga mientras se mide (Vite reinyecta módulos al
	// vuelo), el contexto muere y la medición se pierde. Se reintenta una vez
	// en lugar de abortar la revisión entera por un accidente de tiempo.
	const medir = () =>
		pagina.evaluate(() => {
			const c = document.querySelector(".slide__content");
			const figuras = [...document.querySelectorAll("[data-figure]")].map(
				(f) => ({
					nombre: f.dataset.figure,
					cargada: Boolean(f.querySelector("svg")),
				}),
			);
			const enlaces = [...document.querySelectorAll(".slide-nav__link")].map(
				(a) => a.getAttribute("href"),
			);

			/* Medir solo .slide__content no basta. Un bloque interior puede
			   rebosar su caja sin que el contenedor de la diapositiva crezca:
			   basta que algún ancestro recorte (La hora del código lleva
			   overflow:hidden para redondear sus esquinas) o que un hermano
			   posterior se pinte encima. Así se coló un prompt con la última
			   línea tapada que la comprobación daba por bueno.

			   La holgura aquí es de 4 px y no la general de 12: dentro de un
			   bloque no hay barra de desplazamiento que absorba nada, y 7 px de
			   texto tapado ya son una línea ilegible. */
			const HOLGURA_INTERIOR = 4;
			const nombre = (el) =>
				(typeof el.className === "string" ? el.className : "")
					.split(" ")
					.filter(Boolean)
					.slice(0, 2)
					.join(".") || el.tagName.toLowerCase();

			const recortes = [];
			// Se parte de los que RECORTAN, no de todos los elementos: medir
			// scrollHeight en cualquier nodo delata además cada descendente de
			// una tipografía apretada, que no pierde nada porque su contenedor
			// no recorta. Lo que importa es el texto que un borde se come.
			const recortadores = [
				...document.querySelectorAll(".slide__content, .slide__content *"),
			].filter((el) => {
				const o = getComputedStyle(el);
				return o.overflowY !== "visible" || o.overflowX !== "visible";
			});

			for (const clip of recortadores) {
				// Un <details> cerrado oculta su cuerpo a propósito: eso no es
				// contenido perdido, es el componente haciendo su trabajo.
				if (clip.closest("details:not([open])")) continue;
				const caja = clip.getBoundingClientRect();
				const fondo = caja.top + clip.clientTop + clip.clientHeight;
				for (const hijo of clip.querySelectorAll("*")) {
					if (hijo.closest("svg")) continue; // el SVG gestiona su viewBox
					const r = hijo.getBoundingClientRect();
					if (r.height === 0) continue;
					const exceso = Math.round(r.bottom - fondo);
					if (exceso > HOLGURA_INTERIOR) {
						recortes.push({
							donde: `${nombre(hijo)} dentro de ${nombre(clip)}`,
							exceso,
						});
						break; // con el primero basta para localizar la lámina
					}
				}
			}

			/* Segundo caso, más traicionero: una composición (grid o flex) cuyo
			   contenido no cabe en la fila que se le asignó. No la recorta
			   nadie —se sale por debajo— pero el bloque siguiente se pinta
			   encima y tapa las últimas líneas. Se limita a grid/flex a
			   propósito: en un párrafo suelto, scrollHeight mayor que
			   clientHeight solo delata un interlineado apretado, que no pierde
			   texto. */
			for (const el of document.querySelectorAll(".slide__content *")) {
				const display = getComputedStyle(el).display;
				if (display !== "grid" && display !== "flex") continue;
				const exceso = el.scrollHeight - el.clientHeight;
				if (exceso > HOLGURA_INTERIOR) {
					recortes.push({
						donde: `la composición ${nombre(el)}`,
						exceso,
					});
				}
			}

			/* Solapamiento: un elemento escalado con transform se ve grande pero
			   ocupa su caja original, así que puede montarse sobre el rótulo de
			   abajo sin que ningún contenedor desborde. Se detecta comparando la
			   caja pintada del componente con la del hermano siguiente. */
			const solapes = [];
			for (const hw of document.querySelectorAll(".hw-set")) {
				const caja = hw.getBoundingClientRect();
				const siguiente = hw.parentElement?.nextElementSibling;
				while (siguiente) {
					const otra = siguiente.getBoundingClientRect();
					if (otra.height > 0 && caja.bottom > otra.top + 2) {
						solapes.push(Math.round(caja.bottom - otra.top));
					}
					break;
				}
			}

			/* Alto necesario frente a alto disponible.

			   Medir `scrollHeight - clientHeight` sobre este contenedor no es
			   fiable: es un flex con `justify-content: safe center` que crece
			   para llenar la lámina, y su área de desplazamiento incorpora las
			   cajas transformadas de los descendientes. Eso devolvía desbordes
			   de exactamente un renglón, en láminas distintas en cada pasada.

			   Aquí se suelta la restricción de alto, se lee lo que el
			   contenido pide de verdad y se restaura. La resta es determinista
			   y responde a la única pregunta que importa: ¿cabe? */
			let desborde = 0;
			if (c) {
				const flex = c.style.flex;
				const alto = c.style.maxHeight;
				const disponible = c.clientHeight;
				c.style.flex = "0 0 auto";
				c.style.maxHeight = "none";
				desborde = c.scrollHeight - disponible;
				c.style.flex = flex;
				c.style.maxHeight = alto;
			}

			return {
				desborde,
				figuras,
				enlaces,
				recortes,
				solapes,
			};
		});

	let medida;
	try {
		medida = await medir();
	} catch {
		await pagina.waitForTimeout(500);
		medida = await medir();
	}

	if (medida.desborde > TOLERANCIA_PX) {
		problemas.push(`${d.rel}  desborda ${medida.desborde}px`);
	}
	for (const f of medida.figuras) {
		if (!f.cargada) problemas.push(`${d.rel}  figura sin cargar: ${f.nombre}`);
	}
	for (const href of medida.enlaces) {
		if (!href || href.startsWith("/") || href.startsWith("http")) continue;
		if (!existsSync(path.join(SLIDES, d.clase, href))) {
			problemas.push(`${d.rel}  enlace roto: ${href}`);
		}
	}
	for (const r of medida.recortes) {
		problemas.push(`${d.rel}  contenido tapado en ${r.donde} (${r.exceso}px)`);
	}
	for (const s of medida.solapes) {
		problemas.push(`${d.rel}  .hw-set se monta ${s}px sobre lo que sigue`);
	}
	for (const e of errores) {
		problemas.push(`${d.rel}  error de consola: ${e}`);
	}

	if (soloCaptura) {
		const nombre = d.rel.replace("/", "__").replace(".html", ".png");
		await pagina.screenshot({ path: path.join(CAPTURAS, nombre) });
	}
}

await navegador.close();

/* La portada del proyecto enlaza a mano una tarjeta por sesión, y por eso se
   queda atrás cada vez que se añade una: nada la obligaba a estar completa.
   Se comprueba aquí, no en una pasada aparte, porque es el mismo tipo de
   fallo que los enlaces rotos entre láminas. */
if (!filtro) {
	const portada = readFileSync(path.join(RAIZ, "index.html"), "utf8");
	for (const clase of readdirSync(SLIDES)
		.filter((d) => d.startsWith("clase-"))
		.sort()) {
		if (!portada.includes(`/src/slides/${clase}/`)) {
			problemas.push(`index.html  no enlaza a ${clase}`);
		}
	}
}

console.log(`Revisadas ${diapositivas.length} diapositivas.`);
if (problemas.length === 0) {
	console.log("Sin problemas.");
} else {
	console.log(`\n${problemas.length} problema(s):`);
	for (const p of problemas) console.log(`  · ${p}`);
	process.exitCode = 1;
}
