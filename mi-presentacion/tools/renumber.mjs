/* Reordena y renumera las diapositivas de una sesión.

   Insertar una lámina en medio de una sesión obliga a renombrar todas las
   siguientes, reescribir los enlaces anterior/siguiente de cada vecina y
   corregir el total en <body data-deck-total>. Hecho a mano son decenas de
   ediciones y basta una para romper la cadena de navegación en silencio.

   El orden deseado se declara en un archivo de plan JSON:

     {
       "clase": "clase-01",
       "orden": ["portada", "clasificacion-dispositivo", ...]
     }

   donde cada elemento es el "slug" del archivo (el nombre sin el número ni
   la extensión). Los archivos nuevos deben existir ya en el directorio con
   CUALQUIER número: este script les asigna el que les toca.

   El rótulo con el que cada lámina aparece en la navegación de sus vecinas
   se conserva: se deduce leyendo cómo la enlazan hoy. Para una lámina nueva
   se toma de su propio <h1>/<h2>, o del <title> como último recurso.

   Uso:  node tools/renumber.mjs plan.json
         node tools/renumber.mjs plan.json --dry     (solo informa)
*/

import { readdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import path from "node:path";

const RAIZ = path.resolve(import.meta.dirname, "..");
const SLIDES = path.join(RAIZ, "src", "slides");

const [planPath, ...resto] = process.argv.slice(2);
if (!planPath) {
	console.error("Uso: node tools/renumber.mjs <plan.json> [--dry]");
	process.exit(1);
}
const soloInforme = resto.includes("--dry");

const plan = JSON.parse(readFileSync(planPath, "utf8"));
const dir = path.join(SLIDES, plan.clase);

const slugDe = (archivo) => archivo.replace(/^\d+-/, "").replace(/\.html$/, "");
const dosDigitos = (n) => String(n).padStart(2, "0");

const actuales = readdirSync(dir)
	.filter((f) => f.endsWith(".html"))
	.sort();

const porSlug = new Map(actuales.map((f) => [slugDe(f), f]));

// El rótulo de navegación de cada lámina: lo que escriben sus vecinas dentro
// del <span> del enlace. Se recoge antes de tocar nada.
const rotulos = new Map();
for (const archivo of actuales) {
	const html = readFileSync(path.join(dir, archivo), "utf8");
	const re =
		/<a class="slide-nav__link" href="([^"]+\.html)"[\s\S]*?<span>([\s\S]*?)<\/span>/g;
	for (const m of html.matchAll(re)) {
		const destino = slugDe(m[1]);
		if (!rotulos.has(destino)) {
			rotulos.set(destino, m[2].replace(/\s+/g, " ").trim());
		}
	}
}

// Para una lámina nueva que nadie enlaza todavía: su propio encabezado.
function rotuloPropio(archivo) {
	const html = readFileSync(path.join(dir, archivo), "utf8");
	const h =
		html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) ||
		html.match(/<h2[^>]*>([\s\S]*?)<\/h2>/) ||
		html.match(/<title>([\s\S]*?)<\/title>/);
	if (!h) return slugDe(archivo);
	return h[1]
		.replace(/<[^>]+>/g, "")
		.split("·")[0]
		.replace(/\s+/g, " ")
		.trim();
}

const faltantes = plan.orden.filter((s) => !porSlug.has(s));
if (faltantes.length) {
	console.error(`No existen estos archivos en ${plan.clase}:`);
	for (const s of faltantes) console.error(`  · ${s}.html`);
	process.exit(1);
}
const sobrantes = [...porSlug.keys()].filter((s) => !plan.orden.includes(s));
if (sobrantes.length) {
	console.error(`El plan no menciona estas láminas de ${plan.clase}:`);
	for (const s of sobrantes) console.error(`  · ${porSlug.get(s)}`);
	process.exit(1);
}

const total = plan.orden.length;
const destino = plan.orden.map((slug, i) => ({
	slug,
	desde: porSlug.get(slug),
	hacia: `${dosDigitos(i + 1)}-${slug}.html`,
	rotulo: rotulos.get(slug) || rotuloPropio(porSlug.get(slug)),
}));

console.log(`${plan.clase}: ${total} láminas`);
for (const [i, d] of destino.entries()) {
	if (d.desde !== d.hacia) console.log(`  ${d.desde}  →  ${d.hacia}`);
	else if (i === 0) console.log(`  ${d.hacia}  (sin cambio)`);
}
if (soloInforme) process.exit(0);

/* Renombrado en dos pasos, vía nombres temporales. Un renombrado directo
   puede pisar un archivo que todavía no se ha movido (05→06 antes de que
   06→07 haya ocurrido) y perderlo sin aviso. */
for (const d of destino) {
	if (d.desde !== d.hacia) {
		renameSync(path.join(dir, d.desde), path.join(dir, `~tmp~${d.hacia}`));
	}
}
for (const d of destino) {
	if (d.desde !== d.hacia) {
		renameSync(path.join(dir, `~tmp~${d.hacia}`), path.join(dir, d.hacia));
	}
}

const icono = (nombre) =>
	`<svg class="icon" aria-hidden="true"><use href="/course-icons.svg#${nombre}" /></svg>`;

function bloqueNav(i) {
	const prev = i > 0 ? destino[i - 1] : null;
	const next = i < total - 1 ? destino[i + 1] : null;
	const lineas = [
		'\t\t\t<nav class="slide-nav" aria-label="Navegación de la diapositiva">',
	];
	if (prev) {
		lineas.push(
			`\t\t\t\t<a class="slide-nav__link" href="${prev.hacia}">`,
			`\t\t\t\t\t${icono("i-flow")}`,
			`\t\t\t\t\t<span>${prev.rotulo}</span>`,
			"\t\t\t\t</a>",
		);
	} else {
		// La portada no tiene anterior, pero el hueco debe existir para que
		// el enlace "siguiente" siga alineado a la derecha.
		lineas.push("\t\t\t\t<span></span>");
	}
	if (next) {
		lineas.push(
			`\t\t\t\t<a class="slide-nav__link" href="${next.hacia}">`,
			`\t\t\t\t\t<span>${next.rotulo}</span>`,
			`\t\t\t\t\t${icono("i-flow")}`,
			"\t\t\t\t</a>",
		);
	} else {
		lineas.push("\t\t\t\t<span></span>");
	}
	lineas.push("\t\t\t</nav>");
	return lineas.join("\n");
}

for (const [i, d] of destino.entries()) {
	const archivo = path.join(dir, d.hacia);
	let html = readFileSync(archivo, "utf8");

	html = html.replace(
		/<nav class="slide-nav"[\s\S]*?<\/nav>/,
		bloqueNav(i).replace(/^\t{3}/, ""),
	);
	html = html.replace(/data-deck-total="\d+"/, `data-deck-total="${total}"`);

	writeFileSync(archivo, html, "utf8");
}

console.log(`Navegación reescrita y data-deck-total = ${total}.`);
console.log("Recuerda reiniciar el servidor de desarrollo antes de verificar.");
