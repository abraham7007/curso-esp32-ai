/* Comprueba que el puerto 5173 lo sirve ESTE proyecto y no otro.
 *
 * En este equipo conviven varios cursos, cada uno con su Vite. El puerto lo
 * toma el que arranca primero, y el siguiente se va al 5174 sin avisar. El día
 * que este proyecto se caiga y arranque otro antes, todos los verificadores
 * seguirían respondiendo «sin problemas» — sobre un mazo distinto.
 *
 * Un fallo así no se nota: no hay error, hay un informe correcto de otra cosa.
 * Por eso cada herramienta que lee del servidor llama a esto antes de empezar.
 */
import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";

const RAIZ = path.resolve(import.meta.dirname, "..", "..");

/** Aborta si el servidor no responde o si no es el de este proyecto. */
export async function asegurarServidor(base = "http://localhost:5173") {
	const clases = readdirSync(path.join(RAIZ, "src", "slides")).sort();
	const clase = clases[clases.length - 1];
	const archivo = readdirSync(path.join(RAIZ, "src", "slides", clase))
		.filter((f) => f.endsWith(".html"))
		.sort()
		.pop();
	const rel = `src/slides/${clase}/${archivo}`;

	/* El código de estado NO sirve para distinguir un servidor de otro: ante
	   una ruta que no conoce, Vite devuelve 200 con su índice en vez de 404.
	   La primera versión de esta comprobación daba por bueno el servidor del
	   otro curso por ese motivo. Se compara el TÍTULO que devuelve con el del
	   archivo en disco, que es único de esta lámina. */
	const titulo = (readFileSync(path.join(RAIZ, rel), "utf8").match(
		/<title>([^<]*)<\/title>/,
	) ?? [])[1];

	let servido;
	try {
		const r = await fetch(`${base}/${rel}`, {
			signal: AbortSignal.timeout(5000),
		});
		servido = ((await r.text()).match(/<title>([^<]*)<\/title>/) ?? [])[1];
	} catch (e) {
		console.error(
			`\nEl servidor de desarrollo no responde en ${base}.\n` +
				`Arráncalo con «npm run dev» y vuelve a ejecutar.\n` +
				`Detalle: ${e.message}\n`,
		);
		process.exit(2);
	}

	if (servido !== titulo) {
		console.error(
			`\n${base} responde, pero NO es el servidor de este proyecto.\n\n` +
				`  se esperaba: «${titulo}»\n` +
				`  se recibió : «${servido ?? "(sin título)"}»\n\n` +
				`Otro proyecto se ha quedado con el puerto. Compruébalo con:\n` +
				`  lsof -nP -iTCP:5173 -sTCP:LISTEN\n\n` +
				`Sin esta parada, la verificación habría dado «sin problemas» sobre\n` +
				`un mazo que no es este.\n`,
		);
		process.exit(2);
	}
}
