/* Decide, por lámina, qué bloque debe reclamar el alto sobrante.
 *
 * `is-stretch` no es una mejora automática: marcar el bloque equivocado empeora
 * la lámina. Estirar un split cuya columna visual no puede crecer despega el
 * texto del título y parte el vacío en dos; estirar un bloque de texto le
 * infla el relleno. En la sesión 1 esa decisión se tomó a ojo, lámina por
 * lámina, y por eso no llegó a las otras once.
 *
 * Aquí se toma midiendo: para cada candidato se aplica la clase en el
 * navegador, se vuelve a medir el mayor vacío contiguo y se conserva el
 * candidato que más lo reduce. Si ninguno mejora por encima del margen, la
 * lámina se declara sin propuesta y queda para revisión a mano — es el caso de
 * las láminas que simplemente tienen menos contenido que espacio, donde el
 * arreglo no es de reparto sino de contenido.
 *
 * No modifica ningún archivo: emite el plan en JSON para aplicarlo aparte.
 *
 * Uso:  node tools/proponer-stretch.mjs [clase-03] [--umbral 140] [--margen 40]
 *       node tools/proponer-stretch.mjs --json plan.json
 */
import { readdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { chromium } from "playwright";
import {
	medirHueco,
	prepararLamina,
	UMBRAL_POR_OMISION,
} from "./lib/medir-hueco.mjs";
import { asegurarServidor } from "./lib/servidor.mjs";

const RAIZ = path.resolve(import.meta.dirname, "..");
const BASE = "http://localhost:5173";
const SLIDES = path.join(RAIZ, "src", "slides");

const args = process.argv.slice(2);
const leer = (bandera, omision) => {
	const i = args.indexOf(bandera);
	return i === -1 ? omision : args[i + 1];
};
const UMBRAL = Number(leer("--umbral", UMBRAL_POR_OMISION));
const MARGEN = Number(leer("--margen", 40));
const JSON_SALIDA = leer("--json", null);
const banderas = new Set(["--umbral", "--margen", "--json"]);
const filtro = args.find(
	(a, i) => !a.startsWith("--") && !banderas.has(args[i - 1]),
);

const laminas = [];
for (const clase of readdirSync(SLIDES).sort()) {
	for (const archivo of readdirSync(path.join(SLIDES, clase)).sort()) {
		if (!archivo.endsWith(".html")) continue;
		const rel = `${clase}/${archivo}`;
		if (filtro && !rel.includes(filtro)) continue;
		laminas.push(rel);
	}
}

await asegurarServidor();

const navegador = await chromium.launch({ channel: "chrome" });
const pagina = await navegador.newPage({
	viewport: { width: 1440, height: 900 },
});

const plan = [];
const sinPropuesta = [];

for (const rel of laminas) {
	await pagina.goto(`${BASE}/src/slides/${rel}`, { waitUntil: "networkidle" });
	await prepararLamina(pagina);

	const antes = await medirHueco(pagina);
	if (!antes || antes.px < UMBRAL) {
		process.stdout.write(".");
		continue;
	}
	/* Candidatos de estiramiento: los hijos directos que pueden absorber alto.
	   Un bloque de texto suelto no está en la lista a propósito — estirarlo le
	   infla el relleno en vez de repartir contenido.

	   Si la lámina YA trae un is-stretch puesto a mano, ese es el único
	   candidato: se le añaden repartos, pero no se mueve. El aplicador solo
	   sabe añadir clases, no quitarlas, así que proponer moverlo daría un plan
	   que no se puede aplicar; y además esa elección se revisó por captura en
	   su día. */
	const estirables = await pagina.evaluate(() => {
		const raiz = document.querySelector(".slide__content");
		const yaPuesto = [...raiz.children].findIndex((el) =>
			el.classList.contains("is-stretch"),
		);
		if (yaPuesto !== -1) return [yaPuesto];
		const puede = (el) =>
			el.matches(".layout, .slide__split, .grid, .table-scroll") ||
			!!el.querySelector(".table-scroll, .problem-card, .usecase, .compare");
		return [...raiz.children]
			.map((el, i) => ({ i, apto: puede(el) }))
			.filter((c) => c.apto)
			.map((c) => c.i);
	});

	/* Todas las combinaciones se prueban de verdad y se comparan por medición.
	   El reparto (`is-spread`) sirve donde el estiramiento no: láminas de tres
	   o cuatro bloques de texto, que son la mayoría de los casos que quedan.
	   `columna` reparte dentro de la columna de texto de un split estirado,
	   que es donde se junta el vacío cuando la columna visual no puede crecer
	   —un panel de simulación, una figura de proporción fija—. */
	const REPARTOS = ["", "lamina", "columna", "lamina+columna"];
	const variantes = [];
	for (const estirar of [null, ...estirables]) {
		for (const repartir of REPARTOS) {
			if (estirar === null && repartir === "") continue; // el estado actual
			variantes.push({ estirar, repartir });
		}
	}

	let mejor = null;
	for (const v of variantes) {
		await pagina.evaluate((w) => {
			const raiz = document.querySelector(".slide__content");
			for (const el of raiz.querySelectorAll(".is-spread"))
				el.classList.remove("is-spread");
			raiz.classList.remove("is-spread");
			for (const el of raiz.children) el.classList.remove("is-stretch");

			if (w.estirar !== null)
				raiz.children[w.estirar].classList.add("is-stretch");
			if (w.repartir.includes("lamina")) raiz.classList.add("is-spread");
			if (w.repartir.includes("columna")) {
				const col = raiz.querySelector(
					".is-stretch.slide__split > .slide__split-text",
				);
				if (col) col.classList.add("is-spread");
			}
		}, v);
		await pagina.waitForTimeout(140);
		const m = await medirHueco(pagina);
		/* Estirar puede provocar desbordamiento: si el contenido deja de caber
		   la propuesta no vale, por mucho que el hueco baje. */
		const desborda = await pagina.evaluate(() => {
			const c = document.querySelector(".slide__content");
			return c.scrollHeight - c.clientHeight > 12;
		});
		if (desborda) continue;
		if (!mejor || m.px < mejor.despues.px) {
			/* El bloque se identifica por sus clases de ORIGEN, no por su
			   posición: en las sesiones 5-12 la fuente es el generador, donde
			   `cabecera()` emite dos hijos que en el archivo no se ven, así que
			   el índice del navegador no coincide con el del código. `is-visible`
			   la añade la entrada escalonada en tiempo de ejecución y no está en
			   la fuente; fuera. */
			const seña =
				v.estirar === null
					? null
					: await pagina.evaluate((k) => {
							const raiz = document.querySelector(".slide__content");
							const el = raiz.children[k];
							const clases = [...el.classList].filter(
								(c) => c !== "is-stretch" && c !== "is-visible",
							);
							const firma = clases.join(" ");
							const mismos = [...raiz.children].filter(
								(h) =>
									[...h.classList]
										.filter((c) => c !== "is-stretch" && c !== "is-visible")
										.join(" ") === firma,
							);
							return {
								etiqueta: el.tagName.toLowerCase(),
								clases: firma,
								ordinal: mismos.indexOf(el),
								hermanos: mismos.length,
							};
						}, v.estirar);
			mejor = { ...v, seña, despues: m };
		}
	}

	if (mejor && antes.px - mejor.despues.px >= MARGEN) {
		plan.push({
			lamina: rel,
			repartir: mejor.repartir,
			estirar: mejor.seña,
			antes: antes.px,
			despues: mejor.despues.px,
			donde: mejor.despues.donde,
		});
		process.stdout.write("+");
	} else {
		sinPropuesta.push({
			lamina: rel,
			antes: antes.px,
			donde: antes.donde,
			mejorPosible: mejor ? mejor.despues.px : null,
		});
		process.stdout.write("!");
	}
}

await navegador.close();

console.log(`\n\n=== Propuestas (${plan.length}) ===`);
for (const p of plan.sort(
	(a, b) => b.antes - b.despues - (a.antes - a.despues),
)) {
	const qué = [
		p.estirar
			? `estirar ${p.estirar.etiqueta}.${p.estirar.clases.split(" ")[0]}`
			: null,
		p.repartir ? `repartir ${p.repartir}` : null,
	]
		.filter(Boolean)
		.join(" + ");
	console.log(
		`  ${String(p.antes).padStart(4)} → ${String(p.despues).padStart(3)} px  ${p.lamina}  [${qué}]`,
	);
}

console.log(`\n=== Sin propuesta (${sinPropuesta.length}) ===`);
for (const s of sinPropuesta.sort((a, b) => b.antes - a.antes)) {
	const m =
		s.mejorPosible === null ? "sin candidato" : `mejor ${s.mejorPosible}`;
	console.log(
		`  ${String(s.antes).padStart(4)} px  ${s.lamina}  (${s.donde}, ${m})`,
	);
}

if (JSON_SALIDA) {
	writeFileSync(
		JSON_SALIDA,
		`${JSON.stringify({ plan, sinPropuesta }, null, 2)}\n`,
	);
	console.log(`\nPlan escrito en ${JSON_SALIDA}`);
}
